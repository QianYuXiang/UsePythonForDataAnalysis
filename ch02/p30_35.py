import pandas as pd
from utils import print0 as print
import numpy as np

path = '/Users/qianyuxiang/pydata-book/ch02/movielens/{}'

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(path.format('users.dat'), sep = '::', header = None, names = unames, engine = 'python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(path.format('ratings.dat'), sep = '::', header = None, names = rnames, engine = 'python')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(path.format('movies.dat'), sep = '::', header = None, names = mnames, engine = 'python')

print(users[:5])
print(ratings[:5])
print(movies[:5])

data = pd.merge(pd.merge(users, ratings), movies)
print(data.ix[0])

mean_ratings = pd.DataFrame.pivot_table(data, values = 'rating', index = ['title'], columns = ['gender'], aggfunc = np.mean)
print(mean_ratings[:5])

ratings_by_title = data.groupby('title').size()
print(ratings_by_title[:10])

active_titles = ratings_by_title.index[ratings_by_title >= 250]
print(active_titles)

mean_ratings = mean_ratings.ix[active_titles]
print(mean_ratings)

print(mean_ratings.sort_index(by = 'F', ascending = False)[:10])

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_index(by='diff')
print(sorted_by_diff[:15])

print(sorted_by_diff[::-1][:15])

rating_std_by_title = data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.ix[active_titles]
print(rating_std_by_title.order(ascending = False)[:10])