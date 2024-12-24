import { useState } from "react";
import * as yup from "yup";
import { useFormik } from "formik";


export default function SignUpContainer({
    setAccounts
}){
    
    //set state
    const [signUpComplete, setSignUpComplete] = useState(false);
    const [loading, setLoading] = useState(false);
    const [emailInUse, setEmailInUse] = useState(false)

    //Set up form schema
    const formSchema = yup.object().shape({
        newUserEmail: yup
            .string()
            .email("Invalid email address")
            .required("Must enter an email address"),
        newUserPassword: yup
            .string()
            .required("Must enter a password"),
        confirmPassword: yup
            .string()
            .oneOf([yup.ref("newUserPassword"), null], "Passwords must match")
            .required("Must confirm password"),
        newUserFirstName: yup
            .string()
            .required("Must enter first name"),
        newUserSurname: yup 
            .string()
            .required("Must enter last name"),
        newUserIntro: yup
            .string(),
    })

    const formik = useFormik({
        initialValues: {
            newUserEmail: "",
            newUserPassword: "",
            confirmPassword: "",
            newUserFirstName: "",
            newUserSurname: "",
            newUserIntro: "",
            newUserType: "User"
        },
        validationSchema: formSchema,
        onSubmit: (values) => { // Correct casing here
            setLoading(true);
            fetch("/users", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(values, null, 2)
            })
                .then(res => {
                    setLoading(false);
                    if (res.status === 201) {
                        setSignUpComplete(true);
                        // Fetch all users again after successful signup
                        fetch("/users")
                            .then(r => {
                                if (r.ok) {
                                    r.json().then(users => setAccounts(users));
                                }
                            });
                    } else if (res.status === 400) {
                        setEmailInUse(true);
                    }
                })
                .catch(() => {
                    setLoading(false);
                });
        }
    });
    

    //Set up new user inputs
    const newUser = (labelHeader, variable, inputType) => {
        return(
            <>
                <div
                    style={{
                        marginBottom: "10px"
                    }}
                >
                    <label>
                        {labelHeader}
                    </label>

                    <input 
                        onChange={formik.handleChange}
                        type={inputType}
                        style={{marginLeft: "10px"}}
                        name={variable}
                        value={formik.values[variable]}
                    />
                </div>
                <p
                    style={{color: "red"}}
                >
                    {formik.errors[variable]}
                </p>
            </>
        )
    }

    console.log(signUpComplete)

    return signUpComplete ? (
            <div id="signUpConfirmed">
                <h2>Thank you for signing up to Flix-Ation</h2>
                <h2 style={{ marginLeft: "10px", marginRight: "10px" }}>
                    Please log in to get your cinematic journey started
                </h2>
            </div>
            ) : (
            <form
                onSubmit={formik.handleSubmit}
            >
                <>
                    {newUser("Enter your email:", "newUserEmail", "text")}
                    {newUser("Enter your password:", "newUserPassword", "password")}
                    {newUser("Re-enter Password:", "confirmPassword", "password")}
                    {newUser("Enter your first name:", "newUserFirstName", "text")}
                    {newUser("Enter your surname:", "newUserSurname", "text")}
                    {newUser("Enter your introduction:", "newUserIntro", "text")}
                </>

                <button
                    type="submit"
                >
                    Sign Up
                </button>
            </form>
    )
}
