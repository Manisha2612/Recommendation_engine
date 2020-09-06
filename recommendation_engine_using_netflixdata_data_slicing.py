#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import numpy as np
import math
import re
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")


# In[48]:


df = pd.read_csv('combined_data_1.txt', names = ["Cust_Id","Rating"],usecols = [0,1] ,nrows=2000)
tqdm.pandas()
df['Rating'] = df['Rating'].astype(float)
last_row_index=df.shape[0]
print(df)


# In[49]:



#view data

ax = sns.countplot(x="Rating", data=df)
plt.title('Data provided for each rating', fontsize=11)
total = float(len(df))
for p in ax.patches:
    percentage = '{:.1f}%'.format(100 * p.get_height()/total)
    x = p.get_x() + p.get_width()
    y = p.get_height()
    ax.annotate(percentage, (x, y),ha='center')
plt.show()


# In[50]:


customer_df = df[pd.notnull(df['Rating'])]
print(customer_df.shape)
print(df.shape)


# In[51]:


# adding moviesid column in customer_df
movie_np = np.array([])
# get movie count
movie_count = df.isnull().sum()[1]
print('total no of movies',movie_count)
#get all the movie id where Rating column value is none
df_nan = pd.DataFrame(pd.isnull(df.Rating))
df_nan = df_nan[df_nan['Rating'] == True]
df_nan = df_nan.reset_index()
movie_id_collection=df_nan['index'].to_numpy()
print('row containing movieid',movie_id_collection)


# In[52]:


mov_ar=df.loc[movie_id_collection].to_numpy()
mov_ar=np.delete(mov_ar,[1],1)
print(mov_ar)


# In[53]:


#replace values in movie_np with actual movie ID
start=0
end=0
for i in tqdm(range(len(movie_id_collection))):
    row_id=movie_id_collection[i]
    movie_id=mov_ar[i][0]
    movie_id=movie_id.strip(':')
    
    start=movie_id_collection[i]+1
    if i!=len(movie_id_collection)-1:
        end=movie_id_collection[i+1]-1
    else:
        end=last_row_index-1
    movie=np.array([movie_id]*(end-start+1))
    movie_np=np.append( movie_np , movie )


# In[54]:


print(movie_np.shape)
print(customer_df.shape)


# In[55]:


customer_df['Movies_Id']=movie_np.astype(int)


# In[56]:


#print(customer_df.head(50))


# In[57]:


#Data Slicing
cols = ['count','mean']

df_movie_data = customer_df.groupby('Movies_Id')['Rating'].agg(cols)
#print(df_movie_data)
movie_benchmark = round(df_movie_data['count'].quantile(0.75),0)
drop_movie_list = df_movie_data[df_movie_data['count'] < movie_benchmark].index

print('Movies with minimum review: {}'.format(movie_benchmark))

df_cust_data= customer_df.groupby('Cust_Id')['Rating'].agg(cols)
#print(df_cust_data)
df_cust_data.index = df_cust_data.index.map(int)
cust_benchmark = round(df_cust_data['count'].quantile(0.75),0)
drop_cust_list = df_cust_data[df_cust_data['count'] < cust_benchmark].index

print('Customers with minimum times of review: {}'.format(cust_benchmark))


# In[58]:


print('Original Shape: {}'.format(customer_df.shape))

customer_df = customer_df[~customer_df['Movies_Id'].isin(drop_movie_list)]
customer_df = customer_df[~customer_df['Cust_Id'].isin(drop_cust_list)]
print('After Trim Shape: {}'.format(customer_df.shape))
print(customer_df)


# In[ ]:





# In[ ]:





# In[ ]:




