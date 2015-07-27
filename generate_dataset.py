"""
Simple script to generate datasets from movielens dataset

__author__: vikasrtr

"""

import numpy as np
import pandas as pd
import scipy.sparse as spr

# load data
print('Loading Dataset')
movies = pd.read_csv('data/movies.csv')
tags = pd.read_csv('data/tags.csv')

del tags['timestamp']
del movies['title']
# del movies['movieId']

# since this is totally content based
del tags['userId']

# get all genres as tag list
print('computing tags')
mixed_genres = movies.genres.values
gens = set()
for g in mixed_genres:
    lst = g.split('|')
    gens.update(lst)

gens.remove('(no genres listed)')
all_gens = list()
all_gens.extend(gens)

# extract tags from tags
all_tags = tags.tag.unique().tolist()

# combine all tags
all_tags.extend(all_gens)
all_tags = list(set(all_tags))
all_tags.sort()

print('Creating movie vs tags matrix')

mat = np.zeros((movies.shape[0], len(all_tags)))

movies['id'] = range(movies.shape[0])
mov = movies.values

# update mat matrix from movie genres
for m in mov:
    gns = m[1].split('|')
    for gn in gns:
        if gn != '(no genres listed)':
            mat[m[2], all_tags.index(gn)] = 1

# update mat matrix from tags
comb = movies.merge(tags, how='left', on=['movieId'])
comb = comb.values
for m in comb:
    tg = m[3]
    try:
        x = all_tags.index(tg)
        mat[m[2], x] = 1
    except:
        x = 0

print('Done')
