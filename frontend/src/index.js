import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';           // Optional global styles
import App from './App';
import { CssBaseline } from '@mui/material'; // MUI baseline for global resets

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <CssBaseline />  {/* Apply Material UI's CSS reset */}
    <App />
  </React.StrictMode>
);
