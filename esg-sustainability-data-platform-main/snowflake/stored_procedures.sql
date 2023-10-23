create or replace procedure DL_ESG_DEV.ESG_CONFIGURATION.Create_table_historical_load_sales("Database" varchar(16777216))
RETURNS VARIANT
Language Javascript
execute as owner
AS
$$
try{
var msg = [];
    var db = Database;
    msg.push({prc:"Create_table_historical_load:" +new Date().toISOString(),txt:"start"});
    var list_tables_stmt = snowflake.createStatement({
    sqlText: `select tgtschema,targetschema,srctbl from config_tbl where srcdb = '`+db+`';`
    });
    var tables = list_tables_stmt.execute();

    msg.push({prc: "TABLES :" + tables[0],txt: "Base table dropped"});
 
 while(tables.next())
 {
  var database = 'DL_ESG_DEV';
  var db_schema = tables.getColumnValue(1)
  var table = tables.getColumnValue(3)
  var table_schema = tables.getColumnValue(2).replaceAll("|",",");
  var table_schema_split = tables.getColumnValue(2).split("|");
  var table_schema_staging = table_schema_split.map(stagingSchemaMapping).toString();
  
function stagingSchemaMapping(str)
    {
    var splitted_str = str.split(" ")
    return splitted_str[0] + " varchar";
    }
  
  //drop base table
    var truncate_qry_bs = `drop table if exists ` + database + `.` +db_schema + `.` + table + `;`
    var truncate_stmt_bs = snowflake.createStatement({sqlText: truncate_qry_bs});
    truncate_stmt_bs.execute();
  msg.push({prc: "Create_table_historical_load :" + table,txt: "Base table dropped"});
    
    
  //create base table
    var stage_create_qry_bs = `create or replace table ` + database + `.` +db_schema + `.` + table + ` (` + table_schema + `);`
    var create_stmt_bs = snowflake.createStatement({sqlText: stage_create_qry_bs});
    create_stmt_bs.execute()
  msg.push({prc: "Create_table_historical_load :" + table,txt: "Base table created"});
  
  //drop staging table
    var truncate_qry_stg = `drop table if exists ` + database + `.` +db_schema + `._TMP_` + table + `;`
    var truncate_stmt_stg = snowflake.createStatement({sqlText: truncate_qry_stg});
    truncate_stmt_stg.execute();
  msg.push({prc: "Create_table_historical_load :" + table,txt: "Stage table dropped"});
    
    
//create create staging table
   var stage_create_qry_stg = `create or replace table ` + database + `.` +db_schema + `._TMP_` + table + ` (` + table_schema_staging + `);`
    var create_stmt_stg = snowflake.createStatement({sqlText: stage_create_qry_stg});
    create_stmt_stg.execute()
  msg.push({prc: "Create_table_historical_load :" + table,txt: "Stage table created" + stage_create_qry_stg});
 }
  return{status:1, ret: "success",msg:msg}
    
    }
catch(err){
    msg.push({prc:"Create_table_historical_load:" +new Date().toISOString(),txt:"stage:",Failed:  + err + table_schema_staging});
    return{status:0, ret:null, msg:msg};
}
$$;


create or replace procedure DL_ESG_DEV.ESG_CONFIGURATION.historical_full_load_sales("Database" varchar(16777216))
RETURNS VARIANT
Language Javascript
execute as caller
AS
$$
try{
    var msg = [];
    var tblName;
    var db = Database;
    msg.push({prc:"Historical_full_load: " + new Date().toISOString(),txt:"start"})
    
    //list the table in source schema
    var table_filter = `select tgtdb,targetschema,srctbl,adlsfile,tgtschema,sourcecolumn
     from DL_ESG_DEV.ESG_CONFIGURATION.config_tbl where srcdb = 'pocdb';`
     
 msg.push({prc:"Historical_full_load1: " + new Date().toISOString(),txt:"running"})
   // from config_tbl where srcdb = '`+db+`';`
    
    var table_filter_stmt = snowflake.createStatement({sqlText: table_filter});
    msg.push({prc:"Historical_full_load1: " + new Date().toISOString(),txt:"completed "+table_filter})
    var tables = table_filter_stmt.execute();
    msg.push({prc:"Historical_full_load1: " + new Date().toISOString(),txt:"completed "+tables.toString()})
    
    while (tables.next())
        {
        var database = tables.getColumnValue(1);
        var col_schema = tables.getColumnValue(2);
        var table = tables.getColumnValue(3);
        var adls_path = tables.getColumnValue(4);
        var db_schema = tables.getColumnValue(5);
        var col_list = tables.getColumnValue(6);
        msg.push({prc:"Historical_full_load1: " + new Date().toISOString(),txt:"parsing "+table})
        
//Generate schema with try cast
        var split_col_schema = col_schema.split("|");
        msg.push({prc:"Historical_full_load1: " + new Date().toISOString(),txt:"splitting" +split_col_schema})
        var col_schema_trycast = split_col_schema.map(addTryCastSales).toString();
        msg.push({prc:"Historical_full_load1: " + new Date().toISOString(),txt:"tcast" +col_schema_trycast})
        var col_schema_parse = split_col_schema.map(jsonparseSales).toString();
        msg.push({prc:"Historical_full_load1: " + new Date().toISOString(),txt:"json"})
        tblName = table;
        
//function to add try cast
        function addTryCastSales(str)
            {
            var splitted_str = str.split(' ')
            // return + splitted_str[0] + " " +splitted_str[1];
            return "try_cast(" + splitted_str[0] + " as " +splitted_str[1] +")";
           // return "try_cast("+ splitted_str[0] " as "+ splitted_str[1]")";
            }
//function to create json parsing statement
        function jsonparseSales(str)
            {
            var splitted_str = str.split(" ")
//            return "src:" + splitted_str[0] + ":: VARCHAR(16777216) AS " + splitted_str[0];
            return "$1:" + splitted_str[0];
            }
            
//truncate temp table
    var truncate_qry = `truncate table ` + database + `.` + db_schema +`.` + table +`;`
    var truncate_qry_stmt = snowflake.createStatement({sqlText: truncate_qry});
    truncate_qry_stmt.execute();
    msg.push({prc:"Historical_full_load: " + table,txt:"Trucate staging table completed"})
        
//copy to src variant temp table
        var copy_to_stage_qry = `copy into ` + database + `.` + db_schema + `.` + table + ` FROM (SELECT `+ col_schema_parse +` from @DL_ESG_DEV.external_stages.aws_stage/` +adls_path+`) FILE_FORMAT = DL_ESG_DEV.CUSTOMER.raw_json_format FORCE = true;`
        var copy_to_stage_stmt = snowflake.createStatement({sqlText: copy_to_stage_qry});
        
        msg.push({prc: "Historical_full_load: "+ table,txt:"src variant table loaded " + copy_to_stage_qry})
        copy_to_stage_stmt.execute();
        msg.push({prc: "Historical_full_load: "+ table,txt:"src variant table loaded"})
 
    }
    
    return{status:1, ret: "success",msg:msg}
    }
    
catch(err){
    msg.push({prc:"Historical_full_load:" +new Date().toISOString(),txt:"stage:",Failed:  + err});
    return{status:0, ret:null, msg:msg};
}
$$;