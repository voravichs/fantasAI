import React, { useState, useRef, useEffect } from 'react';
import './Feeding.css'; // Import your CSS file
import Modal from 'react-modal'; // Import Modal from react-modal library
import { useGlobalState } from '../PetClass';

function Feeding() {
    
    const {hunger, setHunger, happiness, setHappiness, likesSweet, setLikesSweet} = useGlobalState();

    const [selectedVoice, setSelectedVoice] = useState('Random');
    const [userDescription, setUserDescription] = useState('');
    const [conversation, setConversation] = useState([]);
    const [foodOptions, setFoodOptions] = useState({});
    const [foodTypeOptions, setFoodTypeOptions] = useState({});
    const [fedPet, setFedPet] = useState([]);
    const [foodAte, setFoodAte] = useState([]);
    const [uploadedImage, setUploadedImage] = useState(null);
    const conversationRef = useRef(null);

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
            const newConversation = [...conversation, { role: 'user', content: userDescription }, { role: 'fridge', content: data.food }];
            setConversation(newConversation);
            setFoodOptions(data.food);
            setFoodTypeOptions(data.food_type);
            console.log(data.food);
            setUserDescription('');
        })
        .catch(error => console.error('Error:', error));
    };

    const handleGenerateFeedPet = (key) => {

        const curFoodType = foodTypeOptions[key];

        fetch('http://localhost:8000/api/feed', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ food: key, hunger_level: hunger, happiness_level: happiness, likes_sweet: likesSweet, food_type: curFoodType })
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'pet', content: data.fed }, { role: 'ate', content: key }];
            setConversation(newConversation);
            setFedPet(data.fed);
            setFoodAte(key);
            setHappiness(data.happiness);
            setHunger(data.hunger);
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
                    <h2>Feed Pet</h2>
                    <img src={uploadedImage ? URL.createObjectURL(uploadedImage) : '/Frog.gif'} alt="Pet" className="pet-image" />
                    
                    <div className="petStats" ref={conversationRef}>
                    <div>
                            Hunger Level: {hunger}
                    </div>
                    <div>
                            Happiness Level: {happiness}
                    </div>
                    <div>
                            Food Preferences: {likesSweet}
                    </div>
                    </div>

                    <div className="petFed" ref={conversationRef}>
                    <div>
                            {foodAte}
                    </div>
                    <div>
                            {fedPet}
                    </div>
                    </div>

                    <div className="input-group">
                        <button id="generate-btn" onClick={handleGenerateFood}>Check what is in the fridge</button>
                        <div className="foodOptions" ref={conversationRef}>
                        <div className='food-row'>
                            {Object.entries(foodOptions).map(([key, val]) => (
                                <div className="food-box" key={key} onClick={() => handleGenerateFeedPet(key)}>
                                <h3>{key}</h3>
                                <p>{val}</p>
                                </div>
                            ))}
                        </div>

                        </div>
                        {/* <label htmlFor="description">I would like to feed my pet:</label>
                        <textarea
                            id="description"
                            rows="2"
                            value={userDescription}
                            onChange={(e) => setUserDescription(e.target.value)}
                            onKeyDown={handleKeyPress} // Call handleKeyPress on key down event
                        ></textarea> */}

                    </div>
                </div>
            </main>
        </div>
    );
}

export default Feeding;

