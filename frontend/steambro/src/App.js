import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import SteamGames from './components/SteamGames'
import SteamGameLoadingComponent from './components/SteamGameLoading'
// import SteamGamesLoading from './components/SteamGameLoading'


function App() {
  const SteamGameLoading = SteamGameLoadingComponent(SteamGames);
  const [appState, setAppState] = useState({
    loading: false,
    steamGames: null,
  });
  
  useEffect(()=>{
    setAppState({ loading: true});
    const apiUrl = `http://localhost:8000/api/`
    fetch(apiUrl)
    .then((data)=> data.json())
    .then((steamGames) => {
      setAppState({ loading: false, steamGames: steamGames});
    });
    }, [setAppState]);
  return (
      <div className="App">
        <h1>SteamGames</h1>
        <SteamGameLoading isLoading={appState.loading} steamGames={appState.steamGames} />
      </div>
    );
}

export default App;