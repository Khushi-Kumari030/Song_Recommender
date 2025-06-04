import pandas as pd
import numpy as np
import streamlit as st
import pickle 

with open('df.pkl','rb') as f:
    df=pickle.load(f)
with open('cosine_sim.pkl','rb') as g:
    cosine_sim=pickle.load(g)    

st.title('Instant Song Recommender 🎵')
song_list= sorted(df['song'].dropna().unique())
selected_song= st.selectbox('Select a song',song_list)

#recommendation function
def recommend_songs(song_name, cosine_sim=cosine_sim, df=df, top_n=5):
  #find the index of song
  idx=df[df['song'].str.lower()==song_name.lower()].index
  if len(idx)==0:
    return 'song not found in database'
  idx=idx[0]

  #get similarity score
  sim_scores=list(enumerate(cosine_sim[idx]))  #list like [indices, sim_score]=[2 0.55]

  #sort songs based on similarity score
  sim_scores=sorted(sim_scores,key=lambda x:x[1],reverse=True)
  sim_scores=sim_scores[1:top_n+1]  #not recommending same song

  #get song indices
  song_indices=[i[0] for i in sim_scores]

  #return top n songs
  return df[['artist','song']].iloc[song_indices]




if st.button('Recommend'):
  with st.spinner('finding similar songs...'):
    recommendations= recommend_songs(selected_song)
    if recommendations is None:
      st.warning('sorry, song not found')
    else:
      st.success('recommendations:')
      st.table(recommendations)