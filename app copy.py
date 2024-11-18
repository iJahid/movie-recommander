import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stemme(text):
    l=[]
    if type(text)==str:
        d=text.split()
        for i in d:
            l.append(ps.stem(i))
    else:
        l.append(text)

    if(len(l)>1):
        return " ".join(l)
    else:
        return text

similarmovie=pickle.load(open('recommander.pkl','rb'))
tfidf_matrix=pickle.load(open('tfidf_matrix.pkl','rb'))
vectorizer=pickle.load(open('vectorizer.pkl','rb'))

API_KEY='538e4e8a58b198a88a2bd6bb065ab261'
poster_path='https://image.tmdb.org/t/p/w200/'
url='https://api.themoviedb.org/3/movie/'

def fetchPoster(movieid):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movieid,API_KEY))
    data=response.json()    
    return poster_path+data['poster_path']

st.title('Movie Search And Recomandation System ')
mv=pd.read_csv('movie_final.csv')

moviename=st.text_input('Moivie Name :', value="", max_chars=None, key='MovieName', type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible")



content=st.text_area("Search By Content:")
if content:
    query=content
    
    # query_vector = vectorizer.fit([query])
    query_vector = vectorizer.transform([stemme(query).lower()])
    
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    # Get indices of top N similar movies
    # similar_indices = similarities.argsort()[::-1][:5]
    threshold = 0.2 # Define a similarity threshold
    # sorted( similarities,reverse=True,key=lambda x:x[1])[0:6]
    similar_indices = [i for i, similarity in enumerate(similarities) if similarity > threshold and mv.iloc[i].vote_average>5.3]
    # similar_indices = similarities.argsort()[::-1]
    # Return the top N movies
    ccol1, ccol2, ccol3,ccol4 = st.columns(4,gap='small',vertical_alignment="top")
    ccount=0
    for i in similar_indices:
        # if(similarities[i]>0):
        # print(movies.iloc[i]["title"],movies.iloc[i].vote_average, similarities[i])
        
        c= mv.loc[i]
        poster=fetchPoster(c.id)
        strHeader=f'{c["title"]}  | ({c["vote_average"]})'
        # st.write(c.title,i[0])
        ccount=ccount+1

        if ccount>812:
            break

        if(ccount==1 or ccount==5  or ccount==9):
            
            with ccol1.container(height=250):
                st.write(strHeader)              
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
                
        if(ccount==2 or ccount==6 or ccount==10):
            with ccol2.container(height=250):
            
                st.write(strHeader) 
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
        if(ccount==3 or ccount==7 or ccount==11):
            with ccol3.container(height=250):
            
                st.write(strHeader) 
                    # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
        if(ccount==4 or ccount==8 or ccount==12):
            with ccol4.container(height=250):

                st.write(strHeader) 
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
     
        

# moviename=st.selectbox('Moivie Name :', mv['title'],
    # index=None,
    #   placeholder="Please Enter Movie Name that You Want To Search" )
# my_expander = st.expander(label='Expand me')
# with my_expander:
firstmovieid=-1
if(moviename):
    
    st.write('Searching for ' +moviename)
    m=mv[mv['title'].str.contains(moviename,na=False,case=False)==True]
    # st.write(type(m))
    # print(m)
    output=[[]]
    count=0  
    if len(m)>0:
        col1, col2, col3,col4 = st.columns(4,gap='small',vertical_alignment="top")
        
        
        for index, row in m.iterrows():
            if  row["vote_average"]>5:
                
                strHeader=f'{row["title"]} ({row["vote_average"]})'
                # strHeader=  f'<div style="vertical-alignment:top;max-height:40px;font-size: 15px;font-weight:600"><span style="width:30px;font-size:12px;padding:3px;text-align:center;border:1px solid;border-radius:50px;margin-top:-30px;"> {row["vote_average"]}</span>&nbsp;{row["title"]}</div>'
                
                poster=fetchPoster(row['id'])
                # 'https://image.tmdb.org/t/p/w500'+row["poster_path"]
                # st.write(count)
                count=count+1

                if count>3:
                    break

                if(count==1):
                    firstmovieid=row["id"]
                    with col1.container(height=250):
                        st.write(strHeader)              
                        # st.markdown(strHeader,unsafe_allow_html=True)
                        st.image(poster)
                        
                if(count==2):
                    with col2.container(height=250):
                    
                        st.write(strHeader) 
                        # st.markdown(strHeader,unsafe_allow_html=True)
                        st.image(poster)
                if(count==3):
                    with col3.container(height=250):
                    
                        st.write(strHeader) 
                            # st.markdown(strHeader,unsafe_allow_html=True)
                        st.image(poster)
                if(count==4):
                    with col4.container(height=250):
       
                        st.write(strHeader) 
                        # st.markdown(strHeader,unsafe_allow_html=True)
                        st.image(poster)
                
if firstmovieid>-1:
    fm=mv[mv.id==firstmovieid]
    iloc=fm.index[0]
    # st.write(fm)
    # st.write(iloc)
     
    movievector=similarmovie[iloc]
    # matched=sorted(list(enumerate( movievector)),reverse=True,key=lambda x:x[1])[1:6]
    matched=sorted(movievector,reverse=True,key=lambda x:x[1])[1:6]
    st.html("<b>Recomanded for You:<b>")
    cols = st.columns(5)
    icol=0
    for i in matched:
        c= mv.loc[i[0]]
        if(c.vote_average.astype(float)>5):
             with cols[icol]:
                poster=fetchPoster(c.id)
                st.write(f'{c.title}  | {c.vote_average}'  )
                st.image(poster)
                icol=icol+1
                if icol>=5:
                    break


