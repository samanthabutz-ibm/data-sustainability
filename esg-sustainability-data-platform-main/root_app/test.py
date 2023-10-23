
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import snowflake.connector

connection_paramter = snowflake.connector.connect(account = "se58322-fsesg",
                        user="Muhammad Nauman",
                        password="Muhammad23",
                        role="RL_ESG_OBJECTS_DEVELOPER",
                        warehouse="WH_ESG_SUSTAINABILITY",
                        ocsp_fail_open=False)
 
cp = connection_paramter.cursor()

def fetch_users_dict():
    try:
        cp.execute("select username, password from DL_ESG_DEV.ESG_CONFIGURATION.user_table")
        result = cp.fetchall()
        # print(result)
    except:
        return False


    res_dict = {'usernames': {}}

    for res in result:
        # print(res)
        res_dict['usernames'][res[0]] = {'name':res[0], 'password':res[1]}

    # print(res_dict)

    return res_dict


{'credentials': {'usernames': {'nauman': 
                    {'email': 'nauman@gmail.com', 'name': 'nauman', 
                    'password': '$2b$12$bGobrw13eICGwyPUhxCHfes0LFnQm6LfePxOLrnAJGtTBM5qL6i1O'}}
                }, 'cookie': {'expiry_days': 30, 'key': 'some_signature_key', 'name': 'some_cookie_name'}, 'preauthorized': {'emails': ['nauman@gmail.com']}}
    

fetch_users_dict()


# hashed_passwords = stauth.Hasher(['nauman']).generate()

# print(hashed_passwords)

