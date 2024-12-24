
import { useState } from "react"
import "./SignUp.css"

import SignIn from "./Components/1.01-SignIn"
import SignUpContainer from "./Components/1.02-SignUpContainer"

import logo from "../../assets/Logo.png"

export default function SignUp({
    setAccounts,
    setLoggedUser
}){
    //set state
    const [signInUp, setSignInUp] = useState("In")

    const signInBackground="https://www.theyshootpictures.com/resources/hitchcockalfred01.jpg"

    const pgOptions = (option, setVariable, chosenOption, buttonOption) => {
        return(
            <div
                style={{display: "flex", flexDirection: "column"}}
            >
                <p
                    style={{marginBottom: "2px", color: "rgb(198, 7, 179)"}}
                >
                    {option}
                </p>

                <button
                    onClick={() => setVariable(chosenOption)}
                    id="signInOptionButton"
                >
                    {buttonOption}
                </button>
            </div>
        )
    }

    return(
        <div
            id="signUpPg"
            style={{
                backgroundImage: `url(${signInBackground})`
            }}
        >  
            <img 
                src={logo}
                id="signUpLogo"
            />
            <div
                id={signInUp === "In"? "signInContainer" : "signUpContainer"}
            >
                <h3>{
                    signInUp === "In" ? 
                        `Sign-In to Flix-Ation` 
                    :
                        "Sign-Up to Flix-Ation"
                    }
                </h3>

                {signInUp === "In"?
                    <SignIn 
                    setLoggedUser={setLoggedUser}
                    />
                    :
                    <SignUpContainer 
                        setAccounts={setAccounts}
                    />
                }

                {signInUp === "In"?
                    pgOptions(
                        "Don't have an account?",
                        setSignInUp,
                        "Up",
                        "Create An Account"
                    )
                    :
                    pgOptions(
                        "Already have an account?",
                        setSignInUp,
                        "In",
                        "Go to Sign In"
                    )
                }
            </div>
        </div>
    )
}