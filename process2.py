import numpy as np
import pandas as pd
import statsmodels.api as sm

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

print(result.summary())
print(result.pvalues)
