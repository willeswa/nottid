import React, { useState, useEffect } from 'react';
import './App.css';

function LoginScreen() {
    const [submit, setSubmit] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("")

    useEffect(() => {
        if (submit) {
            setIsLoading(true)
            fetch("http://willies.eba-cdbcz9vh.us-east-2.elasticbeanstalk.com/nottid/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            })
                .then(res => {
                    if (res.status != 200) {
                        setError("");
                    }
                    return res.json();
                })
                .then((result) => {
                    setIsLoading(false);
                    setError(result.error);
                    localStorage.setItem('isLoggedIn', true);
                    localStorage.setItem('apiKey', result.token);
                    window.location.reload(true)
                },
                    (error) => {
                        setIsLoading(false);
                        setError(error);
                    })
        }
        setSubmit(false)
    }, [submit])


    const handleSubmit = (event) => {
        event.preventDefault()
        setError(null)
        if (email == null || password == "") {
            alert("email or password cannot be empty")
        } else {
            setSubmit(true)
        }
    }
    return (<div className='Block'>
        <p className='error'>{error}</p>
        <p className='Heading'>Already have an account? Login to continue</p>
        <form onSubmit={handleSubmit}>
            <input
                type='email' id='email'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder='Enter email' className='InlineBlock' />
            <input
                type='password'
                id='password'
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder='******'
                className='InlineBlock' />
            <button type='submit' className='Flex-Item-Half Button'>{isLoading ? "Loading" : "Login"}</button>
        </form>

    </div>)
}

export default LoginScreen;