import pickle
from pathlib import Path

from snowflake.snowpark import Session

import streamlit as st  # pip install streamlit

st.set_page_config(
   page_title="My Streamlit App",
   #page_icon=chart_with_upwards_trend,
   layout="wide",
   initial_sidebar_state="auto",
   menu_items=None,
)

import codes.main_app as main

import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
import hashlib

from  connection.connection import connection_paramter,cp

# st.markdown('''
#     <style>
#     body { 
#         margin: -100px; font-family: Arial, Helvetica, sans-serif;
#         } 
#     .header
#         {
#             padding: 30px 20px; background: green; color: blue; position:fixed;top:0;width: 80%;
#         } 
#     .sticky { 
#         position: fixed; top: 10; width: 80%;
#         } 
#     </style>
#     <div class="header" id="myHeader"></div>''', unsafe_allow_html=True)

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
 
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
 
def add_user(username,password):
    cp.execute("insert into DL_ESG_DEV.ESG_CONFIGURATION.user_table "
                "values (?, ?)", (username,password))
   
def login_user(username,password):
    try:
        cp.execute("select username from DL_ESG_DEV.ESG_CONFIGURATION.user_table"
        " where username = (?) and password =(?)", (username,password))
        return cp.fetchone()[0]
    except:
        return False

def fetch_users_dict():
    res_dict = {'usernames': {}}
    try:
        cp.execute("select username, password from DL_ESG_DEV.ESG_CONFIGURATION.user_table")
        result = cp.fetchall()
    except:
        return res_dict

    for res in result:
        # print(res)
        res_dict['usernames'][res[0]] = {'name':res[0], 'password':res[1]}

    # print(res_dict)

    return res_dict


def upsert_users_dict():
    old_users = fetch_users_dict()['usernames']
    new_users = authenticator.credentials['usernames']

    for user in new_users:
        if user not in list(old_users.keys()):
            print('Adding User:', user)
            try:
                # cp.execute("insert into DL_ESG_DEV.ESG_CONFIGURATION.user_table "
                #     "values (?, ?)", (new_users['name'],new_users['password']))
                add_user(new_users[user]['name'],new_users[user]['password'])
            except Exception as e:
                print('ERROR', str(e))
                # return False

    # print(new_users)


# menu = ["Home","Login","SignUp"]
# choice = st.sidebar.selectbox("Menu",menu)
 
# if choice == "Home":
#     st.subheader("Home")
 
# elif choice == "Login":
#     st.subheader("Login Section")


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)
    print('config', config)

credentials = fetch_users_dict()


authenticator = stauth.Authenticate(
        credentials,
        # config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

# name, authentication_status, username = authenticator.login('Login', 'main')

# print('authentication_status', authentication_status, st.session_state)

# st.button("Sign Up")

def login():
    name, authentication_status, username = authenticator.login('Login', 'main')

def signup():
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            upsert_users_dict()
    except Exception as e:
        st.error(e)

# def forgotP():
#     try:
#         if authenticator.forgot_password('Forgot Password'):
#             st.success('Password instructions sent to email successfully')
#             #upsert_users_dict()
#     except Exception as e:
#         st.error(e)


def logout():
    authenticator.logout('Logout', 'main')


# authenticator.credentials['usernames']['sanchit 2'] = {'name': 'sanchit', 'password': '9a0dd19de6d0fd5d4e784f1e180e7bf4dbe46269f4435d054d524973df818416'}
# print('authenticator.credentials', authenticator.credentials)
# upsert_users_dict(authenticator.credentials)

page_names_to_funcs = {
        "Log In": login,
        "Sign Up": signup,
    }


if st.session_state["authentication_status"]:
    # st.session_state.sidebar_state = 'collapsed'
    # st.set_page_config(initial_sidebar_state="collapsed")
    # st.empty()
    # authenticator.logout('Logout', 'main')

    # st.sidebar.button("Logout", logout)

    # sidebarLoginList = st.empty()
    
    # with sidebarLoginList:
    #     selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    #     page_names_to_funcs[selected_page]()
    main.main(st.session_state["name"], cp, authenticator)

    # try:
    #     if authenticator.reset_password(username, 'Reset password'):
    #         st.success('Password modified successfully')
    # except Exception as e:
    #     st.error(e)

    #st.write(f'Welcome *{st.session_state["name"]}*')
    #st.title('Some content')
# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')

elif (st.session_state["authentication_status"] == None) or (st.session_state["authentication_status"] == False):
    
    ## TODO: Hash when signup

    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()

    if selected_page=="Log In":
        if st.session_state["authentication_status"] == False:
            st.error('Username/password is incorrect')
        else:
            st.warning('Please enter your username and password')

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{name}*')
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')


# username = st.sidebar.text_input("User Name")
# password = st.sidebar.text_input("Password",type='password')
# if st.sidebar.checkbox("Login"):
#     hashed_pswd = make_hashes(password)
#     print('hash password' , hashed_pswd)
#     result = login_user(username,hashed_pswd)
#     print('result',result)

    
#     if result:
#         st.success("Logged In as {}".format(username))  

#         ## TODO: Remove/Hide components

#         main.main(None, username)    
#     else:
#         st.warning("Incorrect Username/Password")
 
# elif choice == "SignUp":
#     st.subheader("Create New Account")
#     new_user = st.text_input("Username",key='1')
#     new_password = st.text_input("Password",type='password',key='2')
 
#     if st.button("Signup"):
#         add_user(new_user,make_hashes(new_password))
#         st.success("You have successfully created a valid Account")
#         st.info("Go to Login Menu to login")


# names = ["Sagar", "Nauman", "Bisma"]
# usernames = ["sagarc", "nauman", "bismaa"]

# credentials = {"usernames":{}}

# # load hashed passwords
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)
        
# for uname,name,pwd in zip(usernames,names,hashed_passwords):
#     user_dict = {"name": name, "password": pwd}
#     credentials["usernames"].update({uname: user_dict})
        

        ####### BREAK
# authenticator= stauth.Authenticate(credentials, "cookiename", "abcd1234")

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status == False:
#     st1.error("Username/password is incorrect")

# if authentication_status == None:
#     st1.warning("Please enter your username and password")

# if authentication_status:
#     main(authenticator,name)