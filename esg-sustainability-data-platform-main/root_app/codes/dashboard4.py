from snowflake.snowpark import Session

import streamlit as st  
from streamlit_searchbox import st_searchbox
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import codes.data_functions as data_functions
from  connection.connection import connection_paramter,cp

def get_ticker_from_name(name_ticker_df, company_name):
    try:
        return name_ticker_df[name_ticker_df["Name"] == company_name]["Ticker"].iloc[0]
    except Exception as e:
        print(f"Exception: {e}")
        return ""





def dashboard4(restart):

    CURR_DATE='2023-01-10'
    #month_start=replace(CURR_DATE,8,2,'01')
    def firstHeader(url):
        st.markdown(f'<p style="font-size:20px;"><b>{url}</b></p>', unsafe_allow_html=True)
    firstHeader('Company Insights')



    st.markdown('''<style>
        .horizontal {
        border-top: 1px solid gray;
        color: rgb(45, 88, 23);
        top:60%;
        }   
        </style><div class = "horizontal">&nbsp;</div>''', unsafe_allow_html=True)
        
    companylist=data_functions.fetch_all_comps(cp)

    all_companies=[['','No Company Selected']]
    company_names=[]
    for i in range(len(companylist)):
        all_companies.append(companylist[i][0:2])
        company_names.append(companylist[i][1])
    
    companylist_df = pd.DataFrame (all_companies, columns = ['Ticker', 'Name'])


    if (st.session_state.cmp_index==-1):
        for i in range(len(companylist_df.index)):
            if st.session_state.sTicker==companylist_df.loc[i,'Ticker']:
                st.session_state.cmp_index=i
                break
            st.session_state.cmp_index=0

    colA, colB = st.columns([0.15,0.85])
    with colA:
        st.markdown(f'''<p> <b>Selected Company: </b> </p>''', unsafe_allow_html=True)
    with colB:
        selected=st.selectbox("",companylist_df['Name'],index=st.session_state.cmp_index,label_visibility='collapsed',key='sCbox')


    if "sCbox" in st.session_state:
        st.session_state.sTicker = get_ticker_from_name(
            companylist_df, st.session_state.sCbox
        )

    if selected=='No Company Selected':
        comp_text= 'None. Please select from a drop down list above'
    else:
        comp_text=selected

    st.markdown('''<style>
        .horizontal {
        border-top: 1px solid gray;
        color: rgb(45, 88, 23);
        top:60%;
        }   
        </style><div class = "horizontal">&nbsp;</div>''', unsafe_allow_html=True)
    st.write('\n')


    if (st.session_state.sTicker==''):
        st.markdown(f'<p style="font-size: 20px;color:#377a4d; text-align:center;">&nbsp;<i> Please select a company for Overview and Insights</i></p>', unsafe_allow_html=True)
    

    else:



        #Hardcoded as of now
        indx='SNP'

        #selected_ticker=st.session_state.sTicker
        #company_data=fetch_cmp_data(selected_ticker,cp)
        #company_history=fetch_history_data(selected_ticker,cp)


        company_data=data_functions.fetch_cmp_data(st.session_state.sTicker,cp)
        company_history=data_functions.fetch_history_data(st.session_state.sTicker,cp)

        stock_current_value,company_history1=data_functions.fetch_history_data1(st.session_state.sTicker,CURR_DATE,cp)

        company_history_table=[]
        for i in range(len(company_history1)):
            company_history_table.append(company_history1[i][2:4])
        company_history_df=pd.DataFrame(company_history_table, columns=['month','price'])

        #index_score=[53,62,66,59]
        index_score=data_functions.fetch_index_score(cp)


        cmpD1,cmpD2, cmpD4 = st.columns( [0.21,0.32, 0.47])

        with cmpD1:
            
            st.markdown(f'<p style="font-size:14px;"> <b>General Information<br></p>', unsafe_allow_html=True)
            st.markdown(f'''<p style="font-size:11px;"> <b>Industry:</b> &emsp; {company_data[1]} <br>
            <b>Country:</b> &emsp; {company_data[2]} <br>
            <b>Index:</b> &emsp;&emsp; {indx} <br>
            <b>ESG:</b>{''} <br>
            </p>''', unsafe_allow_html=True)
      
            avgESG=round(company_data[6])
            score=[avgESG,100-avgESG]

            # Create a pieplot
            fig1, ax1 = plt.subplots(figsize=(1,1))

            ax1.pie(score,startangle=90, colors=['#83b87e','#cbcfd0'])

            scoreLabel = { 'size': 5, 'family': 'Arial' }
            scoreFont={ 'size': 12,'family': 'Arial' }

            barLabel = { 'size': 13,'family': 'arial'  }

            # add a circle at the center to transform it in a donut chart
            ax1=plt.Circle( (0,0), 0.7, color='white')
            plt.text(-.29, -0.14,avgESG,fontdict=scoreFont)
            fig1.gca().add_artist(ax1)

            st.pyplot(fig1)



        with cmpD2:
            st.markdown(f'<p style="font-size:14px;"> <b>ESG Benchmark: ESG vs Industry / Index <br></p>', unsafe_allow_html=True)

            ESGBMark=[company_data[3:7],company_data[7:11],index_score]
            ESGBMark=[list(x) for x in zip(*ESGBMark)]        
            ESGBMarkdf=pd.DataFrame(ESGBMark,columns=['Company','Industry','Index'])


            fig, ax = plt.subplots(figsize=(6,5.5))

            ESGBMarkdf.plot.bar(ax=ax, yticks=[0,20,40,60,80,100],
                                color={'Company': '#849ff6','Industry':'#616160','Index':'#d9dadb'})

            xTicks=['E','S','G','ESG']
            ax.set_xticks(range(0,len(xTicks)))
            ax.set_xticklabels(xTicks, rotation = 'horizontal') 

            ax.grid(axis='y',alpha=0.3,linestyle='--')
            ax.set_ylim(ymax=130,ymin=0)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)

  

            # Add data labels
            for i, bar in enumerate(ax.containers):
                j = 0
                for rect in bar:

                    height = rect.get_height()
                    value = round(ESGBMarkdf.iloc[j][i])
                    ax.text(rect.get_x() + rect.get_width() / 2, height + 2,
                            f'{value}', ha='center', va='bottom')
                    j = j+1

            ax.legend(loc="upper center", ncol=len(ESGBMarkdf.columns))

            st.pyplot(fig)
        

        with cmpD4:
            st.markdown(f'<p style="font-size:14px;"> <b>Financial Snapshot 1Y <br></p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:12px; text-align:center;"> <b>Current Price:</b> ${round(stock_current_value[0],2)}</p>', unsafe_allow_html=True)


            graphColor='#028e1e'
            fig, x = plt.subplots()
            fig = plt.figure(figsize=(7,3.8))
            x=plt.plot(company_history_df['price'],'-o',markersize=8,markerfacecolor='white',color=graphColor,linewidth=2)
            plt.axis([-0.2,(len(company_history_df.index)-0.8) , 0, (max(company_history_df['price'])+15)])
            plt.fill_between(range(len(company_history_df.index)), company_history_df['price'], color=graphColor, alpha=0.4)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.xticks(np.array(range(0, len(company_history_df.index))),company_history_df['month'],fontsize=8)  
            plt.grid(axis = 'y',alpha=0.6,linestyle='--')

            st.pyplot(fig)



        st.write('\n')
        st.markdown('\n')
        
        st.markdown('''<style>
                .horizontal {
                border-top: 1px solid gray;
                color: rgb(45, 88, 23);
                top:60%;
                }   
                </style><div class = "horizontal">&nbsp;</div>''', unsafe_allow_html=True)

        st.markdown(f'<p style="font-size:14px;"> <b>Detailed ESG score per category<br></p>', unsafe_allow_html=True)

        
        companyInsights=data_functions.fetch_comp_insights(st.session_state.sTicker,cp)
        
        
        E_keywords = ["Environmental Solutions", "Water", "Resource Use", "Environmental Stewardship","Waste","Environmental Management","Emissions"]


        #E_Insights=[64,55,88,70,56,65,45]

        E_Insights=companyInsights[0:7]

        S_keywords =  ["Product Access","Community Relations","Product Quality and Safety","Training and Development","Occupational Health and Safety","Labour Rights","Human Rights","Employment Quality","Diversity","Compensation"]
        

        #S_Insights=[67,32,91,64,80,60,66,56,37,45] 

        
        S_Insights=companyInsights[7:17]

        G_keywords=["Forensic Accounting","Transparency","Corporate Governance","Capital Structure","Business Ethics"]

        #G_Insights=[60,66,56,37,45]

        G_Insights=companyInsights[17:22]   



        eInsights,L1, sInsights, L2, gInsights = st.columns([0.33,0.01,0.33, 0.01, 0.33])
        
        with eInsights:
            e_df = pd.DataFrame({"Environment": E_Insights}, index=E_keywords)

            x=e_df.plot.barh( xticks=[0,20,40,60,80,100],color={"Environment": '#9cc699'},label=E_Insights,  figsize=(3,6),width=0.75).figure
    
            #plt.title("Category:", x=-0.2,y=1,fontdict=barLabel)
            plt.grid(axis = 'x',alpha=0.2)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().invert_yaxis()
            plt.axis(ymin=-.5,ymax=7)

            for i in range(len(E_Insights)):
                plt.text(E_Insights[i],i,round(E_Insights[i]),va = 'center',fontsize=10)

            plt.legend(loc="upper center", ncol=len(E_Insights))

            st.pyplot(x)
        

        with sInsights:
            s_df = pd.DataFrame({"Social": S_Insights}, index=S_keywords)

            x=s_df.plot.barh( xticks=[0,20,40,60,80,100],color={"Social": '#f2e4b9'},label=S_Insights,  figsize=(3,6.23),width=0.75).figure
    
            #plt.title("Category:", x=-0.2,y=1,fontdict=barLabel)
            plt.grid(axis = 'x',alpha=0.2)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().invert_yaxis()
            plt.axis(ymin=-.5,ymax=10.5)

            for i in range(len(S_Insights)):
                plt.text(S_Insights[i],i,round(S_Insights[i]),va = 'center',fontsize=10)

            plt.legend(loc="upper center", ncol=len(S_Insights))

        
            st.pyplot(x)


        with gInsights:
            s_df = pd.DataFrame({"Governance": G_Insights}, index=G_keywords)

            x=s_df.plot.barh( xticks=[0,20,40,60,80,100],color={"Governance": '#bdc9e3'},label=G_Insights,  figsize=(3,5.4),width=0.75).figure
    
            #plt.title("Category:", x=-0.2,y=1,fontdict=barLabel)
            plt.grid(axis = 'x',alpha=0.2)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().invert_yaxis()
            plt.axis(ymin=-.5,ymax=5)

            for i in range(len(G_Insights)):
                plt.text(G_Insights[i],i,round(G_Insights[i]),va = 'center',fontsize=10)

            plt.legend(loc="upper center", ncol=len(G_Insights))

        
            st.pyplot(x)
        

    st.write('\n')
    st.markdown('''<style>
        .horizontal {
        border-top: 1px solid gray;
        color: rgb(45, 88, 23);
        top:60%;
        }   
        </style><div class = "horizontal">&nbsp;</div>''', unsafe_allow_html=True)
        
    
    
    
    s = """<style>
            .css-1x8cf1d {
                background-color: #578a00;
                color:#ffffff;
                float:right;
            }
            .css-1x8cf1d:hover {
                color:#f0f0f0;
                border-color:#467a43;
                background-color:#487002;
                }


                .css-5uatcg {
                background-color: #578a00;
                color:#ffffff;
                float:right;
            }
            .css-5uatcg:hover {
                color:#f0f0f0;
                border-color:#467a43;
                background-color:#487002;
                }
            </style>"""
            
    st.markdown(s, unsafe_allow_html=True)
    st.button("Back to Home", key="homeButtond4", on_click=restart)











