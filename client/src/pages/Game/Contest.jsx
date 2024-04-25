import Header from "../../components/Header"

import { useState, useRef, useEffect } from 'react';
import './Contest.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';
import { Link } from "wouter";

export default function Contest(){
    const {name, setName,
        competitive, setCompetitive,
        physical, setPhysical,
        favColor, setFavColor,
        talkative, setTalkative,
        quicklyHungry, setQuicklyHungry,
        happiness, setHappiness,
        hunger, setHunger,
        likesSweet, setLikesSweet} = useGlobalState();

    const [currEnergy, setCurrEnergy] = useState(100)
    const [maxEnergy, setMaxEnergy] = useState(100)
    
    const [discussion, setDiscussion] = useState("")
    const [numTalks, setNumTalks] = useState(0)
    const [response, setResponse] = useState("Talk to me about the game, or anything!")

    const [m1Num, setM1Num] = useState(0)
    const [m1Name, setM1Name] = useState("")
    const [m1Desc, setM1Desc] = useState("")
    const [m2Num, setM2Num] = useState(0)
    const [m2Name, setM2Name] = useState("")
    const [m2Desc, setM2Desc] = useState("")
    const [m3Num, setM3Num] = useState(0)
    const [m3Name, setM3Name] = useState("")
    const [m3Desc, setM3Desc] = useState("")

    const [colorSelect, setColor] = useState("red")

    // const [board, setBoard] = useState([[0,0,0], [0,0,0], [0,0,0]])
    // const [response, setResponse] = useState("Let's Play Tic Tac Toe!")
    // const [move, setMove] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);

    const handleSetupGame = (key) => {
        fetch('http://localhost:8000/api/setup_contest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                name: name,
                physical_details: physical,
                fav_color: favColor,
                talkative: talkative,
                competitive: competitive,
                quicklyHungry: quicklyHungry,
                likesSweet: likesSweet,
                happiness: happiness,
                hunger: hunger
             })
        })
        .then(response => response.json())
        .then(data => {
            setMaxEnergy(data.maxEnergy);
            setCurrEnergy(data.currEnergy);
        })
        .catch(error => console.error('Error:', error));
    };
    
    const handleResetContest = (key) => {
        // setResponse("Ok, Let's start a new game!")
        fetch('http://localhost:8000/api/new_contest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            setCurrEnergy(data.currEnergy);
        })
        .catch(error => console.error('Error:', error));
    };

    const handleAskPet = (key) => {
        setResponse("Thinking...")
        fetch('http://localhost:8000/api/contest_pet_talk', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                discussion: discussion,
                m1Num: m1Num,
                m2Num: m2Num,
                m3Num: m3Num
             })
        })
        .then(response => response.json())
        .then(data => {
            setBoard(data.board);
            setResponse(data.response);
            setNumTalks(numTalks + 1);
        })
        .catch(error => console.error('Error:', error));
    };

    return (
        <div onLoad={handleSetupGame}>
            <Header/>
            <main>
            <div className="column-div">
                <div className="left-column">
                    <div>
                        <img src={uploadedImage ? URL.createObjectURL(uploadedImage) : '/Frog.gif'} alt="Pet" className="pet-image" />
                    </div>
                    <label htmlFor="energy">{currEnergy} out of {maxEnergy} Energy</label>
                    <progress id="energy" value={currEnergy} max={maxEnergy}> {currEnergy} out of {maxEnergy} </progress>
                    <p></p>
                    <button id="generate-btn" onClick={handleResetContest}>Start a New Game</button>
                    <label htmlFor="pet_discussion">{response}</label>
                    <textarea
                        id="pet_discussion"
                        rows="2"
                        value={discussion}
                        onChange={(e) => setDiscussion(e.target.value)}
                    ></textarea>
                    <button id="generate-btn" onClick={handleAskPet}>Talk with your pet</button>
                </div>

                <div className="right-column">
                    <p>
                        TEMP: {numTalks}
                    </p>
                    <p>
                        TEMP: {colorSelect}
                    </p>
                    <select name="Select Color" id="colorSelect">
                        <option value="red">Red</option>
                        <option value="green">Green</option>
                        <option value="yellow">Yellow</option>
                        <option value="orange">Orange</option>
                        <option value="violet">Violet</option>
                    </select>
                </div>

            </div>
            </main>
        </div>
    );
}