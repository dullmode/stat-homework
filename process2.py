import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import *

df = pd.read_csv('output_data/result.csv')
price = df.loc[:, "price"]
dist_from_st = df.loc[:, "dist_from_st"]
pop = df.loc[:, "pop"]
fire_station_num = df.loc[:, "fire_station_num"]
crime_num = df.loc[:, "crime_num"]
tabacco_num = df.loc[:, "tabacco_num"]
restaurant_num = df.loc[:, "restaurant_num"]
historic_num = df.loc[:, "historic_num"]

equation_df=pd.concat([price,
                       pop,
                       dist_from_st,
                       fire_station_num,
                       crime_num,
                       tabacco_num,
                       restaurant_num,
                       historic_num
                       ], axis=1)

equation_df = equation_df.dropna()


price = pd.DataFrame(equation_df.price)
x_list = equation_df.drop("price",1)

model = sm.OLS(price, sm.add_constant(x_list))
result = model.fit()

with open('output_data/重回帰.csv', 'w') as fh:
    fh.write(result.summary().as_csv())

num_cols = model.exog.shape[1] 
vifs = [variance_inflation_factor(model.exog, i) for i in range(0, num_cols)]
pdv = pd.DataFrame(vifs, index=model.exog_names, columns=["VIF"])
pdv.to_csv('output_data/vif.csv')
