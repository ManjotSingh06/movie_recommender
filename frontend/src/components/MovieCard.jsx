import React from 'react';

function MovieCard({ title, poster, onClick }) {
  return (
    <div className="card" onClick={onClick}>
      <img className="poster" src={poster} alt={title} />
      <div className="card-body">
        <p className="movie-title">{title}</p>
      </div>
    </div>
  );
}

export default MovieCard;
