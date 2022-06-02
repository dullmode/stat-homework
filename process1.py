import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('output_data/result.csv')
price = df.loc[:, "price"]
dist_from_st = df.loc[:, "dist_from_st"]
pop = df.loc[:, "pop"]
ezpass_num = df.loc[:, "ezpass_num"]
farmer_num = df.loc[:, "farmer_num"]
greenhouse_num = df.loc[:, "greenhouse_num"]
restaurant_num = df.loc[:, "restaurant_num"]
historic_num = df.loc[:, "historic_num"]

equation_df=pd.concat([price,
                       pop,
                       dist_from_st,
                       ezpass_num,
                       farmer_num,
                       greenhouse_num,
                       restaurant_num,
                       historic_num
                       ], axis=1)

plt.figure(figsize=(12, 9))
a = sns.heatmap(equation_df.corr(), annot=True, cmap='Blues')
a.figure.savefig('output_data/test.png')

b = sns.pairplot(equation_df)
b.savefig('output_data/test2.png')
