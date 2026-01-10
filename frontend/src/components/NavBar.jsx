import React from 'react';

function Navbar() {
  const styles = {
    navbar: {
      backgroundColor: '#111',
      color: 'white',
      padding: '1rem 2rem',
      textAlign: 'center',
      width: '100vh'
    }
  };

  return (
    <nav style={styles.navbar}>
      <h2>🎬 Movie Recommender</h2>
    </nav>
  );
}

export default Navbar;
