import './App.css';
import EntryList from './EntryList';
import RegistrationScreen from './RegistrationScreen';
import React, { useState, useEffect } from 'react';
import LoginScreen from './LoginScreen';

function App() {
  const [apiKey, setApiKey] = useState(null);

  useEffect(() => {
    function checkIfLoggedIn() {
      const key = localStorage.getItem("apiKey");
      const expired = localStorage.getItem("expired");
      if (key) {
        setApiKey(key);
      } else {
        setApiKey(null);
      }

    }

    checkIfLoggedIn()

    window.addEventListener("storage", checkIfLoggedIn);

    return () => {
      window.removeEventListener("storage", checkIfLoggedIn);
    }
  }, [apiKey]);

  if (apiKey != null) {
    return <EntryList />
  }

  return (
    <div className='Row-Container'>
      <RegistrationScreen />
      <LoginScreen />
    </div>
  )

}

export default App;
