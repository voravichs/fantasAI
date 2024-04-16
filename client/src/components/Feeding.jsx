import React, { useState, useRef, useEffect } from 'react';
import './Feeding.css'; // Import your CSS file
import Modal from 'react-modal'; // Import Modal from react-modal library

function Feeding() {
    const [selectedVoice, setSelectedVoice] = useState('Random');
    const [userDescription, setUserDescription] = useState('');
    const [conversation, setConversation] = useState([]);
    const [foodOptions, setFoodOptions] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);
    const conversationRef = useRef(null);

    const pet = {
        "identity": {
            "name": "Hot Pot",
            "physical_details": "A living kettle",
        },
        "personality": {
          "cheerful": true,
          "talkative": true,
          "voice": 0,
          "fav_color": "blue",
          "competitive": true,
          "likes_sweet": true,
          "quickly_hungry": true,
          "introversion": true,
          "hobby": "hiking",
        },
    
        "mood": {
            "hunger_level": 0,
            "happiness": 5,
            "social_battery": 5,
            "last_updated": 0
        }
    }

    useEffect(() => {
        conversationRef.current.scrollTop = conversationRef.current.scrollHeight;
    }, [conversation]);

    const handleGenerateFood = () => {
        fetch('http://localhost:8000/api/food', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify()
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'user', content: userDescription }, { role: 'user', content: data.food }];
            setConversation(newConversation);
            setFoodOptions(data.food);
            setUserDescription('');
        })
        .catch(error => console.error('Error:', error));
    };

    const handleGenerateFeedPet = () => {
        fetch('http://localhost:8000/api/feed', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ food: userDescription })
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'pet', content: data.fed }];
            setConversation(newConversation);
            setUserDescription('');
        })
        .catch(error => console.error('Error:', error));
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior of form submission
            handleGenerateFeedPet();
        }
    };

    return (
        <div className="App">
            <header>
                <h1>FantasAI</h1>
            </header>
            <main>
                <div className="container">
                    <h2>Frogbert</h2>
                    <img src={uploadedImage ? URL.createObjectURL(uploadedImage) : '/Frog.gif'} alt="Pet" className="pet-image" />
                    <div className="conversation" ref={conversationRef}>
                        {conversation.map((message, index) => (
                            <div key={index} className={`message ${message.role}`}>
                                {message.content}
                            </div>
                        ))}
                    </div>
                    <div className="input-group">
                        <button id="generate-btn" onClick={handleGenerateFood}>Generate Food Options</button>
                        <label htmlFor="description">Enter your prompt:</label>
                        <textarea
                            id="description"
                            rows="2"
                            value={userDescription}
                            onChange={(e) => setUserDescription(e.target.value)}
                            onKeyDown={handleKeyPress} // Call handleKeyPress on key down event
                        ></textarea>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default Feeding;

