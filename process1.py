import matplotlib.pyplot as plt
import scipy.stats
import seaborn as sns
import pandas as pd

df = pd.read_csv('output_data/result.csv')
price = df.loc[:, "price"]
pop = df.loc[:, "pop"]
ezpass_num = df.loc[:, "ezpass_num"]
farmer_num = df.loc[:, "farmer_num"]
greenhouse_num = df.loc[:, "greenhouse_num"]
restaurant_num = df.loc[:, "restaurant_num"]

equation_df=pd.concat([price,
                       pop,
                       ezpass_num,
                       farmer_num,
                       greenhouse_num,
                       restaurant_num,
                       ], axis=1)

#plt.figure(figsize=(12, 9))
a = sns.heatmap(equation_df.corr(), annot=True, cmap='Blues')
a.figure.savefig('output_data/test.png')
