import pandas as pd

z = 'zip'

def fix_zip(series):
    return series.astype(str).str.extract('(\d+)', expand=False).str.zfill(5)

#loading all data
ta_df = pd.read_csv("input_data/tabacco.csv")
cr_df = pd.read_csv("input_data/crime.csv")
fs_df = pd.read_csv("input_data/fstation.csv")
pl_df = pd.read_csv("input_data/population.csv")
re_df = pd.read_csv("input_data/restaurant.csv")
hi_df = pd.read_csv("input_data/historic.csv")
ab_df = pd.read_csv('input_data/airbnb.csv')

#checking zip code
re_df[z] = fix_zip(re_df['Zip Code'])
ta_df[z] = fix_zip(ta_df['ZIP'])
fs_df[z] = fix_zip(fs_df['Zip'])
cr_df[z] = fix_zip(cr_df['zip'])
pl_df[z] = fix_zip(pl_df['zip'])
hi_df[z] = fix_zip(hi_df['zip'])
ab_df[z] = fix_zip(ab_df['zip'])

#totaling up by zip code, adding each column names to each columns
ta_df = ta_df[z].value_counts().rename_axis(z).reset_index(name="tabbaco_num")
cr_df = cr_df[z].value_counts().rename_axis(z).reset_index(name="crime_num")
fs_df = fs_df[z].value_counts().rename_axis(z).reset_index(name="greenhouse_num")
re_df = re_df[z].value_counts().rename_axis(z).reset_index(name="restaurant_num")
hi_df = hi_df[z].value_counts().rename_axis(z).reset_index(name="historic_num")

#delete km
ab_df['dist_from_st'] = ab_df['dist_from_st'].str.strip(' km')

#merging all input data
merged_df = pd.merge(pl_df, ta_df,  how='left')
merged_df = pd.merge(merged_df, cr_df,  how='left')
merged_df = pd.merge(merged_df, fs_df,  how='left')
merged_df = pd.merge(merged_df, hi_df,  how='left')
merged_df = pd.merge(merged_df, re_df,  how='left').fillna(0)

merged_df = pd.merge(ab_df, merged_df, how='left')
merged_df.to_csv('output_data/result.csv')
