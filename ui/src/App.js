import React, { useState, useEffect } from 'react';

function App() {
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/hello-world')
            .then(response => response.json())
            .then(data => setMessage(data.message))
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <div className="App">
            <h1> Application demonstration integration albert Ai 

            </h1>
            <p>{message}</p>
        </div>
    );
}

export default App; 