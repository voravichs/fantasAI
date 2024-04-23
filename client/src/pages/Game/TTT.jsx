import Header from "../../components/Header"

import { useState, useRef, useEffect } from 'react';
import './TTT.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';
import { Link } from "wouter";

export default function Connect4() {
    const {name, setName,
        competitive, setCompetitive,
        physical, setPhysical,
        favColor, setFavColor} = useGlobalState();

    const [board, setBoard] = useState([[0,0,0], [0,0,0], [0,0,0]])
    const [response, setResponse] = useState("Let's Play Tic Tac Toe!")
    const [move, setMove] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);

    const handleSetupGame = (key) => {
        fetch('http://localhost:8000/api/setup_games', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                name: name,
                physical_details: physical,
                fav_color: favColor,
                competitive: competitive
             })
        })
        .then(response => response.json())
        .catch(error => console.error('Error:', error));
    };
    
    const handleMakeTTTBoard = (key) => {
        setResponse("Ok, Let's start a new game!")
        fetch('http://localhost:8000/api/new_ttt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            setBoard(data.board);
        })
        .catch(error => console.error('Error:', error));
    };

    const handleMakeTTTMove = (key) => {
        setResponse("Thinking...")
        fetch('http://localhost:8000/api/move_ttt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                move: move
             })
        })
        .then(response => response.json())
        .then(data => {
            setBoard(data.board);
            setResponse(data.response);
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
                        <p>{response}</p>
                    </div>
                    <button id="generate-btn" onClick={handleMakeTTTBoard}>Start a New Game</button>
                    <label htmlFor="next_move">Type where you want to make a move</label>
                    <textarea
                        id="next_move"
                        rows="2"
                        value={move}
                        onChange={(e) => setMove(e.target.value)}
                    ></textarea>
                    <button id="generate-btn" onClick={handleMakeTTTMove}>Make Your Move</button>
                </div>

                <div className="right-column">
                    <p>
                        {board[0][0]}{board[0][1]}{board[0][2]}
                    </p>
                    <p>
                        {board[1][0]}{board[1][1]}{board[1][2]}
                    </p>
                    <p>
                        {board[2][0]}{board[2][1]}{board[2][2]}
                    </p>
                </div>

            </div>
            </main>
        </div>
    );
}