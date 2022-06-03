# **stat-homework**

### **関連のありそうなデータを探す**

元のデータはあまり説明力の高い説明変数が無いようなので個人的に面白そうだと思ったデータを追加します。また、**便宜上ファイル名を変更しています。**

- [ニューヨーク地区別人口のデータ](https://worldpopulationreview.com/zips/new-york) →population.csv
- [Retail Food Stores](https://data.ny.gov/Economic-Development/Retail-Food-Stores/9a8c-vfzj) →restaurant.csv
- [NYPD Arrest Data (Year to Date)](https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc) →crime.csv
-[Active Tobacco Retail Dealer Licenses](https://data.cityofnewyork.us/Business/Active-Tobacco-Retail-Dealer-Licenses/adw8-wvxb) →tabacco.csv
-[National Register of Historic Places](https://data.ny.gov/Recreation/National-Register-of-Historic-Places/iisn-hnyv) → historic.csv
-[Fire Department Directory for New York State](https://data.ny.gov/Public-Safety/Fire-Department-Directory-for-New-York-State/qfsu-zcpv) →fstation.csv
-[Newyork stations](https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49) →station.csv


### **前処理1**

今回は市町村区よりも細かいzipコード別で分析したいので`airbnb.csv`, `historic.csv`などのzipコードがないデータに、緯度経度を使ってzipコードの列を生成します。

1. `airbnb.csv`の列`latitude`,`longitude`から列`zip`を生成
2. `historic.csv`の列`Latitude`,`Longitude`から列`zip`を生成
3. `crime.csv`の列`Latitude`,`Longitude`から列`zip`を生成(元データの10万行だと計算に時間がかかりすぎるので1万行をランダムサンプリング)

```
import pandas as pd
import numpy as np
from geopy import Nominatim, distance
from tqdm import tqdm


def get_zipcode(df, geolocator, lat_field, lon_field):
    location = geolocator.reverse((df[lat_field], df[lon_field]))
    if 'postcode' in location.raw['address']:
        return location.raw['address']['postcode']
    else:
        return np.nan

tqdm.pandas()
ab_df = pd.read_csv("input_data/airbnb.csv")
hi_df = pd.read_csv("input_data/historic.csv")
cr_df = pd.read_csv("input_data/crime.csv")
st_df = pd.read_csv("input_data/station.csv")
geolocator = Nominatim(user_agent='http')

#1
ab_df['zip'] = ab_df.progress_apply(
        get_zipcode,
        axis=1,
        geolocator=geolocator,
        lat_field='latitude',
        lon_field='longitude'
        )

ab_df.to_csv('input_data/airbnb.csv')

#2
hi_df['zip'] = hi_df.progress_apply(
        get_zipcode,
        axis=1,
        geolocator=geolocator,
        lat_field='Latitude',
        lon_field='Longitude'
        )

hi_df.to_csv('input_data/historic.csv')

#3
cr_df['zip'] = cr_df.progress_apply(
        get_zipcode,
        axis=1,
        geolocator=geolocator,
        lat_field='Latitude',
        lon_field='Longitude'
        )

hi_df.to_csv('input_data/crime.csv')
```

### 前処理2
1. `station.csv`と`airbnb.csv`の緯度経度から最寄りの駅までの距離を計算して列`dist_from_sta`に保存

```
def get_min_distance_from_station(df, distance, lat_field, lon_field):
    best_km = None
    for i in st_df['the_geom']:
        i = i.split()
        st_lon = i[1][1:]
        st_lat = i[2][:-2]
        km = distance.distance(
                (df[lat_field], df[lon_field]),
                (st_lat, st_lon)
                )
        if best_km is None or km < best_km:
            best_km = km
    return best_km

ab_df['dist_from_st'] = ab_df.progress_apply(
        get_min_distance_from_station,
        axis=1,
        distance=distance,
        lat_field='latitude',
        lon_field='longitude'
        )
ab_df.to_csv('input_data/airbnb.csv')
```
### 前処理3
ニューヨークに散らばる各施設をzipコード別でまとめます。
1. 読み込む
2. zipコードを関数`fix_zip()`で5桁に統一する
3. geopyを使ったときについたkmを削除する
4. 各施設をzipコード別に集計する
5. 全データを一つずつマージしてresult.csvにまとめる。

**結果**

[result.csv](https://github.com/dullmode/stat-homework/blob/master/output_data/result.csv)

```
import pandas as pd

z = 'zip'

def fix_zip(series):
    return series.astype(str).str.extract('(\d+)', expand=False).str.zfill(5)

#1
ta_df = pd.read_csv("input_data/tabacco.csv")
cr_df = pd.read_csv("input_data/crime.csv")
fs_df = pd.read_csv("input_data/fstation.csv")
pl_df = pd.read_csv("input_data/population.csv")
re_df = pd.read_csv("input_data/restaurant.csv")
hi_df = pd.read_csv("input_data/historic.csv")
ab_df = pd.read_csv('input_data/airbnb.csv')

#2
re_df[z] = fix_zip(re_df['Zip Code'])
fs_df[z] = fix_zip(fs_df['Zip Code'])
ta_df[z] = fix_zip(ta_df['ZIP'])
cr_df[z] = fix_zip(cr_df['zip'])
pl_df[z] = fix_zip(pl_df['zip'])
hi_df[z] = fix_zip(hi_df['zip'])
ab_df[z] = fix_zip(ab_df['zip'])

#3
ab_df['dist_from_st'] = ab_df['dist_from_st'].str.strip(' km')

#4
ta_df = ta_df[z].value_counts().rename_axis(z).reset_index(name="tabacco_num")
cr_df = cr_df[z].value_counts().rename_axis(z).reset_index(name="crime_num")
fs_df = fs_df[z].value_counts().rename_axis(z).reset_index(name="fire_station_num")
re_df = re_df[z].value_counts().rename_axis(z).reset_index(name="restaurant_num")
hi_df = hi_df[z].value_counts().rename_axis(z).reset_index(name="historic_num")

#5
merged_df = pd.merge(pl_df, ta_df,  how='left')
merged_df = pd.merge(merged_df, cr_df,  how='left')
merged_df = pd.merge(merged_df, fs_df,  how='left')
merged_df = pd.merge(merged_df, hi_df,  how='left')
merged_df = pd.merge(merged_df, re_df,  how='left').fillna(0)

merged_df = pd.merge(ab_df, merged_df, how='left')
merged_df.to_csv('output_data/result.csv')
```
### 相関係数を確認する

**結果**

- [相関係数](https://github.com/dullmode/stat-homework/blob/master/output_data/%E7%9B%B8%E9%96%A2%E4%BF%82%E6%95%B0.png)
- [散布図](https://github.com/dullmode/stat-homework/blob/master/output_data/%E6%95%A3%E5%B8%83%E5%9B%B3.png)

2行目を見るとニューヨークでは、人口とレストランの数に強い相関があります。他にもタバコショップや犯罪数に弱い相関があることから、人口が多いほど施設や犯罪数が多いと類推できます。(Vifが高い?)

1行目の価格の項目を見るとあまり相関がない項目が多いと感じました。

```
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
a.figure.savefig('output_data/相関係数.png')

b = sns.pairplot(equation_df)
b.savefig('output_data/散布図.png')
```
### 重回帰分析

**結果**

[重回帰.csv](https://github.com/dullmode/stat-homework/blob/master/output_data/%E9%87%8D%E5%9B%9E%E5%B8%B0.csv)

`Adj. R-squared`が0.037に下がってしまいました。目的変数が価格の時、zipコード毎の人口・犯罪数・駅からの距離・消防署の数・タバコショップの数・レストランの数・歴史的建築物の数などは説明変数として重要では無いことがわかりました。 

```
import numpy as np
import statsmodels.api as sm

equation_df = equation_df.dropna()

price = pd.DataFrame(equation_df.price)
x_list = equation_df.drop("price",1)

model = sm.OLS(price, sm.add_constant(x_list))
result = model.fit()

with open('output_data/重回帰.csv', 'w') as fh:
    fh.write(result.summary().as_csv())
```
### VIF

**結果**

[vif.csv](https://github.com/dullmode/stat-homework/blob/master/output_data/vif.csv)

`const`が11.617914203135623になってしまいました

```
from statsmodels.stats.outliers_influence import *
num_cols = model.exog.shape[1] 
print(num_cols) #説明変数の列数
vifs = [variance_inflation_factor(model.exog, i) for i in range(0, num_cols)]
pdv = pd.DataFrame(vifs, index=model.exog_names, columns=["VIF"])
print(pdv)
```

### 参照
* [geopy documentation](https://geopy.readthedocs.io/en/stable/)
* [Python(StatsModels) で重回帰分析を理解し、分析の精度を上げる方法](https://tanuhack.com/statsmodels-multiple-lra/)
* [newyork open data](https://data.ny.gov/)
* [Is there a way to format a zip code in pandas using leading 00s | stackoverflow](https://stackoverflow.com/questions/66236790/is-there-a-way-to-format-a-zip-code-in-pandas-using-leading-00s)
* [Nearest latitude and longitude points in python | stackoverflow](https://stackoverflow.com/questions/69988283/nearest-latitude-and-longitude-points-in-python)
* [pandasのapplyの進捗をtqdmで表示](https://blog.imind.jp/entry/2019/03/06/111152)
