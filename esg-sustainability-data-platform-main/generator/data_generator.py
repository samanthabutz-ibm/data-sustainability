import pandas as pd, numpy as np
import random,requests
from bs4 import BeautifulSoup
from faker import Faker
import uuid

import math as m
from random import randrange


def get_customer_data(fake, n_names):
    cus_ids = []
    port_ids = []

    fnames=[]
    lnames=[]
    emails=[]
    genders=[]
    ages=[]

    # n_names=2000
    for n in range(n_names):
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        genders.append(gender)
        
        if gender == 'F':
            fn = fake.first_name_female()
        else:
            fn = fake.first_name_male()
            
        ln = fake.last_name()
        
        fnames.append(fn)
        lnames.append(ln)
        emails.append(f"{fn}.{ln}@{fake.domain_name()}")
        
        ages.append(randrange(18, 90))
        
        cus_ids.append(fake.uuid4())

        #     cus_ids.append(uuid.UUID())
        port_ids.append(fake.uuid4())
        
        
    variables=[cus_ids, fnames,lnames, emails, genders, ages, port_ids]

    df=pd.DataFrame(variables).transpose()

    df.columns=["CustomerId", "FirstName", "LastName", "Email", "Gender", "Age","PortfolioId"]

    # df["Customer Address"]=df["Customer Address"].str.replace("\n",",")

    return df


def get_portfolio_data(df, sample_size, epochs, stock_meta):

    sec_df_list = []

    for ep in range(epochs):
        portfolio_samples = np.random.choice(df['PortfolioId'].to_numpy(), sample_size)

        rec_ids = []
        port_ids = []
        tickers = []
        buy_dates = []
        buy_values = []
        num_shares = []
        currs = []
        owned = []
        advisors = []

        curr_choices = ['USD', 'JPY', 'EUR']

        for n in portfolio_samples:
            
            buy_date_tmp = fake.date_between(start_date='-10y', end_date='today')
            
            buy_dates.append(buy_date_tmp)
            
            start_date = buy_date_tmp
            end_date = datetime.strptime('16/12/2022', "%d/%m/%Y")
            
            delta = relativedelta.relativedelta(end_date, start_date)
            # print(delta)
            months_owned = delta.years*12 + delta.months + delta.days/30
            
            owned.append(months_owned)
            
            rec_ids.append(fake.uuid4())
            tickers.append(np.random.choice(stock_meta))
            
            
            va = randrange(100, 300)
            buy_values.append(va)
            
            num_shares.append(m.floor(va/20))
            currs.append(np.random.choice(curr_choices))
            
            
            #     cus_ids.append(uuid.UUID())
            port_ids.append(fake.uuid4())
            
            advisors.append(fake.uuid4())
            
            
        # variables=[names,address,company,claim_reasons,claim_confidentiality_levels]
        variables = [rec_ids, list(portfolio_samples), tickers, buy_dates, buy_values, num_shares, currs, owned, advisors]

        df_port = pd.DataFrame(variables).transpose()

        df_port.columns=["RecordId", "PortfolioId", "Ticker", "BuyDate", "BuyValue", "Number of Shares","Currency", "Months Owned", "AdvisorId"]
        # df["Customer Address"]=df["Customer Address"].str.replace("\n",",")

        # df_port.head()
        # df_port# .to_csv('res.csv')

    sec_df_list.append(df_port)
    final_port_data = pd.concat(sec_df_list).reset_index(drop=True)

    return final_port_data

if __name__ == '__main__':
    #initialize Faker
    fake=Faker()

    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    import random
    from dateutil import relativedelta
    from datetime import datetime

    stock_meta = pd.read_csv('symbols_valid_meta.csv')['Symbol'].to_numpy()

    

    rd = random.Random()
    rd.seed(0)

    customer_data = get_customer_data(fake, 1000)

    customer_data.to_csv('output/customer.csv')

    portfolio_samples = np.random.choice(customer_data['PortfolioId'].to_numpy(), 100)

    portfolio_data = get_portfolio_data(customer_data, 800, 5, stock_meta)

    portfolio_data.to_csv('output/portfolio.csv')
