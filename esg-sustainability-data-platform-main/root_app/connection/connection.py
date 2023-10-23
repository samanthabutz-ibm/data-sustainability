

#st1.set_page_config(
#    page_title="My Streamlit App",
#    #page_icon=chart_with_upwards_trend,
#    layout="wide",
#    initial_sidebar_state="auto",
#    menu_items=None,
#)

import snowflake.connector
import yaml
import streamlit as st

# connection_paramter = snowflake.connector.connect(account = "se58322-fsesg",
#                         user="Muhammad Nauman",
#                         password="Muhammad23",
#                         role="DEVELOPER",
#                         warehouse="WH_ESG_SUSTAINABILITY",
#                         ocsp_fail_open=False)


#@st.cache_resource
def init_connection():
    return snowflake.connector.connect(account = "se58322-fsesg",
    user="ESGAdmin",
    password="esgadmin",
    role="RL_ESG_OBJECTS_DEVELOPER",
    warehouse="WH_ESG_SUSTAINABILITY",
    ocsp_fail_open=False)

connection_paramter = init_connection()

cp = connection_paramter.cursor()

# def cookie_function():
#     with open('./config.yaml') as file:
#     config = yaml.load(file, Loader=yaml.SafeLoader)
#     print('config', config)
#     authenticator = stauth.Authenticate(
#         credentials,
#         # config['credentials'],
#         config['cookie']['name'],
#         config['cookie']['key'],
#         config['cookie']['expiry_days'],
#         config['preauthorized']
#     )
