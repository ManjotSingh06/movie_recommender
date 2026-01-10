import React from 'react';

function Footer() {
  return (
    <footer style={{
      position: 'fixed',
      left: 0,
      right: 0,
      bottom: 0,
      width: '100%',
      textAlign: 'center',
      padding: '1px',
      background: '#000000ff',
      zIndex: 1000
    }}>
      <p>© 2025 Movie Recommender. Built with React + Flask.</p>
    </footer>
  );
}

export default Footer;
