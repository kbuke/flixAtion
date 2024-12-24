import { useFormik } from "formik"
import "./1.01-SignIn.css"

import { useState } from "react"
import * as yup from "yup";

export default function SignIn({
    setLoggedUser
}){
    //Set state
    const [userEmail, setUserEmail] = useState("")
    const [userPassword, setUserPassword] = useState("")
    const [signInError, setSignInError] = useState(false)

    //Set up form schema
    const formSchema = yup.object().shape({
        userEmail: yup
            .string()
            .required("Please enter your email"),
        userPassword: yup
            .string()
            .required("Please enter password")
    })

    const formik = useFormik({
        initialValues: {
            userEmail: "",
            userPassword: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(values, null, 2),
            })
                .then(res => {
                    if(res.ok) {
                        return res.json()
                    } else {
                        setSignInError(true)
                    }
                })
                .then(user => {
                    if(user) {
                        setLoggedUser(user)
                    }
                })
        }
    })
  
    //Create Inputs for sign in
    const signInInputs = (text, variable, type) => {
        return(
            <>
                <div
                    className="userSignInInputContainer"
                >
                    <label>
                        {text}
                    </label>

                    <input 
                        className="userSignInInpus"
                        type={type}
                        onChange={formik.handleChange}
                        name={variable}
                        value={formik.values[variable]}
                    />
                </div>
                <p style={{color: "red"}}>
                    {formik.errors[variable]}
                </p>
            </>
        )
    }

    return(
        <form
            style={{display: "flex", flexDirection: "column"}}
            onSubmit={formik.handleSubmit}
        >
            <div>
                {signInInputs("Enter Email Address:", "userEmail", "text")}
                {signInInputs("Enter Password:", "userPassword", "password")}
            </div>

            <button
                id="signInButton"
                type="submit"
            >
                Sign In
            </button>
        </form>
    )
}