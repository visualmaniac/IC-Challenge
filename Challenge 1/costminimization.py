import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as sp

#get data
df = pd.read_csv('daten.csv', header=None)

#change type of first column to datetime and right format
df[0] = pd.to_datetime(df[0])
df[0] = df[0].dt.strftime("%d-%m-%Y")
df[0] = pd.to_datetime(df[0])

#change from string to numeric value
df[1] = df[1].str.replace(',', '.')
df[1] = pd.to_numeric(df[1])

#get prices
prices = pd.read_csv('preise.csv', header=None)
prices.iloc[:, 1:] = prices.iloc[:, 1:].applymap(lambda x: pd.to_numeric(x.replace(',', '.')))

#define objective function
def objective(param):
    
    param_year = param[0]
    param_quarter = param[1:5]
    param_months = param[5:17]
    penalty_months = prices[3]
    
    penalty_list = []

    #calculate dayly costs for whole year
    for day in range(366):
        
        #get demand of this day
        this_day, daily_demand = df[0][day], df[1][day]
        
        #get pricing today depending on quarter, month
        quarter = this_day.quarter - 1
        month = this_day.month - 1  # -1 for combatibility with list indexing
        
        #calculate penalty cost of this day
        demand_satisfied = param_year + param_quarter[quarter] + param_months[month]
        missing_demand = max(0, daily_demand - demand_satisfied)
        
        penalty_cost = missing_demand * penalty_months[month]
        
        #save penalty cost in list
        penalty_list.append(penalty_cost)
     
    #calculate total penalty cost and package cost
    total_penalty_cost = sum(penalty_list)
    cost_year = param_year
    cost_quarter = 0.425 * param_quarter[0] + 0.25 * param_quarter[1] + 0.25 * param_quarter[2] + 0.425 * param_quarter[3]
    cost_months = 0
    i = 0
    while i<12:
        cost_months += param_months[i]*prices[2][i]
        i += 1
    
    package_cost = cost_year + cost_quarter + cost_months
    
    total_cost = total_penalty_cost + package_cost
    return total_cost


#start optimization
initial_guess = [1]*17
bnds = tuple([(0, None)]*17)
result = sp.minimize(objective, initial_guess, bounds=bnds)

print(result)

print( "units_year = " + str(result.x[0]), "\n",
    "units_quarter = " + str(result.x[1:5]),"\n",
    "units_year = " + str(result.x[5:]))