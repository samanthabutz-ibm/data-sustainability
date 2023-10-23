import streamlit as st  

@st.cache_data
def fetch_cust_score(name,_cp):
    try:
        _cp.execute("""select ACS.* from DM_ESG_DEV.ESG_MODELS.AVG_CUS_SCORE ACS
                    INNER JOIN DL_ESG_DEV.ESG_CONFIGURATION.USER_TABLE USR ON USR.C_ID=ACS.C_ID
                    WHERE USR.USERNAME =(?)""",[name])
        result = _cp.fetchone()
        print(result)
        return result
    except Exception as e:
        print('ERROR', str(e))
        return False


@st.cache_data
def fetch_stock_score(cust_id, _cp):
    try:
        _cp.execute("""select distinct avgss.ticker, avgss."name", avgss.ENVIRONMENTAL,avgss.social,avgss.governance, avgss.TOTAL_SCORE, prtf.SHARES_, 
        avgss.latest_price, (avgss.latest_price)*(prtf.SHARES_) as "Total value", avgss.ONE_YEAR_SPAN,avgss.ONE_MONTH_SPAN
        ,EBI."AVG_SCORE" "Industry_score" 
        from DL_ESG_DEV.CUSTOMER.PORTFOLIO prtf
        inner join DL_ESG_DEV.CUSTOMER.CUSTOMER cust ON cust.PORTFOLIO_ID=prtf.P_ID 
        inner join DM_ESG_DEV.ESG_MODELS.AVG_STOCK_SCORE avgss on avgss.ticker=prtf.ticker
        INNER JOIN DL_ESG_DEV.ESG.TRIAL_SCO_ESG_262 TSE ON TSE."ticker"=prtf.ticker
        inner join DM_ESG_DEV.ESG_MODELS.ESG_BY_INDUSTRY EBI oN TSE."industry"=EBI."industry" 
        WHERE avgss."name" is not null and cust.C_ID=(?);""",[cust_id])

        result = _cp.fetchall()
        return result
    except Exception as e:
        print('ERROR', str(e))
        return False  


@st.cache_data
def fetch_benchmarks(_cp):
    try:
        _cp.execute("""select avg(avg_esg_e),avg(avg_esg_s),avg(avg_esg_g), avg(avg_esg) from (
            select avg(tse."esg") avg_esg, avg(tse."esg_e") avg_esg_e, avg(tse."esg_s") avg_esg_s, avg(tse."esg_g") avg_esg_g
                    from DL_ESG_DEV.CUSTOMER.PORTFOLIO p
                    inner JOIN DL_ESG_DEV.ESG.TRIAL_SCO_ESG_262 tse ON p.TICKER = tse."ticker"
                    inner join DL_ESG_DEV.CUSTOMER.CUSTOMER cust ON cust.PORTFOLIO_ID = p.P_ID
                    inner join DM_ESG_DEV.ESG_MODELS.AVG_STOCK_SCORE avgss on avgss.ticker = p.ticker
                    group by p.p_id having avg(tse."esg")> (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (
                ORDER BY average_esg
                )
                FROM(
            select avg(tse."esg") average_esg, avg(tse."esg_e") avg_esg_e, avg(tse."esg_s") avg_esg_s, avg(tse."esg_g") avg_esg_g
                    from DL_ESG_DEV.CUSTOMER.PORTFOLIO p
                    inner JOIN DL_ESG_DEV.ESG.TRIAL_SCO_ESG_262 tse ON p.TICKER = tse."ticker"
                    inner join DL_ESG_DEV.CUSTOMER.CUSTOMER cust ON cust.PORTFOLIO_ID = p.P_ID
                    inner join DM_ESG_DEV.ESG_MODELS.AVG_STOCK_SCORE avgss on avgss.ticker = p.ticker
                    group by p.p_id)));""")

        top25 = _cp.fetchone()
        
        _cp.execute("""select avg(avg_esg_e),avg(avg_esg_s),avg(avg_esg_g), avg(avg_esg) from (
  select avg(tse."esg") avg_esg, avg(tse."esg_e") avg_esg_e, avg(tse."esg_s") avg_esg_s, avg(tse."esg_g") avg_esg_g
        from DL_ESG_DEV.CUSTOMER.PORTFOLIO p
        inner JOIN DL_ESG_DEV.ESG.TRIAL_SCO_ESG_262 tse ON p.TICKER = tse."ticker"
        inner join DL_ESG_DEV.CUSTOMER.CUSTOMER cust ON cust.PORTFOLIO_ID = p.P_ID
        inner join DM_ESG_DEV.ESG_MODELS.AVG_STOCK_SCORE avgss on avgss.ticker = p.ticker
        group by p.p_id);""")

        allC = _cp.fetchone()

        return allC,top25

    except Exception as e:
        print('ERROR', str(e))
        return False   


@st.cache_data
def fetch_all_comps(_cp):
    try:
        _cp.execute("""select distinct "ticker","name"  from "DL_ESG_DEV"."ESG"."TRIAL_SCO_ESG_262";""")
        result = _cp.fetchall()
        return result
    
    except Exception as e:
        print('ERROR', str(e))
        return False


@st.cache_data
def fetch_cmp_data(compname,_cp):
    try:
        _cp.execute("""select a."name",a."industry",a."dom_country_iso",a."esg_e",a."esg_s",a."esg_g",a."esg", b."AVG_SCORE",b."AVG_SCORE_E",b."AVG_SCORE_S",b."AVG_SCORE_G"
from DL_ESG_DEV.ESG.TRIAL_SCO_ESG_262 a  
inner join "DM_ESG_DEV"."ESG_MODELS"."ESG_BY_INDUSTRY" b on a."industry"=b."industry"
where a."ticker"=(?);""",[compname])

        result = _cp.fetchone()
        return result
    except Exception as e:
        print('ERROR', str(e))
        return False


@st.cache_data
def fetch_history_data(compname,_cp):
    try:
        _cp.execute("""select LATEST_PRICE,MONTH_1,MONTH_2,MONTH_3,MONTH_4,MONTH_5,MONTH_6 from "DM_ESG_DEV"."ESG_MODELS"."AVG_STOCK_SCORE" where "TICKER"=(?) limit 1""",[compname])
        result = _cp.fetchone()
        print(result)
        return result
    except Exception as e:
        print('ERROR', str(e))
        return False
    



@st.cache_data
def fetch_history_data1(ticker,curr_date,_cp):
    try:
        _cp.execute("""select ticker,
    date,
    monthname(date) || '''' || substr(year(date), 3, 4) as "xtick",
    close
from DL_ESG_DEV.FINANCIAL_MARKET.STOCK_DATA
where ticker = ((?))
    and date in (
        SELECT max(date) as date
        FROM DL_ESG_DEV.FINANCIAL_MARKET.STOCK_DATA
        where date < (select last_day((to_date((?)))- interval '1 month') + interval '1 day')
        and date>(select (last_day((to_date('2023-01-30'))- interval '1 month') + interval '1 day')- interval '12 month')
        GROUP BY month(date)
    )
    order by date asc;""" ,[ticker,curr_date])

        result1 = _cp.fetchall()
        print(result1)


        _cp.execute("""select LATEST_PRICE from "DM_ESG_DEV"."ESG_MODELS"."AVG_STOCK_SCORE" where ticker = (?);""",[ticker])
        
        result2 = _cp.fetchone()
        print(result2)


        return result2,result1
    except Exception as e:
        print('ERROR', str(e))
        return False


@st.cache_data
def fetch_index_score(_cp):
    try:
        _cp.execute("""select AVG("esg"),avg("esg_e"),avg("esg_s"),avg("esg_g") from "DL_ESG_DEV"."ESG"."TRIAL_SCO_ESG_262";""")

        result = _cp.fetchone()
        return result
    except Exception as e:
        print('ERROR', str(e))
        return False


@st.cache_data
def fetch_comp_insights(compname,_cp):
    try:
        _cp.execute("""select ENV_SOLS,WATER,RES_USE,ENV_SHP,WASTE,ENV_MNG,EMISSIONS,
PROD_ACS, COM_REL, QUALITY_SAFETY,TRN_DEV, HEALTH_SAFETY, LABOUR_RIGHTS, HUMAN_RIGHTS,EMPLOYMENT_QUALITY,DIVERSITY,COMPENSATION,
FORENSIC_ACCOUNTING, TRANSPARENCY, CORP_GOV,CAPITAL_STRUCTURE, BUSINESS_ETHICS
from "DL_ESG_DEV"."ESG"."ESG_DETAILS" where ticker =(?);""",[compname])

        result = _cp.fetchone()
        return result
    except Exception as e:
        print('ERROR', str(e))
        return False