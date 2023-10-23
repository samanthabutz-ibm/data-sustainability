from snowflake.snowpark import Session
import streamlit as st  # pip install streamlit

from codes.dashboard1 import dashboard1
from codes.dashboard2 import dashboard2
from codes.dashboard3 import dashboard3
from codes.dashboard4 import dashboard4
from connection.connection import connection_paramter,cp



# def navbar():
#     pass

#st.set_page_config(layout='wide')
#make it look nice from the start
# st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)



# def navigation():
#     try:
#         path = st.experimental_get_query_params()['p'][0]
#     except Exception as e:
#         st.error('Please use the main app.')
#         return None
#     return path

def main(name, cp, authenticator):

    if "page" not in st.session_state:
        st.session_state.page = 1


    def restart(): st.session_state.page = 1
    def db1(): st.session_state.page=1        
    def db2(): st.session_state.page=2
    def db3(): st.session_state.page=3
    def db4(): 
        st.session_state.sTicker=''
        st.session_state.cmp_index=-1
        st.session_state.page=4
                # st.session_state.sTicker=selected_ticker
    # def db4_1(selected_ticker): 
    #     st.session_state.page=4
    #     sTicker=selected_ticker

    # def db4_1(selected_ticker): 
    #     st.session_state.page=4
    #     sTicker=selected_ticker

    

    # specify the primary menu definition
    # menu_data = [
    #     {'id':'ESG Score','icon':"〽️",'label':"",'ttip':"ESG Score"},
    #     {'id':'Chart2','icon': "far fa-chart-bar",'label':"",'ttip':"DB 2"},#no tooltip message
    #     {'id':'Chart3','icon': "💹",'label':"",'ttip':"Chart3"}, #can add a tooltip message
    #     {'id':'Chart4','icon': "💬", 'label':"", 'ttip':"Contact and Support"},
    # ]

    # over_theme = {'txc_inactive': '#ffffff'}
    # over_theme = {'txc_inactive': 'white','menu_background':'#85e0a5'}
    # menu_id = hc.nav_bar(
    #     menu_definition=menu_data,
    #     override_theme=over_theme,
    #     home_name='Home',
    #     login_name='Logout',
    #     # hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    #     # sticky_nav=True, #at the top or not
    #     # sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    # )

    #if st.button('click me'):
     #   st.info('You clicked at: {}'.format(menu_id))


    #get the id of the menu item clicked
    # st.info(f"{menu_id}")

    ## Header
    # navbar()

    # menu_id = hc.nav_bar(
    #     menu_definition=menu_data,
    #     override_theme=over_theme,
    #     home_name='Home',
    #     hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    #     sticky_nav=True, #at the top or not
    #     sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
    # )

    # def clear_session():
    # # Clear session state
    #     for key in st.session_state.keys():
    #         del st.session_state[key]

    # ---- SIDEBAR ----
    # st.sidebar.button("Logout",  key="logout",on_click=clear_session) 
    authenticator.logout("Logout", "sidebar")


    #sidebarLoginList.empty()
    st.sidebar.title(f"Welcome, {name}")
    st.sidebar.write('''This tool is designed to help you analyse your current stock portfolio with respect to the impact on Environment, Social and Governance parameters from each individual stock held, eventually helping make better informed investment decisions.''')
   

    st.sidebar.markdown("***")

    s = """<style>
        .css-629wbf  {
            background-color: rgb(218,219,220);
            color:#000000;
            border-color: white;
            border-width:2px;
            width:100%;
            justify-content:left !important;
        }
        .css-629wbf:hover {
            color:black;
            border-color:#467a43;
            background-color:#9cc699;
            }
        .css-629wbf:active {
            color:black;
            border-color:#467a43;
            background-color:#9cc699;
            }

        .css-z09lfk  {
            background-color: rgb(128, 129, 130);
            color:white;
            border-color: gray;
            border-width:2px;
            width:100%;
            justify-content:left !important;
        }
        .css-z09lfk:hover {
            color:black;
            border-color:#467a43;
            background-color:#9de698;
            }
        .css-z09lfk:active {
            color:black;
            border-color:#467a43;
            background-color:#9de698;
            }
        </style>"""


    st.markdown(s, unsafe_allow_html=True)
    with st.sidebar:
        st.sidebar.button("Home",  key="db1Button",on_click=db1) 
        st.sidebar.button("My Portfolio Analysis", key="db2Button", on_click=db2)
        st.sidebar.button("My Portfolio Optimization", key="db3Button", on_click=db3)
        st.sidebar.button("Company Insights", key="db4Button", on_click=db4)

    if (st.session_state.page == 1):
        dashboard1(db2)

    elif (st.session_state.page == 2):
        dashboard2(name,cp) 

    elif (st.session_state.page == 3):
        dashboard3(name, cp)
        pass

    elif (st.session_state.page == 4):
        dashboard4(restart)