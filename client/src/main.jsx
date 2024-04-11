import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Feeding from "./components/Feeding"

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
    <Feeding />
  </React.StrictMode>
);