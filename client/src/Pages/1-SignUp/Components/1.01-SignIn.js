import "./1.01-SignIn.css"

import { useState } from "react"

export default function SignIn(){
    //Set state
    const [userEmail, setUserEmail] = useState("")
    const [userPassword, setUserPassword] = useState("")

    //Set up form schema
  
    //Create Inputs for sign in
    const signInInputs = (text, setVariable, type) => {
        return(
            <div
                className="userSignInInputContainer"
            >
                <label>
                    {text}
                </label>

                <input 
                    onChange={(e) => setVariable(e.target.value)}
                    type={type}
                    className="userSignInInputs"
                />
            </div>
        )
    }

    return(
        <form
            style={{display: "flex", flexDirection: "column"}}
        >
            <div>
                {signInInputs("Enter Email Address:", setUserEmail, "text")}
                {signInInputs("Enter Password:", setUserPassword, "password")}
            </div>

            <button
                id="signInButton"
            >
                Sign In
            </button>
        </form>
    )
}