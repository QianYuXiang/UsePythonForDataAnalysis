from ch02.main import records
from ch02.main import print

from pandas import *

frame = DataFrame(records)
print(frame)
print(frame['tz'][:10])