create or replace TABLE CONFIG_TBL (
	SERIALNUM NUMBER(38,0) autoincrement,
	SRCTBL VARCHAR(16777216),
	SRCDB VARCHAR(16777216),
	SRCHSCHEMA VARCHAR(16777216),
	TGTTBL VARCHAR(16777216),
	TGTDB VARCHAR(16777216),
	TGTSCHEMA VARCHAR(16777216),
	SOURCECOLUMN VARCHAR(16777216),
	SOURCESCHEMA VARCHAR(16777216),
	TARGETSCHEMA VARCHAR(16777216),
	WATERMARKCOLUMN VARCHAR(16777216),
	PRIMARYKEY VARCHAR(16777216),
	FREQUENCY VARCHAR(16777216),
	APPNAME VARCHAR(16777216),
	ADLSCONTAINER VARCHAR(16777216),
	ADLSFOLDER VARCHAR(16777216),
	ADLSFILE VARCHAR(16777216),
	ISACTIVE VARCHAR(16777216),
	ISPROCESSED VARCHAR(16777216),
	LASTPROCESSED TIMESTAMP_NTZ(9)
);


INSERT INTO DL_ESG_DEV.ESG_CONFIGURATION.CONFIG_TBL(srctbl,srcdb,srchschema,tgttbl,tgtdb,tgtschema,sourcecolumn,sourceschema,targetschema,watermarkcolumn,primarykey,frequency,appname,adlscontainer,adlsfolder,adlsfile,isactive,isprocessed) 
VALUES ('customer', 'pocdb', 'SalesLT','customer', 'DL_ESG_DEV','CUSTOMER', 
        'C_ID,FIRST_NAME,LAST_NAME,EMAIL,GENDER,AGE,PORTFOLIO_ID',
        'C_ID nvarchar|FIRST_NAME nvarchar|LAST_NAME nvarchar|EMAIL nvarchar|GENDER nvarchar|AGE nvarchar|PORTFOLIO_ID nvarchar', 
        'C_ID varchar|FIRST_NAME varchar|LAST_NAME varchar|EMAIL varchar|GENDER varchar|AGE varchar|PORTFOLIO_ID varchar' ,
        '' , 'C_ID','A', 'coc','raw', 'coc','coc/customer', 1, 0);

        
INSERT INTO DL_ESG_DEV.ESG_CONFIGURATION.CONFIG_TBL(srctbl,srcdb,srchschema,tgttbl,tgtdb,tgtschema,sourcecolumn,sourceschema,targetschema,watermarkcolumn,primarykey,frequency,appname,adlscontainer,adlsfolder,adlsfile,isactive,isprocessed) 
VALUES ('portfolio', 'pocdb', 'SalesLT','portfolio', 'DL_ESG_DEV','CUSTOMER', 
        'R_ID,P_ID,TICKER,BUY_DATE,BUY_VALUE,SHARES_,CURRENCY,OWNED,ADVISOR_ID',
        'R_ID nvarchar|P_ID nvarchar|TICKER nvarchar|BUY_DATE nvarchar|BUY_VALUE nvarchar|SHARES_ nvarchar|CURRENCY nvarchar|OWNED nvarchar|ADVISOR_ID nvarchar', 
        'R_ID varchar|P_ID varchar|TICKER varchar|BUY_DATE varchar|BUY_VALUE varchar|SHARES_ varchar|CURRENCY varchar|OWNED varchar|ADVISOR_ID varchar' ,
        '' , 'R_ID','A', 'coc','raw', 'coc','coc/portfolio', 1, 0);


