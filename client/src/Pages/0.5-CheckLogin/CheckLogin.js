import { useOutletContext } from "react-router-dom";

import SignUp from "../1-SignUp/SignUp";

export default function CheckLogin(){
    const appData=useOutletContext()
    
    const loggedUser = appData.loggedUser

    const accounts = appData.accounts
    const setAccounts= appData.setAccounts

    console.log(loggedUser)
    console.log(accounts)

    return(
        <div>
            {!loggedUser ?
                <SignUp 
                    setAccounts={setAccounts}
                />
                :
                null
            }
        </div>
    )
}