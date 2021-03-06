from ch02.main import records
from utils import print0 as print

time_zones = [record['tz'] for record in records if 'tz' in record]

def get_counts(sequence):
    counts = {}
    for record in sequence:
        if record in counts:
            counts[record] += 1
        else:
            counts[record] = 1
    return counts

print(get_counts(time_zones))

def get_counts2(sequence):
    from collections import defaultdict
    counts = defaultdict(int)
    for record in sequence:
        counts[record] += 1
    return counts

print(get_counts2(time_zones))

def top_counts(count_dict, n = 10):
    pairs = [(tz, count) for tz, count in count_dict.items()]
    pairs.sort(key = lambda x: x[1])
    return pairs[-n : ]

print(top_counts(get_counts2(time_zones)))

from collections import Counter
counts = Counter(time_zones)
print(counts.most_common(10))