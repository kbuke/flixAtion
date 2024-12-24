import { Children } from "react";

import App from "./App";

import CheckLogin from "./Pages/0.5-CheckLogin/CheckLogin";
import SignUp from "./Pages/1-SignUp/SignUp";
import Interests from "./Pages/2-Interests/Interests";
import Home from "./Pages/5-Home/Home";


const routes = [
    {
        path: "/",
        element: <App />,
        children: [{
            path: "/",
            element: <CheckLogin />,
            children: [
                {
                    path: '/',
                    element: <SignUp />
                },
                {
                    path: '/',
                    element: <Home />
                }
            ]
        }]
    }
]

export default routes