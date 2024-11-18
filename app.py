import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

st.set_page_config(layout="wide")
# modal = Modal(key="Demo Key",title="Related Movies",width="large")

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
tags=pickle.load(open('unique_tags.pkl','rb'))


API_KEY=st.secrets['API_KEY']
poster_path='https://image.tmdb.org/t/p/w200/'
url='https://api.themoviedb.org/3/movie/'

def fetchPoster(movieid):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movieid,API_KEY))
    data=response.json()    
    return poster_path+data['poster_path']

st.title('Movie Search And Recommendation  System ')

mv=pd.read_csv('movie_tags_1.csv')
colt1,colt2=st.columns(2)

moviename=colt1.selectbox('Search by [Actors/Actoress/Director/Movie Name]:',tags )
content=colt2.text_area('Search by contect:' )

count=0 

@st.dialog("Related Movies", width="large")
def related(title,index):
    # st.write(index)
    movievector=similarmovie[index]
    # st.write(movievector)
    # matched=sorted(list(enumerate( movievector)),reverse=True,key=lambda x:x[1])[1:6]
    matched=sorted(movievector,reverse=True,key=lambda x:x[1])[1:6]
    st.write("Related to this :red["+title+"] Movie")
    cols = st.columns(5)
    icol=0
    for i in matched:
         c= mv.loc[i[0]]

         if(c.vote_average.astype(float)>5):
              with cols[icol]:
                 poster=fetchPoster(c.id)
                 strHeader=f':blue[{c["title"]}] &mdash; :green[{c["vote_average"]}]'
                 st.write(strHeader )
                 st.image(poster)
                 icol=icol+1
                 if icol>=5:
                     break
if content:
    query=content
    moviename=""
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

        if ccount>12:
            break

        if(ccount==1 or ccount==5  or ccount==9):
            
            with ccol1:
                if st.button(strHeader,key=f"br{c['id']}"):

                    # with modal.container():
                    related(c["title"], i)

                st.image(poster)
                
        if(ccount==2 or ccount==6 or ccount==10):
            with ccol2:
            
                if st.button(strHeader,key=f"br{c['id']}"):

                    # with modal.container():
                    related(c["title"], i)
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
        if(ccount==3 or ccount==7 or ccount==11):
            with ccol3:
            
                if st.button(strHeader,key=f"br{c['id']}"):

                    # with modal.container():
                    related(c["title"], i)
                    # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
        if(ccount==4 or ccount==8 or ccount==12):
            with ccol4:

                if st.button(strHeader,key=f"br{c['id']}"):

                    # with modal.container():
                    related(c["title"], i) 
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)

if(moviename ):
    
    st.write(f"Searching For {moviename}.. After displaying the result :red[Click On The Title To See the Related Movie]")
    search_pattern=moviename
    m=mv[mv['tags'].str.contains(moviename,na=False,case=False)==True]
    # st.write(type(mv['tags']))
    # matching_rows_with_pattern = mv[mv['tags'].contains(moviename)==True] #.apply(lambda lst: any(search_pattern in item for item in lst)) ]
    mlist=m.sort_values(by='vote_average',ascending=False)[:8]
    col1, col2, col3,col4 = st.columns(4,gap='small',vertical_alignment="top")
    for index, row in mlist.iterrows():
        # strHeader=f'<span style="font-size=12px;color:dak-green">{row["title"]} ({row["vote_average"]})</span>'
        strHeader=f':blue[{row["title"]}] &mdash; :green[{row["vote_average"]}]'
        poster=fetchPoster(row['id'])
        count=count+1
        
        if count>10:
            break 

        if(count==1 or count==5):
            
            with col1:
                if st.button(strHeader,key=f"b{row['id']}"):

                    # with modal.container():
                    related(row["title"], index)
                
                     
                # st.text_input(label)
                              
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
                
                
        if(count==2 or count==6):
            with col2:
            
                if st.button(strHeader,key=f"b{row['id']}"):
                    # with modal.container():
                    related(row["title"], index)
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
        if(count==3 or count==7):
            with col3:
            
                if st.button(strHeader,key=f"b{row['id']}"):
                    # with modal.container():
                    related(strHeader, index)
                    # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)
        if(count==4 or count==8):
            with col4:

                if st.button(strHeader,key=f"b{row['id']}"):
                    # with modal.container():
                    related(row["title"], index)
                # st.markdown(strHeader,unsafe_allow_html=True)
                st.image(poster)





#     st.write('Searching for ' +moviename)
#     m=mv[mv['title'].str.contains(moviename,na=False,case=False)==True]
#     # st.write(type(m))
#     # print(m)
#     output=[[]]
#     count=0  
#     if len(m)>0:
#         col1, col2, col3,col4 = st.columns(4,gap='small',vertical_alignment="top")
        
        
#         for index, row in m.iterrows():
#             if  row["vote_average"]>5:
                
#                 strHeader=f'{row["title"]} ({row["vote_average"]})'
#                 # strHeader=  f'<div style="vertical-alignment:top;max-height:40px;font-size: 15px;font-weight:600"><span style="width:30px;font-size:12px;padding:3px;text-align:center;border:1px solid;border-radius:50px;margin-top:-30px;"> {row["vote_average"]}</span>&nbsp;{row["title"]}</div>'
                
#                 poster=fetchPoster(row['id'])
#                 # 'https://image.tmdb.org/t/p/w500'+row["poster_path"]
#                 # st.write(count)
#                 count=count+1

#                 if count>3:
#                     break

#                 if(count==1):
#                     firstmovieid=row["id"]
#                     with col1.container(height=250):
#                         st.write(strHeader)              
#                         # st.markdown(strHeader,unsafe_allow_html=True)
#                         st.image(poster)
                        
#                 if(count==2):
#                     with col2.container(height=250):
                    
#                         st.write(strHeader) 
#                         # st.markdown(strHeader,unsafe_allow_html=True)
#                         st.image(poster)
#                 if(count==3):
#                     with col3.container(height=250):
                    
#                         st.write(strHeader) 
#                             # st.markdown(strHeader,unsafe_allow_html=True)
#                         st.image(poster)
#                 if(count==4):
#                     with col4.container(height=250):
       
#                         st.write(strHeader) 
#                         # st.markdown(strHeader,unsafe_allow_html=True)
#                         st.image(poster)
                        
                        
# content=st.text_area("Search By Content:")
     
        

# # moviename=st.selectbox('Moivie Name :', mv['title'],
#     # index=None,
#     #   placeholder="Please Enter Movie Name that You Want To Search" )
# # my_expander = st.expander(label='Expand me')
# # with my_expander:
# firstmovieid=-1

                
# if firstmovieid>-1:
#     fm=mv[mv.id==firstmovieid]
#     iloc=fm.index[0]
#     # st.write(fm)
#     # st.write(iloc)
     
#     movievector=similarmovie[iloc]
#     # matched=sorted(list(enumerate( movievector)),reverse=True,key=lambda x:x[1])[1:6]
#     matched=sorted(movievector,reverse=True,key=lambda x:x[1])[1:6]
#     st.html("<b>Recomanded for You:<b>")
#     cols = st.columns(5)
#     icol=0
#     for i in matched:
#         c= mv.loc[i[0]]
#         if(c.vote_average.astype(float)>5):
#              with cols[icol]:
#                 poster=fetchPoster(c.id)
#                 st.write(f'{c.title}  | {c.vote_average}'  )
#                 st.image(poster)
#                 icol=icol+1
#                 if icol>=5:
#                     break


