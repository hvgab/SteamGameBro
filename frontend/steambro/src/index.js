import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import App from './App';
import Header from './components/Header';
import Footer from './components/Footer';
import connectionExample from './App';

const routing = (
  <BrowserRouter>
    <React.StrictMode>
      <Header />
      <Routes>
        <Route exact path='/' element={<App/>} />
        {/* <Route exact path={"/connectionExample"} component={connectionExample} /> */}
      </Routes>
      <Footer />
    </React.StrictMode>
  </BrowserRouter>
);

ReactDOM.render(routing, document.getElementById('root'));