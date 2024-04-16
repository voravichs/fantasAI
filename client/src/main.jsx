import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Feeding from "./components/Feeding"
import React, { useState, useRef, useEffect } from 'react';
import { PetClass } from './PetClass';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <PetClass>
    <App />
    <Feeding />
    </PetClass>
  </React.StrictMode>
);