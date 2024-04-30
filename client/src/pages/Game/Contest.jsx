import Header from "../../components/Header"

import { useState, useRef, useEffect } from 'react';
import './Contest.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';

export default function Contest(){
    const {happiness, hunger} = useGlobalState();

    const [currEnergy, setCurrEnergy] = useState(100)
    const [maxEnergy, setMaxEnergy] = useState(100)
    const [currPoints, setCurrPoints] = useState(0)
    const [goalPoints, setGoalPoints] = useState(100)
    const [phase, setPhase] = useState("Opener")
    const [multiplier, setMultiplier] = useState(1)
    
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

    const [summary, setSummary] = useState("")
    
    const handleResetContest = (key) => {
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
            setCurrPoints(data.currPoints);
            setGoalPoints(data.goalPoints);
            setPhase(data.phase);
            setMultiplier(data.multiplier);
            setSummary("");
        })
        .catch(error => console.error('Error:', error));

        handleNewMoves();
    };

    const handleNewMoves = (key) => {
        fetch('http://localhost:8000/api/new_contest_moves', {
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

    const handleMakeMove = (key) => {
        if (summary != "Making the Move..." && phase != "End of Show")
        {
            setSummary("Making the Move...")
            fetch('http://localhost:8000/api/move_contest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    move: key,
                    colorSelect: colorSelect,
                    numTalks: numTalks,
                    hunger: hunger,
                    happiness: happiness
                })
            })
            .then(response => response.json())
            .then(data => {
                setPhase(data.phase)
                setCurrEnergy(data.currEnergy)
                setCurrPoints(data.currPoints)
                setGoalPoints(data.goalPoints)
                setMultiplier(data.multiplier)
                setSummary(data.summary)
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
        }
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
                        Current Phase: {phase}
                    </p>
                    <p>{summary}</p>
                    <p></p>
                    <button id="Move1" onClick={(e) => handleMakeMove(e.target.value)} value={m1Num}>{m1Name}<br />{m1Desc}</button>
                    <button id="Move2" onClick={(e) => handleMakeMove(e.target.value)} value={m2Num}>{m2Name}<br />{m2Desc}</button>
                    <button id="Move3" onClick={(e) => handleMakeMove(e.target.value)} value={m3Num}>{m3Name}<br />{m3Desc}</button>
                    <p>------Game Info------</p>
                    <p>Current Points: {currPoints}</p>
                    <p>Point Goal: {goalPoints}</p>
                    <p>Current Point Multiplier: {multiplier}x</p>
                    <p>Current Hunger Level: {hunger}</p>
                    <p>Current Happiness Level: {happiness}</p>
                    <label htmlFor="colorSelect">Some Moves Require You to Select a Color</label>
                    <select name="Select Color" id="colorSelect" onChange={(e) => setColor(e.target.value)}>
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