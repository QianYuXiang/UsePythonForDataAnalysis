from ch02.main import records
from ch02.main import print

from pandas import *
from matplotlib import pyplot as plt

import numpy as np

frame = DataFrame(records)
print(frame['tz'].value_counts()[:10])

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'

tz_counts = clean_tz.value_counts()

print(tz_counts[:10])
tz_counts[:10].plot(kind = 'barh', rot = 0)

cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
print(operating_system[:5])

by_tz_os = cframe.groupby(['tz', operating_system])
print(by_tz_os)
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])

indexer = agg_counts.sum(1).argsort()
print(indexer[:10])
count_subset = agg_counts.take(indexer)[-10:]
print(count_subset)
count_subset.plot(kind = 'barh', stacked = True)


normed_subset = count_subset.div(count_subset.sum(1), axis = 0)
normed_subset.plot(kind = 'barh', stacked = True)

plt.show()