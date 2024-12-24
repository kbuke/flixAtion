import { useOutletContext } from "react-router-dom";

import SignUp from "../1-SignUp/SignUp";
import Home from "../5-Home/Home";

export default function CheckLogin(){
    const appData=useOutletContext()
    
    const loggedUser = appData.loggedUser
    const setLoggedUser = appData.setLoggedUser

    const accounts = appData.accounts
    const setAccounts= appData.setAccounts

    console.log(loggedUser)
    console.log(accounts)

    return(
        <div>
            {!loggedUser ?
                <SignUp 
                    setAccounts={setAccounts}
                    setLoggedUser={setLoggedUser}
                />
                :
                <Home />
            }
        </div>
    )
}