import pandas as pd

z = 'zip'

def fix_zip(series):
    return series.astype(str).str.extract('(\d+)', expand=False).str.zfill(5)

#loading all data
ez_df = pd.read_csv("input_data/ez_pass.csv")
fm_df = pd.read_csv("input_data/farmer.csv")
gh_df = pd.read_csv("input_data/greenhouse.csv")
pl_df = pd.read_csv("input_data/population.csv")
re_df = pd.read_csv("input_data/restaurant.csv")
hi_df = pd.read_csv("input_data/historic.csv")
ab_df = pd.read_csv('input_data/airbnb.csv')

#checking zip code
ez_df[z] = fix_zip(ez_df['Zip Code'])
fm_df[z] = fix_zip(fm_df['Zip'])
gh_df[z] = fix_zip(gh_df['Zip Code'])
re_df[z] = fix_zip(re_df['Zip Code'])
pl_df[z] = fix_zip(pl_df['zip'])
hi_df[z] = fix_zip(hi_df['zip'])
ab_df[z] = fix_zip(ab_df['zip'])

#totaling up by zip code, adding each column names to each columns
ez_df = ez_df[z].value_counts().rename_axis(z).reset_index(name="ezpass_num")
fm_df = fm_df[z].value_counts().rename_axis(z).reset_index(name="farmer_num")
gh_df = gh_df[z].value_counts().rename_axis(z).reset_index(name="greenhouse_num")
re_df = re_df[z].value_counts().rename_axis(z).reset_index(name="restaurant_num")
hi_df = hi_df[z].value_counts().rename_axis(z).reset_index(name="historic_place")

#merging all input data
merged_df = pd.merge(pl_df, ez_df,  how='left')
merged_df = pd.merge(merged_df, fm_df,  how='left')
merged_df = pd.merge(merged_df, gh_df,  how='left')
merged_df = pd.merge(merged_df, hi_df,  how='left')
merged_df = pd.merge(merged_df, re_df,  how='left').fillna(0)

merged_df = pd.merge(ab_df, merged_df, how='left')
merged_df.to_csv('output_data/result.csv')
