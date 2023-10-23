import numpy as np
from snowflake.snowpark import Session
import streamlit as st  
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from  connection.connection import connection_paramter,cp
from codes.dashboard3_optimization import recommend
from streamlit_modal import Modal
import codes.data_functions as data_functions
from streamlit_elements import elements, mui, html


def dashboard3(name, cp):

    def firstHeader(url):
        st.markdown(f'<p style="font-size:20px;"><b>{url}</b></p>', unsafe_allow_html=True)

    #1. Grab data and initialize variables
    agg_data = data_functions.fetch_cust_score(name,cp)
    avgESG=round(agg_data[2])
    allC,top25=data_functions.fetch_benchmarks(cp)
    currScore=[round(agg_data[3]), round(agg_data[4]), round(agg_data[5])]
    if "score" not in st.session_state:
                st.session_state.score = [currScore[0],currScore[1],currScore[2]]

    portfolio_data = data_functions.fetch_stock_score(agg_data[0], cp)
    portfolio_companies=[['','No Company Selected']]
    for i in range(len(portfolio_data)):
        portfolio_companies.append(portfolio_data[i][0:2])
    
    portfolio_companies_df=pd.DataFrame (portfolio_companies,columns=['Ticker', 'Name'])
    portfolio_data = pd.DataFrame(portfolio_data).iloc[:, 1:]
    portfolio_data.columns = ['Name', 'E Rating', 'S Rating','G Rating','ESG Rating','Number of Stocks','Stock Price', 'Allocation in Portfolio value','One year performance','Last month performance','ESG vs Industry Benchmark']
    portfolio_data = portfolio_data.astype({'E Rating':'float','S Rating':'float','G Rating':'float','ESG Rating':'float','Number of Stocks':'float','Stock Price':'float','Allocation in Portfolio value':'float','One year performance':'float','Last month performance':'float'})
    portfolio_data.drop(['Last month performance','ESG vs Industry Benchmark'], axis=1, inplace=True)

    #2. Calculate recommendation
    esg_target = (st.session_state.score[0],st.session_state.score[1],st.session_state.score[2])
    recom_shares = recommend(portfolio_data, esg_target)
    feasible_flag = True
    if recom_shares.empty:
        feasible_flag=False
        recom_shares = recommend(portfolio_data, (currScore[0],currScore[1],currScore[2]))
    
    #3. Create Target recommendation dataframe
    recom_shares.drop(['One year performance'], axis=1, inplace=True)
    recom_shares['Allocation in Portfolio value new'] = recom_shares['Recommended Number of Stocks']*recom_shares['Stock Price']
    total_amount_spent = recom_shares['Allocation in Portfolio value'].sum()
    total_amount_spent_new = recom_shares['Allocation in Portfolio value new'].sum()

    for i in range(len(recom_shares.index)):
        recom_shares.loc[i,'% of Portfolio']=str(round(((recom_shares.at[i,'Allocation in Portfolio value'])/total_amount_spent)*100,1))+'%'
        recom_shares.loc[i,'% of Portfolio new']=str(round(((recom_shares.at[i,'Allocation in Portfolio value new'])/total_amount_spent_new)*100,1))+'%'
    recom_shares['Change in Stocks'] = (recom_shares['Recommended Number of Stocks']-recom_shares['Number of Stocks'])
    recom_shares = recom_shares.round({'E Rating':0,'S Rating':0,'G Rating':0,'ESG Rating':0,'Number of Stocks':0,'Stock Price':0,'Allocation in Portfolio value':0,'Change in Stocks':0,'Recommended Number of Stocks':0})
    recom_shares[['E Rating', 'S Rating','G Rating','ESG Rating','Number of Stocks','Stock Price','Allocation in Portfolio value','Change in Stocks','Recommended Number of Stocks']] = recom_shares[['E Rating','S Rating','G Rating','ESG Rating','Number of Stocks','Stock Price', 'Allocation in Portfolio value','Change in Stocks','Recommended Number of Stocks']].astype(np.int64)
    #Change column order for display
    recom_shares = recom_shares[['Name','E Rating','S Rating','G Rating','ESG Rating','Stock Price','Number of Stocks','Recommended Number of Stocks','Allocation in Portfolio value','Allocation in Portfolio value new','% of Portfolio','% of Portfolio new', 'Change in Stocks']]
    #Calculate achieved E,S & G Score
    recom_E = (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']*recom_shares['E Rating']).sum() / (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']).sum()
    recom_S = (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']*recom_shares['S Rating']).sum() / (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']).sum()
    recom_G = (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']*recom_shares['G Rating']).sum() / (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']).sum()
    recom_ESG = (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']*recom_shares['ESG Rating']).sum() / (recom_shares['Recommended Number of Stocks'] * recom_shares['Stock Price']).sum()
    achievedScore = [recom_E,recom_S,recom_G,recom_ESG]
    
    
    #4. GUI Elements 
    #4.1 GUI Elements header and info modal
    header, info = st.columns( [0.3, 0.7])
    with header:
        firstHeader("Portfolio Optimization")
    with info:
        modal = Modal("ESG Portfolio Optimization", key='modal1' ) 
    
        infoCont = st.container()
        with infoCont:

            open_modal = st.button("ⓘ", key='info',type='primary',help='ESG Portfolio Optimization')
            infoB = """<style>
                .css-firdtp {
                    background-color: #ffffff;
                    color:black;
                    border:white;
                    margin:0px 0px 0rem;
                    margin-top:8px;
                    font-size=1px;
                }
                .css-1aqmucy {
                    float: right;
                }
                .css-firdtp:hover {
                    color:gray;
                    background-color:white;
                    border:white;
                    }




                .css-15hz85m {
                    float: right;
                }
                .css-10rzsyr {
                    background-color: RGB(14,17,22);
                    color:white;
                    border:white;
                    height: 40px;
                    margin-top: -3px !important;
                    margin:0px 0px 0rem;
                    font-size=30px;
                }

                .css-10rzsyr:hover {
                    color:gray;
                    background-color:RGB(14,17,22);
                    border:white;
                    margin-top: -3px;
                }

                
                </style>"""
            st.markdown(infoB, unsafe_allow_html=True)


        if open_modal:
            modal.open()

        if modal.is_open():
            with modal.container():
                st.write('''The purpose of the ESG optimiser is to increase the E, S, and G rating of your portfolio to a level specified by you.  You can select a benchmark to get a better feeling for what a good E, S, and G rating is and how your own portfolio compares. Use the “desired score” boxes to input your goal.''')
                st.write('''The optimizer tries to match the rating indicated by you with a precision of 5%, while trying to minimize the reallocation required to do so:''')
                st.write('''- Keeping the total amount invested stable (± 5%)''')
                st.write('''- Ensuring that the performance of your portfolio with the new stock allocation is not worse compared to the performance of your portfolio over the past year''')
                st.write('''Some solutions might not be feasible with your current portfolio composition, in which case the optimizer will let you know that your desired solution is not feasible.''')
                st.write(''' ''')
                st.markdown('''The result of the optimizer is for informational purposes only and depends on the inputs provided by you. You should not construe any such information or other material as legal, tax, investment, financial, or other advice. Any and all rebalancing of your portfolio should be discussed and implemented together with you broker. Contact your financial advisor here.''')


                html_string = '''

                <style>
                div[data-modal-container="true"][key="modal1"] {
                    position:absolute !important;
                    left: -200px !important;
                    width: 0px !important; 
                }
                </style>
                
                '''
                #components.html(html_string)
                st.markdown(html_string, unsafe_allow_html=True)
    
    #4.2 GUI Elements Infotext and ESG input fields
    descr, scoreInput = st.columns( [0.57, 0.43])
    with descr:
        with elements("header"):
            mui.Typography("Enter your target environment, social and governance score below. Your proposed portfolio composition will be adjusted automatically. For more information on the optimization see “i”.")
    with scoreInput:
        with elements("scores"):
            
            def handle_E_score(event, value):
                st.session_state.score[0] = float(event.target.value)

            def handle_S_score(event, value):
                st.session_state.score[1] = float(event.target.value)

            def handle_G_score(event, value):
                st.session_state.score[2] = float(event.target.value)

            with mui.Box(component="form", sx={'& .MuiTextField-root': { 'm': 1, 'width': '15ch', "background": "#ecf2eb"}}):
                mui.TextField(id="E",label="E Rating",variant="outlined",defaultValue=currScore[0],type="number",onChange=handle_E_score,
                                InputProps={"startAdornment": mui.InputAdornment(position="start", children=mui.icon.Spa)})
                mui.TextField(id="S",label="S Rating",variant="outlined",defaultValue=currScore[1],type="number",onChange=handle_S_score,
                                InputProps={"startAdornment": mui.InputAdornment(position="start", children=mui.icon.Handshake)})
                mui.TextField(id="G",label="G Rating",variant="outlined",defaultValue=currScore[2],type="number",onChange=handle_G_score,
                                InputProps={"startAdornment": mui.InputAdornment(position="start", children=mui.icon.AssuredWorkload)})
            if not feasible_flag:
                mui.Typography("No reallocation - The desired ESG rates are infeasible")

    #4.3. GUI Elements Benchmark Tabs
    with elements("multiple_children"):
        if "selection" not in st.session_state:
            st.session_state.selection = "NB"

        def handle_change(event, value):
            st.session_state.selection = value

        with mui.Box(sx={"borderBottom": 1, "borderColor": 'divider',"backgroundColor":"#ecf2eb",
                        "& button:active":{"backgroundColor":"#9cc699"},
                        "& button.Mui-selected":{"color":"green"}}):
            with mui.Tabs(TabIndicatorProps={"sx":{"backgroundColor":"green"}},
                          value=st.session_state.selection,exclusive=True,onChange=handle_change,variant='fullWidth'
                          ):
                mui.Tab(value="NB",label="Standard")
                mui.Tab(value="AC",label="Benchmark All Customers")
                mui.Tab(value="TC",label="Benchmark Top 25% Customers")

    #4.4 GUI Elements Pie Chart and Bar Plot
    firstHeader('Overall and Category Breakdown')
    col0, col1 = st.columns( [0.15, 0.85])

    if st.session_state.selection=='NB':
        with col0: #Pie Chart
            score=[avgESG,100-avgESG]
            scoreAchieved=[achievedScore[3],100-achievedScore[3]]

            plt.figure(figsize=(2,2))
            
            #outer ring
            plt.pie(score,startangle=90,radius=0.8, colors=['#83b87e','#cbcfd0'],labels=[round(score[0]),''], 
                    labeldistance=0.78, wedgeprops=dict(width=0.4, edgecolor='w') , textprops={'fontsize': 8})
            #middle ring
            plt.pie(scoreAchieved, colors=['#3d85c6','#cbcfd0'], radius=0.6,startangle=90, labels=[round(scoreAchieved[0]),''],
                    labeldistance=0.69, wedgeprops=dict(linewidth=3, width=0.3, edgecolor='w'),
                    textprops={'fontsize': 8})

            #inner circle
            centre_circle = plt.Circle((0, 0), 0.4, color='white', linewidth=0)

            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.axis('equal')
            plt.tight_layout()

            st.pyplot(fig)

        with col1: # Bar Plot
            ESG_keywords = ["Environment", "Social", "Governance"]
            df1 = pd.DataFrame({"Your Portfolio": currScore}, index=ESG_keywords)
            df2 = pd.DataFrame({"Achieved": achievedScore[0:3]}, index=ESG_keywords)
            df=pd.merge(df1,df2, left_index=True, right_index=True)
            x=df.plot.barh( xticks=[0,20,40,60,80,100],color={"Your Portfolio": '#9cc699', "Achieved": '#3d85c6'}, figsize=(7,1),width=0.75,label=currScore).figure

            plt.grid(axis = 'x',alpha=0.2)
            plt.axis(xmax=130,xmin=0)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().invert_yaxis()
            plt.gcf().autofmt_xdate()
           

            for i in range(len(currScore)):
                plt.text(currScore[i]+0.3,i-(1/4.9),currScore[i],va = 'center',fontsize=6)
                plt.text(achievedScore[i]+0.3,i+(1/4.9),round(achievedScore[i]),va = 'center',fontsize=6)
            st.pyplot(x)
    else:
        with col0: #pie chart with Benchmark
            score=[avgESG,100-avgESG]
            selectedScore=[]
            score1=[allC[3],100-allC[3]]
            score2=[top25[3],100-top25[3]]
            scoreAchieved=[achievedScore[3],100-achievedScore[3]]

            if(st.session_state.selection)=='AC':
                selectedScore=score1

            elif(st.session_state.selection)=='TC':
                selectedScore=score2

            plt.figure(figsize=(2,2))
            
            #outer ring
            plt.pie(score,startangle=90,radius=0.8, colors=['#83b87e','#cbcfd0'],labels=[round(score[0]),''], 
                    labeldistance=0.78, wedgeprops=dict(width=0.4, edgecolor='w') , textprops={'fontsize': 8})
            #middle ring
            plt.pie(scoreAchieved, colors=['#3d85c6','#cbcfd0'], radius=0.6,startangle=90, labels=[round(scoreAchieved[0]),''],
                    labeldistance=0.69, wedgeprops=dict(linewidth=3, width=0.3, edgecolor='w'),
                    textprops={'fontsize': 8})
            #inner ring
            plt.pie(selectedScore, colors=['#FFCE53', '#cbcfd0'], radius=0.4,startangle=90, labels= [round(selectedScore[0]),''],
                    labeldistance=0.55, wedgeprops=dict(linewidth=3, width=0.3, edgecolor='w'),
                    textprops={'fontsize': 8})
            
            #inner circle
            centre_circle = plt.Circle((0, 0), 0.2, color='white', linewidth=0)

            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.axis('equal')
            plt.tight_layout()

            st.pyplot(fig)
            
        with col1: # Bar Plot with Benchmark
            ESG_keywords = ["Environment", "Social", "Governance"]

            bmrkScore=[]
            bmrkScore1=[allC[0],allC[1],allC[2]]
            bmrkScore2=[top25[0],top25[1],top25[2]]

            if(st.session_state.selection)=='AC':
                bmrkScore=bmrkScore1

            elif(st.session_state.selection)=='TC':
                bmrkScore=bmrkScore2

            df1 = pd.DataFrame({"Your Portfolio": currScore}, index=ESG_keywords)
            df2 = pd.DataFrame({"Achieved": achievedScore[0:3]}, index=ESG_keywords)
            df3 = pd.DataFrame({"Benchmark": bmrkScore}, index=ESG_keywords)
            df=pd.merge(df1,df2, left_index=True, right_index=True)
            df=pd.merge(df,df3, left_index=True, right_index=True)

            x=df.plot.barh( xticks=[0,20,40,60,80,100],color={"Your Portfolio": '#9cc699',"Benchmark": '#FFCE53', "Achieved": '#3d85c6'}, figsize=(7,1),width=0.75,label=currScore).figure
            
            plt.grid(axis = 'x',alpha=0.2)
            plt.axis(xmax=150,xmin=0)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().invert_yaxis()

            for i in range(len(currScore)):
                plt.text(currScore[i]+(3/10),i-(3/10),currScore[i],va = 'center',fontsize=5)
                plt.text(achievedScore[i]+(3/10),i,round(achievedScore[i]),va = 'center',fontsize=5)
                plt.text(bmrkScore[i]+(3/10),i+(3/10),round(bmrkScore[i]),va = 'center',fontsize=5)

            st.pyplot(x)


    #4.5 GUI Elements Key Figures
    ColBox1,ColBox2=st.columns([0.5,0.5])
    with ColBox1:
        #New Porftolio value
        cur_PortfolioValue = (recom_shares['Number of Stocks']*(recom_shares['Stock Price'])).sum()

        rec_PortfolioValue = (recom_shares['Recommended Number of Stocks']*(recom_shares['Stock Price'])).sum()

        change_PortfolioValue = rec_PortfolioValue - cur_PortfolioValue
        
        with elements("PortfolioValue"):
            with mui.Table(sx={'& .MuiTableCell-head': {"font-weight": '500'}, '& .MuiTableCell-root': {"text-align":'center'}}):
                mui.TableHead(mui.TableRow(mui.TableCell(children="Portfolio Value - Current"),mui.TableCell(children="Portfolio Value - New"),mui.TableCell(children="Portfolio Value - Change")))
                mui.TableBody(mui.TableRow(mui.TableCell(children=str(cur_PortfolioValue)+" USD"),mui.TableCell(children=str(rec_PortfolioValue)+" USD"),mui.TableCell(children=str(change_PortfolioValue)+" USD")))
    #summary number of shares to be bought and sold   
    with ColBox2:
        #calculation of sold and purchased Shares
        SellShares = 0
        BuyShares = 0
        for ind, row in recom_shares.iterrows():
            if row['Change in Stocks'] > 0:
                BuyShares = row['Change in Stocks'] + BuyShares

            elif row['Change in Stocks'] < 0:
                SellShares = row['Change in Stocks'] + SellShares

        changeTotalShares = (recom_shares['Recommended Number of Stocks'] - recom_shares['Number of Stocks']).sum()        
                   
        with elements("Stocks"):
            with mui.Table(sx={'& .MuiTableCell-head': {"font-weight": '500'}, '& .MuiTableCell-root': {"text-align":'center'}}):
                mui.TableHead(mui.TableRow(mui.TableCell(children="Number of Stocks - Buy"),mui.TableCell(children="Number of Stocks - Sell"),mui.TableCell(children="Number of Stocks - Change")))
                mui.TableBody(mui.TableRow(mui.TableCell(children=str(BuyShares)),mui.TableCell(children=str(SellShares)),mui.TableCell(children=str(changeTotalShares))))

    #4.6 GUI Element Table
    
    #coloring of values - Does not work
    def color_negative_red(value):
        val=value.replace('%','')
        if float(val) < 0:
            color = 'red'
            return 'color: %s' % color
        elif float(val) > 0:
            color = 'green'
            return 'color: %s' % color

    #representation of successful reallocation  
    def smooth_user_preference(x):
        return str(round(float(x)))[:] + ' USD'
    recom_shares['Stock Price'] = recom_shares['Stock Price'].apply(smooth_user_preference)
    recom_shares['Allocation in Portfolio value'] = recom_shares['Allocation in Portfolio value'].apply(smooth_user_preference)
    recom_shares['Allocation in Portfolio value new'] = recom_shares['Allocation in Portfolio value new'].apply(smooth_user_preference)
    recom_shares = recom_shares.astype(str)
    recom_shares["id"] = recom_shares.index + 1
    recom_shares = recom_shares[['id','Name','E Rating','S Rating','G Rating','ESG Rating','Stock Price','Number of Stocks','Recommended Number of Stocks','Allocation in Portfolio value','Allocation in Portfolio value new','% of Portfolio','% of Portfolio new', 'Change in Stocks']]
    #recom_shares=recom_shares.style.applymap(color_negative_red, subset=['Change in Stocks'])
    columns = [
    {"field": "Name", "headerName": "Name", "width": 180},
    {"field": "E Rating", "headerName": "E Rating", "width": 60},
    {"field": 'S Rating', "headerName": 'S Rating', "width": 60},
    {"field": 'G Rating', "headerName": 'G Rating', "width": 60},
    {"field": 'ESG Rating', "headerName": 'ESG Rating', "width": 60},
    {"field": 'Stock Price', "headerName": 'Stock Price', "width": 80},
    {"field": 'Allocation in Portfolio value', "headerName": 'Allocation in Portfolio value', "width": 110},
    {"field": 'Allocation in Portfolio value new', "headerName": 'Allocation in Portfolio value new', "width": 120},
    {"field": '% of Portfolio', "headerName": '% of Portfolio', "width": 100},
    {"field": 'Number of Stocks', "headerName": 'Initial number of Stocks', "width": 110},
    {"field": 'Change in Stocks', "headerName": 'Recommended Change', "width": 110}
]

    with elements("Table"):
        
        with mui.Box(sx={"height": 58*(len(recom_shares.index)+1),'& .MuiDataGrid-root': {"font-size": 12},"& .MuiDataGrid-columnHeaderTitle": {'overflow': "visible",
                                                                                                                                                       'lineHeight': "20px",
                                                                                                                                                       'whiteSpace': "normal","font-weight":700}}):
            mui.DataGrid(
                columns=columns,
                rows=recom_shares.to_dict(orient = "records"),
                pageSize=15,
                rowsPerPageOptions=[15],
                checkboxSelection=False,
            )
    #4.7 GUI Element Button and Select Box
    #Style the button
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
    #All changes regarding selectbox here



    compS=''

    btCol1,btCol2,btCol3=st.columns([0.4,0.38,0.22])
    with btCol1:
        pass
    with btCol2:
        compS = st.selectbox(' ',portfolio_companies_df['Name'], key='compBox', label_visibility='collapsed')
        for i in range(len(portfolio_companies_df.index)):
            if compS==portfolio_companies_df.at[i,'Name']:
                compS=str(portfolio_companies_df.at[i,'Ticker'])
                
            
    with btCol3:

        def setsTicker(compS):
            st.session_state.sTicker=compS
            st.session_state.cmp_index=-1
            st.session_state.page=4

        st.button("Go to Company Insights", key="CompIButton", on_click=setsTicker, args=(compS,))  
