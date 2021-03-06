# -*- coding: utf-8 -*-
"""Movie Recoedation Using Python And data analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fcvjvx4xjMitglj3HnBBE9aJ4XnGhl9z
"""

pip install Ipython

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from IPython.display import display

import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (16,5)
plt.style.use('fivethirtyeight')

data = pd.read_csv('movie_metadata2.csv')

data.head()

data.shape

data.info()

data = data.drop(['color','director_facebook_likes','actor_3_facebook_likes',
                  'actor_1_facebook_likes','cast_total_facebook_likes','actor_2_facebook_likes',
                  'facenumber_in_poster','content_rating',
                  'movie_imdb_link','aspect_ratio','plot_keywords'],
                 axis=1)

data.columns

data.info()

round(100*(data.isnull().sum()/len(data.index)),2)

data = data[~np.isnan(data['gross'])]
data = data[~np.isnan(data['budget'])]

data.isnull().sum()

data = data[data.isnull().sum(axis=1)<=2]
data.isnull().sum()

data['num_critic_for_reviews'].fillna(data['num_critic_for_reviews'].mean(),inplace = True)
data['duration'].fillna(data['duration'].mean(),inplace=True)

data['language'].fillna(data['language'].mode()[0],inplace=True)

data['actor_2_name'].fillna('Unknown Actor',inplace=True)
data['actor_3_name'].fillna('Unknown Actor',inplace=True)

data.isnull().sum()

data['budget'] = data['budget']/1000000
data['gross'] = data['gross']/1000000

data['Profit'] = data['gross'] - data['budget']

data[['Profit','movie_title']].sort_values(by='Profit',ascending=False).head(10)

print("Rows before Deleting: ",data.shape[0])

data.drop_duplicates(subset=None,keep='first',inplace=True)
print("Rows after deleting Duplicates",data.shape[0])

data[['Profit','movie_title']].sort_values(by='Profit',ascending=False).head(10)

data['language'].value_counts()

def language(x):
  if x=='English':
    return 'English'
  else:
    return 'Foreign'

data['language']= data['language'].apply(language)
data['language'].value_counts()

data['duration'].value_counts()

data.describe()

data.info()

def duration(x):
  if x <= 120:
    return 2
  else:
    return 1

data['duration']= data['duration'].apply(duration)
data['duration'].value_counts()

data['genres'].value_counts()

data['genres'].str.split('|')[0]

data['Moviegenres'] = data['genres'].str.split('|')
data['Genre1'] = data['Moviegenres'].apply(lambda x: x[0])

data['Genre2'] = data['Moviegenres'].apply(lambda x: x[1] if len(x) > 1 else x[0])
data['Genre3'] = data['Moviegenres'].apply(lambda x: x[2] if len(x) > 2 else x[0])
data['Genre4'] = data['Moviegenres'].apply(lambda x: x[3] if len(x) > 3 else x[0])

data[['genres','Genre1','Genre2','Genre3',"Genre4"]].head(5)

data['Social_Popularity'] = ((data['num_user_for_reviews']/data['num_voted_users'])*(data['movie_facebook_likes']))/1000000

x = data[['movie_title','Social_Popularity']].sort_values(by ='Social_Popularity',
                                                         ascending= False).head(10).reset_index()

print(x)

sns.barplot(x['movie_title'],x['Social_Popularity'],palette='magma')
plt.title('Top 10 Movies Popular on social media')
plt.xticks(rotation = 90,fontsize=14)
plt.show()

display(data[['Genre1','gross']].groupby(['Genre1']).agg(['max','mean','min']).style.background_gradient(cmap='Wistia'))

data[['Genre1','gross']].groupby(['Genre1']).agg(['max','mean','min']).plot(kind = 'line',
                                                                             color= ['red','black','blue'])
plt.title("Most bankable Genre")
plt.xticks(np.arange(17),['Action','Adventure','Animation',
                          'Biography',
                          'Comedy','Crime',
                          'Documentary','Drama',
                          'Family','Fantasy',
                          'Horror','Musical','Mystry','Romance',
                          'Sci-Fi','Thriller','Western'],rotation = 90,fontsize=15)
plt.ylabel('Gross',fontsize=15)
plt.xlabel(' ',)
plt.show()

print('The Most profitable movie from each genre\n')
display(data.loc[data.groupby(data['Genre1'])['Profit'].idxmax()][['Genre1',
                                                                    'movie_title',
                                                                    'gross']].style.background_gradient(cmap='copper'))

data['title_year'] = data['title_year'].astype('int')

print('Most Profitable Year in Boxoffice')
display(data[['title_year','language','Profit']].groupby(['language',
                                                          'title_year']).agg('sum').sort_values(by ='Profit',
                                                                                                ascending=False).head(10).style.background_gradient(cmap='Greens'))

sns.lineplot(data['title_year'],data['Profit'],hue = data['language'])
plt.title('Time Series for Box office Profit for English vs Foreign Movies',fontsize=20)
plt.xticks(fontsize=15)
plt.xlabel(' ')
plt.show()

print("Movies that made Huge Loss")
display(data[data['Profit'] < -2000][['movie_title',
                                      'language',
                                      'Profit']].style.background_gradient(cmap='Reds'))

display(data[data['duration'] == 2][['movie_title','duration','gross',
                                          'Profit']].sort_values(by='Profit',ascending =  False).head(5))
display(data[data['duration'] == 1][['movie_title','duration','gross',
                                           'Profit']].sort_values(by='Profit',ascending = False).head(5))

sns.barplot(data['duration'],data['gross'],hue= data['language'],palette='spring')
plt.title('Gross Comparision')
plt.show()

data.info()

print("Average  IMDB Score for Long duration movie: {0:.2f}".format(data[data['duration'] == 1]['imdb_score'].mean()))
print("Average  IMDB Score for Short duration movie: {0:.2f}".format(data[data['duration'] == 2]['imdb_score'].mean()))

print('\nHighest Rated Long duration Movie\n',
      data[data['duration'] == 1][['movie_title','imdb_score']].sort_values(by='imdb_score',ascending = False).head(5))
print('\nHighest Rated Short duration Movie\n',
      data[data['duration'] == 2][['movie_title','imdb_score']].sort_values(by='imdb_score',ascending = False).head(5))

sns.boxplot(data['imdb_score'],data['duration'],palette='copper')
plt.title("IMDB Rating vs Gross",fontsize=20)
plt.xticks(rotation = 90)
plt.show()

def query_actors(x):
  a = data[data['actor_1_name'] == x]
  b = data[data['actor_2_name'] == x]
  c = data[data['actor_3_name'] == x]
  x = a.append(b)
  y = x.append(c)

  y = y[['movie_title','budget','gross','title_year','genres','language','imdb_score']]
  return y

query_actors('Meryl Streep')

def actors_report(x):
  a = data[data['actor_1_name'] == x]
  b = data[data['actor_2_name'] == x]
  c = data[data['actor_3_name'] == x]
  x = a.append(b)
  y = x.append(c)
  print("Time:",y['title_year'].min(),y['title_year'].max())
  print('Max Gross : {0:.2f} Million'.format(y['gross'].max()))
  print('Average Gross : {0:.2f} Million'.format(y['gross'].mean()))
  print('Max Gross : {0:.2f} Million'.format(y['gross'].min()))
  print('Number of 100 Million Movies :',y[y['gross'] > 100].shape[0])
  print('Avg IMDB Score : {0:.2f}'.format(y['imdb_score'].mean()))
  print('Most Common Genres: \n',y['Genre1'].value_counts().head())  

actors_report('Hugh Jackman')

def critically_acclaimed_actors(m):
  a = data[data['actor_1_name'] == m]
  b = data[data['actor_2_name'] == m]
  c = data[data['actor_3_name'] == m]
  x = a.append(b)
  y = x.append(c)
  return y['num_critic_for_reviews'].sum().astype('int')

print('Number of Critics Reviews for Brad Pitt')
display(critically_acclaimed_actors('Brad Pitt'))

print('Number of Critics Reviews for Leonardo DiCaprio')
display(critically_acclaimed_actors('Leonardo DiCaprio'))

print('Number of Critics Reviews for Hugh Jackman')
display(critically_acclaimed_actors('Hugh Jackman'))

from ipywidgets import interact 
from ipywidgets import interact_manual

pd.set_option('max_rows',3000)

@interact 
def show_movies_more_than(column = 'imdb_score',score=9.0):
  x = data.loc[data[column] > score][['title_year','movie_title','director_name',
                                      'actor_1_name','actor_2_name','actor_3_name',
                                      'Profit','imdb_score']]
  x = x.sort_values(by='imdb_score',ascending= False)
  x = x.drop_duplicates(keep ='first')
  return x

pd.set_option('max_rows',3000)

@interact
def show_articles_more_than(column=['budget','gross'],x=1000):
  return data.loc[data[column] > x][['movie_title','duration','gross','Profit','imdb_score']]

def recommed_lang(x):
  y = data[['language','movie_title','imdb_score']][data['language'] == x]
  y = y.sort_values(by='imdb_score',ascending = False)
  return y.head(10)

recommed_lang('Foreign')

def recommed_movies_on_actors(x):
  a = data[['movie_title','imdb_score']][data['actor_1_name'] == x]
  b = data[['movie_title','imdb_score']][data['actor_2_name'] == x]
  c = data[['movie_title','imdb_score']][data['actor_3_name'] == x]
  x = a.append(b)
  y = x.append(c)
  a = a.sort_values(by='imdb_score',ascending = False)
  return a.head(20)

recommed_movies_on_actors('Tom Cruise')

from mlxtend.preprocessing import TransactionEncoder

x = data['genres'].str.split('|')
te = TransactionEncoder()
x = te.fit_transform(x)
x = pd.DataFrame(x,columns=te.columns_)

x.head()

genres = x.astype('int')
genres.head()

genres.insert(0,'movie_title',data['movie_title'])

genres.head()

genres = genres.set_index('movie_title')
genres.head()

def recommendation(gen):
  gen = genres[gen]
  similar_gen =  genres.corrwith(gen)
  similar_gen =  similar_gen.sort_values(ascending=False)
  similar_gen = similar_gen.iloc[1:]
  return similar_gen.head(3)

recommendation('Action')

x = genres.transpose()
x.head()

def recommendation_movie(movie):
  movie = x[movie +'\xa0']
  similar_movie =  x.corrwith(movie)
  similar_movie =  similar_movie.sort_values(ascending=False)
  similar_movie = similar_movie.iloc[1:]
  return similar_movie.head(15)

recommendation_movie('The Expendables')

