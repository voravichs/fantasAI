import { useState, useRef, useEffect } from 'react';
import './Feeding.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';
import { Link } from "wouter";

export default function Feeding() {
    
    const {name, setName,
        cheerful, setCheerful,
        talkative, setTalkative,
        quicklyHungry, setQuicklyHungry,
        happiness, setHappiness, 
        hunger, setHunger, 
        likesSweet, setLikesSweet} = useGlobalState();

    const [userDescription, setUserDescription] = useState({});
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
                cheerful: cheerful,
                talkative: talkative,
             })
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'narration', content: data.describe }, { role: 'pet', content: data.pet_answer }];
            setConversation(newConversation);
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
        }

    };

    return (
        <div>
            <header>
            <Link href="/">
                <h1>FantasAI</h1>
            </Link>
            </header>
            <main>
                <h2>Feed Pet</h2>
                <div>
                   
                   <div className="column-div">
                    <div className="left-column">
                        <div>
                            <img src={uploadedImage ? URL.createObjectURL(uploadedImage) : '/Frog.gif'} alt="Pet" className="pet-image" />
                        </div>
                        <div className="pet-stats" ref={conversationRef}>
                            <div>
                                    Hunger Level: {hunger}
                            </div>
                            <div>
                                    Happiness Level: {happiness}
                            </div>
                        </div>
                        <div className="input-group">
                            <button id="generate-btn" onClick={handleGenerateFood}>Open the fridge</button>
                            <div className="foodOptions" ref={conversationRef}>
                                <p>Click on a food item to feed your pet!</p>
                                <div className='food-row'>
                                    {Object.entries(foodOptions).map(([key, val]) => (
                                        <div className="food-box" key={key} onClick={() => handleGenerateFeedPet(key)}>
                                        <h3>{key}</h3>
                                        <p>{val}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                    


                    <div className="right-column">
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
