import React, { useEffect, useState } from 'react';
import axios from 'axios';

function MovieModal({ movieTitle, onClose }) {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    if (!movieTitle) {
      setInfo(null);
      return;
    }
    axios.get(`https://www.omdbapi.com/?t=${movieTitle}&apikey=ac5fb13`)
      .then(res => setInfo(res.data));
  }, [movieTitle]);

  if (!movieTitle || !info) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.6)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 6000
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: '8px',
          padding: '20px',
          maxWidth: '600px',
          width: '90%',
          boxSizing: 'border-box',
          color: '#000'
        }}
        onClick={e => e.stopPropagation()}
      >
        <h2>{info.Title}</h2>
        <img src={info.Poster} alt={info.Title} style={{maxWidth: '100%', height: 'auto', marginBottom: '12px'}} />
        <p><strong>Year:</strong> {info.Year}</p>
        <p><strong>Genre:</strong> {info.Genre}</p>
        <p><strong>Plot:</strong> {info.Plot}</p>
        <div style={{textAlign: 'right', marginTop: '12px'}}>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}

export default MovieModal;
