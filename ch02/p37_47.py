import pandas as pd
from utils import print0 as print
from matplotlib import pyplot as plt
import numpy as np

path = '/Users/qianyuxiang/pydata-book/ch02/names/yob{}.txt'
names1880 = pd.read_csv(path.format(1880), names = ['name', 'sex', 'births'])

pieces = []
columns = ['name', 'sex', 'births']

for year in range(1880, 2011):
    path_tmp = path.format(year)
    frame = pd.read_csv(path_tmp, names = columns)
    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)

total_births = pd.pivot_table(names, values='births', index=['year'], columns=['sex'], aggfunc=sum)
#total_births.plot(title='Total birth by sex and year')

def add_prop(group):
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)

def get_top1000(group):
    return group.sort_values(by = 'births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = pd.pivot_table(top1000, values='births', index='year', columns=['name'], aggfunc=sum)
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
#subset.plot(subplots=True, figsize=(12, 10), grid=False, title='Number of births per year')

table = pd.pivot_table(top1000, values='prop', index='year', columns='sex', aggfunc=sum)
#table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))

df = boys[boys.year == 2010]
prop_cumsum = df.sort_values(by = 'prop', ascending=False).prop.cumsum()
#print(prop_cumsum[:10])
print(prop_cumsum.searchsorted(0.5)[0])

def get_quantile_count(group, q=0.5):
    group = group.sort_values(by = 'prop', ascending=False)
    return group.prop.cumsum().searchsorted(q)[0] + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

print(diversity.head(10))
#diversity.plot(title='Number of popular names in top 50%')

last_letters=names.name.map(lambda x:x[-1])
last_letters.name = 'last_letter'

table=pd.pivot_table(names, values='births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)
subtable=table.reindex(columns=[1910, 1960, 2010], level='year')

print(subtable.head(10))
print(subtable.sum())

letter_prop=subtable / subtable.sum().astype(float)
#fig, axes=plt.subplots(2, 1, figsize=(10, 8))
#letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
#letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female')

letter_prop2=table/table.sum()
dyn_ts=letter_prop2.ix[['d', 'n', 'y'], 'M'].T
#print(dyn_ts.head(10))
#dyn_ts.plot()

all_names=top1000.name.unique()
mask=np.array(['lesl' in x.lower() for x in all_names])
lesley_like=all_names[mask]
#print(lesley_like)

filtered=top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()

table=pd.pivot_table(filtered, values='births', index='year', columns='sex', aggfunc=sum)
table=table.div(table.sum(1), axis=0)
table.plot(style={'M': 'k-', 'F': 'k--'})

plt.show()