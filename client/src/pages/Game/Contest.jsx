import Header from "../../components/Header"

import { useState, useRef, useEffect } from 'react';
import './Contest.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';

export default function Contest(){
    const {hunger, setHunger,} = useGlobalState();

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

    const [uploadedImage, setUploadedImage] = useState(null);
    
    const handleResetContest = (key) => {
        // setResponse("Ok, Let's start a new game!")
        fetch('http://localhost:8000/api/new_contest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                hunger: hunger
             })
        })
        .then(response => response.json())
        .then(data => {
            setMaxEnergy(data.maxEnergy);
            setCurrEnergy(data.currEnergy);
        })
        .catch(error => console.error('Error:', error));

        fetch('http://localhost:8000/api/contest_moves', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            setM1Num(data.m1Num)
            setM1Name(data.m1Name)
            setM1Desc(data.m1Desc)
            setM2Num(data.m2Num)
            setM2Name(data.m2Name)
            setM2Desc(data.m2Desc)
            setM3Num(data.m3Num)
            setM3Name(data.m3Name)
            setM3Desc(data.m3Desc)
        })
        .catch(error => console.error('Error:', error));
    };

    const handleNewMoves = (key) => {
        fetch('http://localhost:8000/api/contest_moves', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            setM1Num(data.m1Num)
            setM1Name(data.m1Name)
            setM1Desc(data.m1Desc)
            setM2Num(data.m2Num)
            setM2Name(data.m2Name)
            setM2Desc(data.m2Desc)
            setM3Num(data.m3Num)
            setM3Name(data.m3Name)
            setM3Desc(data.m3Desc)
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
                m3Num: m3Num,
                colorSelect: colorSelect,
                numTalks: numTalks
             })
        })
        .then(response => response.json())
        .then(data => {
            setResponse(data.response);
            setNumTalks(numTalks + 1);
        })
        .catch(error => console.error('Error:', error));
    };

    return (
        <div onLoad={handleResetContest}>
            <Header/>
            <main>
            <div className="column-div">
                <div className="left-column">
                    <div className="flex flex-col items-center">
                        <img className="h-[400px] w-[400px]" src={localStorage.getItem("currImg")} alt="Pet"/>
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
                    <p></p>
                    <button id="Move1">{m1Name}<br />{m1Desc}</button>
                    <button id="Move2">{m2Name}<br />{m2Desc}</button>
                    <button id="Move3">{m3Name}<br />{m3Desc}</button>
                    <p></p>
                    <button id="NewMoves" onClick={handleNewMoves}>New Moves</button>
                </div>

            </div>
            </main>
        </div>
    );
}