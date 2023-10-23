    # Import relevant packages 
from snowflake.snowpark import Session
import matplotlib.pyplot as plt
import streamlit as st  
import pandas as pd
from streamlit.components.v1 import html
import streamlit.components.v1 as components
from streamlit_elements import elements, mui, html
from streamlit_modal import Modal
import codes.data_functions as data_functions

def dashboard2(name,cp):
    def firstHeader(url):
        st.markdown(f'<p style="font-size:20px;"><b>{url}</b></p>', unsafe_allow_html=True)   

    agg_data = data_functions.fetch_cust_score(name,cp)

    avgESG=round(agg_data[2])
    currScore=[round(agg_data[3]), round(agg_data[4]), round(agg_data[5])]

    cust_id=agg_data[0]
    stock_details = data_functions.fetch_stock_score(cust_id, cp)
    stock_details_table = []
    portfolio_companies=[['','No Company Selected']]

    for i in range(len(stock_details)):
        stock_details_table.append(stock_details[i][1:12])
        portfolio_companies.append(stock_details[i][0:2])

    portfolio_companies_df=pd.DataFrame (portfolio_companies,columns=['Ticker', 'Name'])
 
    stock_details_df = pd.DataFrame (stock_details_table, columns = ['Name', 'Environment Rating', 'Social Rating','Governance Rating','ESG Rating','Number of Stocks held','Current Stock Price', 'Allocation in Portfolio value','One year performance','Last month performance','Industry Benchmark'])

    stock_details_df['ESG vs Industry Benchmark']=0

    total_amount_spent = stock_details_df['Allocation in Portfolio value'].sum()
    stock_details_df['% of Portfolio'] = ''
    
    #4. GUI Elements 
    #4.1 GUI Elements header and info modal
    header, info = st.columns( [0.3, 0.7])
    with header:
        firstHeader("Portfolio Analysis")
    with info:
        modal = Modal("ESG Ratings information", key='modal1' )
    
    
        infoCont = st.container()
        with infoCont:

            open_modal = st.button("ⓘ", key='info',type='primary',help='ESG Ratings Information')
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
                st.write("""
                The scores have been derived by a third party (ESG Book) basis external news articles, social feeds, company reports and other sources of information on each company's activities and outcomes in the Environmental, Social and Governance spheres.\n
                """)
                st.markdown('''
                0  -  50: &emsp; &emsp;  A **poor** score indicates that no best practices are being followed.\n
                51 -  60: &emsp;  An **average** score indicates that companies are not on track to meet the benchmarks.\n
                61 -  70: &emsp;  A **good** score signifies that a company is meeting best practices.\n
                71 - 100:   An **excellent** score indicates best practise are being followed.\n''')


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

    
    #4.2 GUI Elements Benchmark Tabs
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

    #4.3 GUI Elements Pie Chart and Bar Plot
    firstHeader('Overall and Category Breakdown')

    allC,top25=data_functions.fetch_benchmarks(cp)
    col1, col2 = st.columns( [0.15, 0.85])

    if st.session_state.selection=='NB':
        with col1:
            score=[avgESG,100-avgESG]

            # Create a pieplot
            fig1, ax1 = plt.subplots()

            ax1.pie(score,startangle=90, colors=['#83b87e','#cbcfd0'])

            scoreLabel = { 'size': 33,'family': 'arial'  }
            scoreFont={ 'size': 40,'weight':'heavy','family': 'Arial' }

            barLabel = { 'size': 13,'family': 'arial'  }

            # add a circle at the center to transform it in a donut chart
            ax1=plt.Circle( (0,0), 0.7, color='white')
            plt.text(-.23, -0.11,avgESG,fontdict=scoreFont)
            fig1.gca().add_artist(ax1)


            st.pyplot(fig1)
        
        with col2:    
            ESG_keywords = ["Environment", "Social", "Governance"]
            df = pd.DataFrame({"Your Portfolio": currScore}, index=ESG_keywords)

            x=df.plot.barh( xticks=[0,20,40,60,80,100],color={"Your Portfolio": '#9cc699'}, figsize=(7,1),width=0.75,label=currScore).figure
    
            plt.grid(axis = 'x',alpha=0.2)
            plt.axis(xmax=130,xmin=0)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().invert_yaxis()

            for i in range(len(currScore)):
                plt.text(currScore[i],i,currScore[i],va = 'center',fontsize=7)

            st.pyplot(x)
        
            


        print('stock_details1234', stock_details)


    else:


        with col1:
            st.markdown(f'<p style="font-size:6.5px;font-weight:bold">&nbsp;&nbsp;</p>', unsafe_allow_html=True)

            score=[avgESG,100-avgESG]
            selectedScore=[]
            score1=[allC[3],100-allC[3]]
            score2=[top25[3],100-top25[3]]

            if st.session_state.selection=='AC':
                selectedScore=score1

            elif st.session_state.selection=='TC':
                selectedScore=score2

            scoreLabel = { 'size': 88,'family': 'arial'  }
            barLabel = { 'size': 13,'family': 'arial'  }



            plt.figure(figsize=(11, 11))

            colors = ['#83b87e','#cbcfd0']
            labels_group = [round(score[0]),'']
            labels_subgroup = [round(selectedScore[0]),'']
            colors_subgroup = ['#FFCE53', '#cbcfd0']

            outside_donut =  plt.pie(score,startangle=90,radius=0.8, colors=colors,labels=labels_group, 
                                    labeldistance=0.78, wedgeprops=dict(width=0.4, edgecolor='w') , textprops={'fontsize': 50})

            inside_donut = plt.pie(selectedScore, colors=colors_subgroup, radius=0.6,startangle=90, labels=labels_subgroup,
                                labeldistance=0.69, wedgeprops=dict(linewidth=3, width=0.3, edgecolor='w'),
                                textprops={'fontsize': 50})

            centre_circle = plt.Circle((0, 0), 0.4, color='white', linewidth=0)

            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.axis('equal')
            plt.tight_layout()

            st.pyplot(fig)
        
        with col2:    
    
            st.markdown(f'<p style="font-size:1px;font-weight:bold">&nbsp;&nbsp;</p>', unsafe_allow_html=True)

            ESG_keywords = ["Environment", "Social", "Governance"]
            barLabel = { 'size': 12,'family': 'arial'  }
            prtfScore=currScore
            bmrkScore=[]
            allC,top25           
            bmrkScore1=[allC[0],allC[1],allC[2]]
            bmrkScore2=[top25[0],top25[1],top25[2]]

            if st.session_state.selection=='AC':
                bmrkScore=bmrkScore1

            elif st.session_state.selection=='TC':
                bmrkScore=bmrkScore2

            df1 = pd.DataFrame({"Your Portfolio": prtfScore}, index=ESG_keywords)
            df2 = pd.DataFrame({"Benchmark": bmrkScore}, index=ESG_keywords)

            df=pd.merge(df1,df2, left_index=True, right_index=True)

            x=df.plot.barh( xticks=[0,20,40,60,80,100],color={"Your Portfolio": '#9cc699',"Benchmark": '#FFCE53'}, figsize=(7,1),width=0.75,label=prtfScore).figure
            
            plt.grid(axis = 'x',alpha=0.2)
            plt.axis(xmax=150,xmin=0)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().invert_yaxis()

            for i in range(len(prtfScore)):
                plt.text(prtfScore[i]+0.3,i-(1/4.9),prtfScore[i],va = 'center',fontsize=6)
                plt.text(round(bmrkScore[i])+0.3,i+(1/4.9),round(bmrkScore[i]),va = 'center',fontsize=6)

            st.pyplot(x)
   
    ColBox1,ColBox2=st.columns([0.5,0.5])
    with ColBox1:        
        with elements("PortfolioValue"):
            with mui.Table(sx={'& .MuiTableCell-head': {"font-weight": '500'}, '& .MuiTableCell-root': {"text-align":'center'}}):
                mui.TableHead(mui.TableRow(mui.TableCell(children="Portfolio Value - Current"),mui.TableCell(children=" Average Portfolio Value - All Customers"),mui.TableCell(children=" Average Portfolio Value - Top 25% Customers")))
                mui.TableBody(mui.TableRow(mui.TableCell(children=str(round(total_amount_spent))+" USD"), mui.TableCell(children="8576 USD"),mui.TableCell(children="8962 USD")))
    

    for i in range(len(stock_details_df.index)):

        stock_details_df.loc[i,'Environment Rating']=str(round(float(stock_details_df.at[i,"Environment Rating"])))[:]
        stock_details_df.loc[i,'Social Rating']=str(round(float(stock_details_df.at[i,"Social Rating"])))[:]
        stock_details_df.loc[i,'Governance Rating']=str(round(float(stock_details_df.at[i,"Governance Rating"])))[:]
        stock_details_df.loc[i,'ESG Rating']=str(round(float(stock_details_df.at[i,"ESG Rating"])))[:]
        #stock_details_df.loc[i,'Current Stock Price']=str(round(stock_details_df.at[i,'Current Stock Price'].tolist(),2))+' USD'
        #stock_details_df.loc[i,'Current Stock Price']=str(round(stock_details_df.at[i,'Current Stock Price'].tolist(),2))+' USD'
        stock_details_df.loc[i,'Allocation in Portfolio value']=round(stock_details_df.at[i,'Allocation in Portfolio value'])
        stock_details_df.loc[i,'% of Portfolio']=str(round(((stock_details_df.at[i,'Allocation in Portfolio value'])/total_amount_spent)*100,1))+'%'
        stock_details_df.loc[i,'One year performance']=str(round(float(stock_details_df.at[i,"One year performance"]),2))[:]+'%'
        stock_details_df.loc[i,'Last month performance']=str(round(float(stock_details_df.at[i,"Last month performance"]),2))[:]+'%'
        stock_details_df.loc[i,'ESG vs Industry Benchmark']=str(round(float(stock_details_df.at[i,'ESG Rating'])-float(stock_details_df.at[i,'Industry Benchmark']),2))[:]

        if float(stock_details_df.loc[i,'ESG vs Industry Benchmark'])>0:
            stock_details_df.loc[i,'Industry Benchmark']=(str(round(float(stock_details_df.at[i,"Industry Benchmark"])))[:])+'⬇'
        elif float(stock_details_df.loc[i,'ESG vs Industry Benchmark'])<0:
            stock_details_df.loc[i,'Industry Benchmark']=str(round(float(stock_details_df.at[i,"Industry Benchmark"])))[:]+'⬆'
        else:
            stock_details_df.loc[i,'Industry Benchmark']=str(round(float(stock_details_df.at[i,"Industry Benchmark"])))[:]+'⬅'



    def smooth_user_preference(x):
        return str(round(float(x)))[:] + ' USD'


    stock_details_df['Current Stock Price'] = stock_details_df['Current Stock Price'].apply(smooth_user_preference)
    stock_details_df['Allocation in Portfolio value'] = stock_details_df['Allocation in Portfolio value'].apply(smooth_user_preference)


     # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                [data-testid="stTable"] > table tbody tr td {
                    border: none !important;
                    font-size:11px;
                }
                [data-testid="stTable"] > table th {
                    border: none !important;
                    font-size:12px;
                    color:#000000;
                    text-align: center !important;

                }
                    [data-testid="stTable"] > table {
                    border: none !important;
                    
                }
                thead tr {background-color:rgb(236, 233, 233); text-align: center !important}
                thead tr th:first-child {display:none}
                tbody th {display:none}


                tbody>thead tr>:nth-child(1),thead tr>:nth-child(2){ 
                    text-align: left !important;
                }

                tbody>tr>:nth-child(3){ 
                    /* color:#285c18; */
                    text-align: center !important;
                }


                tbody>tr>:nth-child(4){ 
                    /* color:#2e297e; */
                    text-align: center !important;
                }
                tbody>tr>:nth-child(5){ 
                    /* color:rgb(177,161,52); */
                    text-align: center !important;
                }
                tbody>tr>:nth-child(6){ 
                   /* color:#7e4729; */
                    text-align: center !important;
                }  
                tbody>tr>:nth-child(7),tr>:nth-child(8),tr>:nth-child(9),tr>:nth-child(10){ 
                    text-align: center !important;
                }  
                tbody>tr>:nth-child(11),tr>:nth-child(12),tr>:nth-child(13){ 
                    text-align: center !important;
                }  
                               
            
                </style>                """

    def color_negative_red(value):
            val=value.replace('%','')
            if float(val) < 0:
                color = 'red'
                return 'color: %s' % color
            elif float(val) > 0:
                color = 'green'
                return 'color: %s' % color

    def bmColor(val):
            if '⬇' in val: 
                color = 'green'
                return 'color: %s' % color
            elif '⬆' in val: 
                color = 'red' 
                return 'color: %s' % color

    st.write('\n')
    st.write('\n')
    #columns only for implementing modal
    Boxcol1, Boxcol2 = st.columns( [0.4, 0.6])

    with Boxcol1:
        firstHeader("Detailed View of Portfolio")

    with Boxcol2:
        modal = Modal("Detailed View of Portfolio", key='info_DPV' )
    
        infoCont = st.container()
        with infoCont:

            open_modal = st.button("ⓘ", key='info_DPV',type='primary',help='Detailed Portfolio View Information')
            infoB = """<style>
                .css-firdtp {
                    background-color: #ffffff;
                    color:black;
                    border:white;
                    margin:0px 0px 0rem;
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
  
                }
                </style>"""
            st.markdown(infoB, unsafe_allow_html=True)

        if open_modal:
            modal.open()

        if modal.is_open():
            with modal.container():
                st.write('''The Detailed View of Portfolio shows insights of your portfolio.''')
                st.write('''- The Environment, Social, Governance and ESG rating of each company is given by the dataset.''')
                st.write('''- ESG vs Industry Benchmark representates how the ESG Rating perfomce against the Industry. If the value is higher than zero, the company outperforms the associated industry.''')
                st.write('''- The Number of Stocks held multiplied with the Current Stock Price result in the Allocation in Portfolio value. ''')
                st.write('''- The One year and Last month performance is the difference between the today's share value and the value one year/month ago.''')
                st.write(''' ''')
                st.markdown('''''')

                html_string = '''

                <style>
                div[data-modal-container="true"][key="info_DPV"] {
                    position:absolute !important;
                    left: -200px !important;
                    top:-300px; !important;
                    width: 0px !important; 
                }
                </style>
                
                '''
                #components.html(html_string)
                st.markdown(html_string, unsafe_allow_html=True)

 
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    stock_details_df1=stock_details_df.loc[:,['Name', 'Environment Rating', 'Social Rating','Governance Rating','ESG Rating','Industry Benchmark','Number of Stocks held','Current Stock Price', 'Allocation in Portfolio value','% of Portfolio','One year performance','Last month performance']]

    s=stock_details_df1.style.applymap(color_negative_red, subset=['One year performance','Last month performance'])
    
    #st.table(s.applymap(bmColor, subset=['Industry Benchmark']))
    stock_details_df1["id"] = stock_details_df1.index + 1
    stock_details_df1.columns = ['Name', 'E Rating', 'S Rating','G Rating','ESG Rating','Industry Benchmark','Number of Stocks','Stock Price', 'Allocation in Portfolio value','% of Portfolio','One year performance','Last month performance','id']

    columns = [
    {"field": "Name", "headerName": "Name", "width": 180},
    {"field": "E Rating", "headerName": "E Rating", "width": 60},
    {"field": 'S Rating', "headerName": 'S Rating', "width": 60},
    {"field": 'G Rating', "headerName": 'G Rating', "width": 60},
    {"field": 'ESG Rating', "headerName": 'ESG Rating', "width": 70},
    {"field": 'Industry Benchmark', "headerName": 'Industry Benchmark', "width": 100},
    {"field": 'Number of Stocks', "headerName": 'Initial number of Stocks', "width": 110},
    {"field": 'Stock Price', "headerName": 'Stock Price', "width": 80},
    {"field": 'Allocation in Portfolio value', "headerName": 'Allocation in Portfolio value', "width": 110},
    {"field": '% of Portfolio', "headerName": '% of Portfolio', "width": 100},
    {"field": 'One year performance', "headerName": 'One year performance', "width": 110},
    {"field": 'Last month performance', "headerName": 'Last month performance', "width": 110},
    ]

    with elements("Table"):
        
        with mui.Box(sx={"height": 58*(len(stock_details_df1.index)+1),'& .MuiDataGrid-root': {"font-size": 12},"& .MuiDataGrid-columnHeaderTitle": {'overflow': "visible",
                                                                                                                                                       'lineHeight': "20px",
                                                                                                                                                       'whiteSpace': "normal","font-weight":700}}):
            mui.DataGrid(
                columns=columns,
                rows=stock_details_df1.to_dict(orient = "records"),
                pageSize=15,
                rowsPerPageOptions=[15],
                checkboxSelection=False,
            )
    
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

        
