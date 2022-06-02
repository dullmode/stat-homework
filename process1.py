import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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

plt.figure(figsize=(12, 9))
a = sns.heatmap(equation_df.corr(), annot=True, cmap='Blues')
a.figure.savefig('output_data/test.png')

b = sns.pairplot(equation_df)
b.savefig('output_data/test2.png')
