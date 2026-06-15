from flask import Flask,jsonify,request
import requests
import pickle
from flask_cors import CORS
from dotenv import OMDB_API_KEY

app = Flask(__name__)
CORS(app)

movies=pickle.load(open("movies_list.pkl","rb"))
similarity=pickle.load(open("similarity.pkl","rb"))



def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        data = requests.get(url).json()
        return data.get("Poster", "https://via.placeholder.com/500x750?text=No+Image")
    except:
        return "https://via.placeholder.com/500x750?text=Error"
    
@app.route('/movie_titles',methods=['GET'])
def get_title():
    return jsonify(list(movies['title'].values))

@app.route('/recommend',methods=['POST'])
def recommend():
    data=request.json
    movie=data['movie']
    if movie not in movies['title'].values:
        return jsonify([])
    
    index =movies[movies['title']==movie].index[0]
    distance = list(enumerate(similarity[index]))
    sorted_movies= sorted(distance,key=lambda x:x[1],reverse=True)[1:6]

    recommendations = []
    for i in sorted_movies:
        title = movies.iloc[i[0]].title
        poster = fetch_poster(title)
        recommendations.append({"title":title,"poster":poster})
    
    return jsonify(recommendations)
if __name__== '__main__':
    app.run(debug=True)


