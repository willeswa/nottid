import React, { useState, useEffect } from 'react';
import './App.css';

function RegistrationScreen() {
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");
    const [submit, setSubmit] = useState(false);

    useEffect(() => {
       if(submit){
        setIsLoading(true)
        fetch("http://willies.eba-cdbcz9vh.us-east-2.elasticbeanstalk.com/nottid/register",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email: email, password: password, username: username})
        })
        .then(res => {
            if(res.status != 200){
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
   
    // setButtonText("Create account")
    // setSubmit(false)


    const handleSubmit = (event) => {
        event.preventDefault()
        setError(null)
        if (email == null || username == "" || password == "") {
            alert("email or password or username cannot be empty")
        } else {
            setSubmit(true)
        }
    }

    return (<div className='Block'>
        <p className='error'>{error}</p>
        <p className='Heading'>Register to get started</p>
        <form
            onSubmit={handleSubmit}>
            <input
                type='text'
                id='username'
                onChange={(e) => setUsername(e.target.value)}
                value={username} placeholder='Enter username'
                className='InlineBlock' />
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
            <button
                type='submit'
                className='Flex-Item-Half Button'
            >{isLoading? 'Loading...': 'Create an account'}</button>
        </form>
    </div>)
}

export default RegistrationScreen;