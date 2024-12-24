
import { Outlet } from 'react-router-dom';
import './App.css';
import { useEffect, useState } from 'react';

function App() {
  const [accounts, setAccounts] = useState([])
  const [loggedUser, setLoggedUser] = useState([])

  //fetch all registered accounts
  useEffect(() => {
    fetch('/users')
    .then(r => {
      if(r.ok){
        r.json()
        .then(accounts => setAccounts(accounts))
      }
    })
  }, [])

  //fetch logged users
  useEffect(() => {
    fetch('/check_session')
    .then(r => {
      if(r.ok){
        r.json()
        .then(loggedUser => setLoggedUser(loggedUser))
      }
    })
  }, [])

  console.log(loggedUser)

  return(
    <div>
      <Outlet 
        context={{
          accounts: accounts,
          setAccounts: setAccounts,

          loggedUser: loggedUser, 
          setLoggedUser: setLoggedUser
        }}
      />
    </div>
  )
}

export default App;
