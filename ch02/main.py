import json
from utils import print0 as print

path = '/Users/qianyuxiang/pydata-book/ch02/usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(record) for record in open(path)]