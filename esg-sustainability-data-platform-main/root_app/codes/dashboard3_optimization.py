import pandas as pd
from pulp import LpMinimize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD

def recommend(portfolio_data, esg_target):
    """ 
    The aim of this function is to calculate the recommended number of stocks that would minimize the target function.

    Args:
        portfolio_data (pandas.Dataframe): A dataframe consisting of 1...n rows and at least the following columns:
            Number of Stocks: current Number of Stocks
            Stock Price: current price of a stock
            One year performance
            E Rating: E Rating of stock
            S Rating: S Rating of stock
            G Rating: G Rating of stock]
         
         esg_target (tuple): A tuple providing the desired overall e s and g rate


    Returns:
        recom_share (pandas.DataFrame): The input dataframe extended with the column "recomm_shares"

    Notes:

    """

    # Initialize the return value
    recom_share = portfolio_data.copy()
    # Initialize the model
    model = LpProblem(name="ESG portfolio opt", sense=LpMinimize)  
    # Initialize the decision variables as integer greater 0
    x = {i: LpVariable(name=f"x{i}", lowBound=0, cat='Integer') for i in range(0, len(portfolio_data.index))}
    x_abs = {i: LpVariable(name=f"x_abs{i}", lowBound=0, cat='Integer') for i in range(0, len(portfolio_data.index))}

    # Add performance constraint
    cur_perf = (portfolio_data['Number of Stocks']*(portfolio_data['One year performance'])).sum()
    rec_perf = lpSum(x[i] * (portfolio_data['One year performance'][i]) for i in range(0, len(portfolio_data.index)))
    
    model += (rec_perf >= cur_perf, "performance_can't_get_worse")
    
    # Add investment amount constraint
    cur_amount = (portfolio_data['Number of Stocks']*portfolio_data['Stock Price']).sum()
    rec_amount = lpSum(x[i] * portfolio_data['Stock Price'][i] for i in range(0, len(portfolio_data.index)))

    model += (rec_amount <= cur_amount*1.05, "invested_amount_max_plus_5%")
    model += (rec_amount >= cur_amount*0.95, "invested_amount_max_minus_5%")

    # Add ESG rating constraint
    r_e_rate = lpSum(x[i] * portfolio_data['Stock Price'][i]*portfolio_data['E Rating'][i] for i in range(0, len(portfolio_data.index)))
    r_e_rate2 = lpSum(x[i] * portfolio_data['Stock Price'][i] for i in range(0, len(portfolio_data.index)))

    r_s_rate = lpSum(x[i] * portfolio_data['Stock Price'][i]*portfolio_data['S Rating'][i] for i in range(0, len(portfolio_data.index)))
    r_s_rate2 = lpSum(x[i] * portfolio_data['Stock Price'][i] for i in range(0, len(portfolio_data.index)))

    r_g_rate = lpSum(x[i] * portfolio_data['Stock Price'][i]*portfolio_data['G Rating'][i] for i in range(0, len(portfolio_data.index)))
    r_g_rate2 = lpSum(x[i] * portfolio_data['Stock Price'][i] for i in range(0, len(portfolio_data.index)))
    
    model += (r_e_rate <= 1.05 * esg_target[0] * r_e_rate2,"E_rating_max_plus_5%")
    model += (r_s_rate <= 1.05 * esg_target[1] * r_s_rate2,"S_rating_max_plus_5%")
    model += (r_g_rate <= 1.05 * esg_target[2] * r_g_rate2,"G_rating_max_plus_5%")
    model += (r_e_rate >= 0.95 * esg_target[0] * r_e_rate2,"E_rating_max_minus_5%")
    model += (r_s_rate >= 0.95 * esg_target[1] * r_s_rate2,"S_rating_max_minus_5%")
    model += (r_g_rate >= 0.95 * esg_target[2] * r_g_rate2,"G_rating_max_minus_5%")

    # ABS constraint, see https://stackoverflow.com/questions/59233699/mathematical-operation-of-abs-in-objective-function-of-pulp
    for i in range(0, len(portfolio_data.index)):
        model += x_abs[i] >= portfolio_data['Number of Stocks'][i] - x[i]
        model += x_abs[i] >= - (portfolio_data['Number of Stocks'][i] - x[i])
    
    # Add target function
    model += lpSum(x_abs[i] for i in range(0, len(portfolio_data.index)))

    # Solve the problem
    status = model.solve(PULP_CBC_CMD(msg=False))
    
    # if no optimal solution could be found, return empty df
    if model.status != 1:
        # Pulp ignores constraints if infeasible
        # For doc of status see https://www.coin-or.org/PuLP/constants.html?highlight=infeasible#pulp.constants.LpStatusInfeasible      
        return pd.DataFrame()

    recom_share["Recommended Number of Stocks"] = list([x[i].varValue for i in range(0, len(recom_share.index))])
    return recom_share

