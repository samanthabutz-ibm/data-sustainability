
from snowflake.snowpark import Session


import streamlit as st  

import streamlit_scrollable_textbox as stx


from  connection.connection import connection_paramter,cp


def horLine():
    st.markdown('''<style>
        .horizontal {
        border-top: 2px solid gray;
        color: rgb(45, 88, 23);
        top:60%;
        }   
        </style><div class = "horizontal"></div>''', unsafe_allow_html=True)


def dashboard1(db2):




    horLine()


    #new_title = '<p style="font-size: 28px; color:#377a4d;">Welcome to your ESG Portfolio Rating!</p>'
    #st.markdown(new_title, unsafe_allow_html=True)

#     st.write('''
# Nowadays it is increasingly important to think about sustainable issues. Because only those who act sustainably and responsibly have a chance of surviving as a company in the market in the long term. The world and the people are changing to a more sustainable and responsible environment. In 2022 already 89% of the investors had adopted the ESG criteria in their investment decision.
# Let´s make a holistic assessment of your portfolio's ESG Impact and take ownership of your portfolio optimization with better informed investment decisions!
#     ''')


    st.markdown('<p style="font-size: 28px; color:#377a4d; text-align:center;">Impact Investing with a purpose</p>', unsafe_allow_html=True)

    st.write('''
Analysis has shown that sustainability generates better risk-adjusted 
performance. And there is an **increasing demand for sustainable 
investments**. Assets under management in Responsible investments 
have **more than tripled** in the last decade. It has also been observed 
that companies and institutions that act responsibly **also tend to 
perform better financially**. \n
This is because, in a large manner, they are **more aware of the risks** 
they are subject to, and by mitigating those, they **effectively run more 
stable, reliable and solid businesses** that others tend to trust and 
invest more in! The world and its people are changing to a more sustainable and 
responsible environment. \n
In 2022, 89% of investors had adopted the ESG criteria in their investment decision.
So, what are you waiting for? Would you want to understand the 
sustainability profile of your current portfolio and let us help you optimize 
it?
    ''')

    horLine()

    st.markdown('<p style="font-size:28px; color:#377a4d; text-align:center; ">Welcome to your ESG Portfolio rating</p>', unsafe_allow_html=True)
    


    st.text('\n')     
    st.text('\n')  
    
    understandESG = '<p style="font-size: 22px; font-family: Verdana;color:#377a4d;vertical-align: bottom;">Understanding ESG</p>'
    st.markdown(understandESG, unsafe_allow_html=True)
  
    st.text("") 


    envText='''Environmental issues may include corporate climate policies, energy use, waste, pollution, natural resource conservation, and treatment of animals. ESG considerations can also help evaluate any environmental risks a company might face and how the company is managing those risks.'''

    sclText='''Social aspects look at the company\'s relationships with internal and external stakeholders.
Does it hold suppliers to its own ESG standards? Do workplace conditions reflect a high regard for employees’ health and safety? Or does the company take unethical advantage of its customers?'''

    gvrnText='''Governance standards ensure a company uses accurate and transparent accounting methods, pursues integrity and diversity in selecting its leadership, and is accountable to shareholders.'''

    envBox = '<p style="font-size: 20px;outline-style: solid;outline-width:thin;outline-color:rgb(221,221,221);color:#377a4d;">&nbsp; Environment  ☁️</p>'
    st.markdown(envBox, unsafe_allow_html=True)

    stx.scrollableTextbox(envText, height=80, key='env')

    st.text('\n')
    #st.text('\n')    

    socBox = '<p style="font-size: 20px;outline-style: solid;outline-width:thin;outline-color:rgb(221,221,221);color:#377a4d;">&nbsp; Social  🤝</p>'
    st.markdown(socBox, unsafe_allow_html=True)

    stx.scrollableTextbox(sclText, height=80, key='scl')

    st.text('\n')  
    #st.text('\n')  

    govBox = '<p style="font-size: 20px;outline-style: solid;outline-width:thin;outline-color:rgb(221,221,221);color:#377a4d;">&nbsp; Governance  ↔️</p>'
    st.markdown(govBox, unsafe_allow_html=True)

    stx.scrollableTextbox(gvrnText, height=80, key='gvrn')


    # colBtn1, colBtn2= st.columns( [0.9,0.1])

 

    # with colBtn1:
    #     pass
    # with colBtn2:
    s = """<style>
            .css-1x8cf1d {
                background-color: #578a00;
                color:#ffffff;
                float: right;
            }
            .css-1x8cf1d:hover {
                color:#f0f0f0;
                border-color:#467a43;
                background-color:#487002;
                }
            </style>"""
    st.markdown(s, unsafe_allow_html=True)
    st.button("Start", key="startButton", on_click=db2)








