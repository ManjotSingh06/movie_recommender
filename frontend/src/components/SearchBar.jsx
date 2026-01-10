import React from 'react';

function SearchBar({ movies, onSelect }) {
  const styles = {
    container: { width: '100%', maxWidth: '400px', margin: '0 auto' },
    input: { width: '100%', padding: '10px', fontSize: '1rem', borderRadius: '5px', border: '1px solid #ccc' }
  };

  return (
    <div style={styles.container}>
      <input
        type="text"
        list="movie-titles"
        placeholder="Search a movie..."
        onChange={(e) => onSelect(e.target.value)}
        style={styles.input}
      />
      <datalist id="movie-titles">
        {movies.map((movie, index) => (
          <option key={index} value={movie} />
        ))}
      </datalist>
    </div>
  );
}

export default SearchBar;
