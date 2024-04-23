import Header from "../../components/Header"

import { useState, useRef, useEffect } from 'react';
import './Feeding.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';
import { Link } from "wouter";

export default function Feeding() {
    
    const {
        happiness, setHappiness, 
        hunger, setHunger, 
        conversationStyle,
        talkative,
        likesSweet } = useGlobalState();

    const [userDescription, setUserDescription] = useState('');
    const [conversation, setConversation] = useState([]);
    const [foodOptions, setFoodOptions] = useState({});
    const [foodTypeOptions, setFoodTypeOptions] = useState({});
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
            const newConversation = [...conversation, { role: 'narration', content: data.narration }];
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
            body: JSON.stringify({ 
                food: key, 
                hunger_level: hunger, 
                happiness_level: happiness, 
                likes_sweet: likesSweet, 
                food_type: curFoodType,
                conversationStyle: conversationStyle,
                talkative: talkative,
             })
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'narration', content: data.describe }, { role: 'pet', content: data.pet_answer }];
            setConversation(newConversation);
            console.log("happiness:")
            console.log(data.happiness);
            setHappiness(data.happiness);
            console.log("hunger:")
            console.log(data.hunger);
            setHunger(data.hunger);
            setUserDescription('');
        })
        .catch(error => console.error('Error:', error));
    };

    const handleTalkToPet = () => {
        fetch('http://localhost:8000/api/feed_talk_to_pet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description: userDescription, likes_sweet: likesSweet, talkative: talkative, conversationStyle: conversationStyle })
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'pet', content: data.answer }];
            setConversation(newConversation);
            setUserDescription('');
            setModalIsOpen(false); // Close the modal after generating pet response
        })
        .catch(error => console.error('Error:', error));
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior of form submission
            handleTalkToPet();
        }

    };

    return (
        <div>
            <Header/>
            <main>
                <h2>Feed Pet</h2>
                <div>
                   
                   <div className="column-div">
                    <div className="left-column">
                        <div className = "pet-details">
                        <div>
                            <img src={uploadedImage ? URL.createObjectURL(uploadedImage) : '/Frog.gif'} alt="Pet" className="pet-image" />
                        </div>
                        <div  ref={conversationRef}>
                            <div className="pet-stats">
                                    Hunger Level: {hunger}
                            </div>
                            <div className="pet-stats">
                                    Happiness Level: {happiness}
                            </div>
                        </div>
                        </div>
                        <div className="fridge">
                            <button id="generate-btn" onClick={handleGenerateFood}>Use a spell to create food</button>
                            <div className="foodOptions" ref={conversationRef}>
                                {Object.keys(foodOptions).length === 0 ? <p></p> : <p>Click on a food item to feed your pet!</p>}
                                <div className='food-row'>
                                    {Object.entries(foodOptions).map(([key, val]) => (
                                        <button className="food-box" key={key} onClick={() => handleGenerateFeedPet(key)}>
                                        <p className = "food-title">{key}</p>
                                        <p className = "food-des">{val}</p>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                    


                    <div className="right-column">
                        <label htmlFor="description">Conversation with pet</label>
                        <div className="conversation" ref={conversationRef}>
                            {conversation.map((message, index) => (
                                <div key={index} className={`message ${message.role}`}>
                                    {message.content}
                                </div>
                            ))}
                        </div>
                        <label htmlFor="description">Ask pet about dietary preferences</label>
                        <textarea
                            id="description"
                            rows="2"
                            value={userDescription}
                            onChange={(e) => setUserDescription(e.target.value)}
                            onKeyDown={handleKeyPress} // Call handleKeyPress on key down event
                        ></textarea>

                    </div>

                    </div>
       
                </div>
            </main>
        </div>
    );
}
