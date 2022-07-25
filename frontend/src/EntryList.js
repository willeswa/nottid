import React, { useEffect, useState } from 'react';

function EntryList() {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [items, setItems] = useState([]);
    const [createButton, setCreateButton] = useState("Create journal")
    const [submit, setSubmit] = useState(false)
    const [text, setText] = useState("")
    const [hasError, setHasError] = useState(false)
    const [message, setMessage] = useState(null)

    useEffect(() => {
        const apikey = localStorage.getItem("apiKey");
        fetch("http://willies.eba-cdbcz9vh.us-east-2.elasticbeanstalk.com/nottid/entries", {
            headers: {
                'Authorization': apikey
            }
        })
            .then(res => {
                console.log(res.status)
                if (res.status == 401 || res.status == 403) {
                    localStorage.clear()
                    localStorage.setItem('expired', true);
                }
                return res.json()
            })
            .then((reseult) => {
                setIsLoaded(true);
                console.log()
                setItems(reseult.entries);
            },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                    console.log("error ==> " + error);
                })
    }, [])

    useEffect(() => {
        if (submit == true) {
            const apikey = localStorage.getItem("apiKey");
            fetch("http://willies.eba-cdbcz9vh.us-east-2.elasticbeanstalk.com/nottid/entries", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': apikey
                },
                body: JSON.stringify({ text: text })
            }).then(res => {
                if (res.status != 200) {
                    setHasError(true)
                }
                return res.json();
            })
                .then(result => {
                    setError(result.error)
                    setMessage(result.message)
                    setSubmit(false)
                    setText("")
                })
        }
    }, [submit])

    const handleSubmit = (event) => {
        event.preventDefault()
        setError(null)
        if (text == "") {
            alert("Jornal cannot be empty")
        } else {
            setSubmit(true)
        }
    }

    const onLogout = () => {
        localStorage.clear()
        window.location.reload(true)
    }

    const onTypingChange = (text) => {
        setMessage(null)
        setText(text)
    }

    if (error) {
        return <div>Error: {error}</div>
    } else if (!isLoaded) {
        return <div>Loading...</div>
    }
    return (
        <div className='Container'>
            <div className='Logout' > <button className='Button' onClick={() => onLogout()}>Logout</button></div>
            <div className='Block'>
                <p className='Heading'>Create A Jornal</p>
                <form onSubmit={handleSubmit}>
                    { message != null ? <p className='Subtitle'>{message}</p> : <p className='Subtitle'>{500 - text.length} characters remainging</p>}
                    <textarea className='TextArea' onChange={(e) => onTypingChange(e.target.value)}  value={text} rows={10} cols={60} maxLength={500}>
                    </textarea>
                    <button type='submit' className='Button AlignRight'>{createButton}</button>
                </form>
            </div>
            {items.length > 0 ? <ul className='Container'>
                {items.map(item => (
                    <li className='NiceItem' key={item.entry.entry_id}>
                        <p> {item.entry.text}</p>
                    </li>
                ))}
            </ul> : <p>n</p>}
        </div>
    );
}



export default EntryList;