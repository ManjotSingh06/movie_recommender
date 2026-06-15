
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import Navbar from './components/navBar';
import Header from './components/Header';
import SearchBar from './components/SearchBar.jsx'
import MovieCard from './components/MovieCard';
import './components/MovieModal';
import './components/Footer';
import MovieModal from './components/MovieModal';
import Footer from './components/Footer';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalMovie, setModalMovie] = useState(null);

  useEffect(() => {
    axios.get(`${API_URL}/movie_titles`)
      .then(res => {
        console.log("Movie titles:");
        setMovies(res.data);
      })
      .catch(err => console.error('Error fetching movie list:', err));
  }, []);

  const getRecommendations = () => {
    if (!selectedMovie) return;
    setLoading(true);
    axios.post(`${API_URL}/recommend`, { movie: selectedMovie })
      .then(res => {
        setRecommendations(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching recommendations:', err);
        setLoading(false);
      });
  };

  return (  
    <div className="app-container">
      
      <Header />

      <div className="dropdown-container">
        <SearchBar movies={movies} onSelect={setSelectedMovie}/>

        <button className="recommend-btn" onClick={getRecommendations} disabled={!selectedMovie}>
          Show Recommendations
        </button>
      </div>
      <div className="movie-searchbar">
      </div>

      {loading ? (
        <div className="loader"></div>
      ) : (
        <div className='recommandations-wrapper'>
          <div className="recommendations">
            {recommendations.map((rec, index) => (
              <MovieCard
                key={index}
                title={rec.title}
                poster={rec.poster}
                onClick={() => setModalMovie(rec.title)}
              />
            ))}
          </div>
        </div>
      )}
      <MovieModal movieTitle={modalMovie} onClose={() => setModalMovie(null)} />
      <Footer />
    </div>
  );
}

export default App;
