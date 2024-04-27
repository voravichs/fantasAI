import Header from "../../components/Header"

import { useState, useEffect } from 'react';
import './TTT.css'; // Import your CSS file

import { FaCircleDot } from "react-icons/fa6";
import { IoClose } from "react-icons/io5";

export default function Connect4() {

    const [board, setBoard] = useState([[0,0,0], [0,0,0], [0,0,0]])
    const [response, setResponse] = useState("Let's Play Tic Tac Toe!")
    const [move, setMove] = useState('');
    const [tttVisual, setTTTVisual] = useState(["", "", "", "", "", "", "", "", ""]);
    
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

    useEffect(() => {
        let tttArray = [];
        for (let i = 0; i < board.length; i++) {
            for (let j = 0; j < board[i].length; j++) {
                if (board[i][j] === 1) {
                    tttArray.push(<FaCircleDot/>)
                } else if (board[i][j] === -1) {
                    tttArray.push(<IoClose/>)
                } else {
                    tttArray.push("")
                }
            }
        }
        setTTTVisual(tttArray)
    }, [board]);

    return (
        <div>
            <Header/>
            <main>
            <div className="column-div">
                <div className="left-column">
                    <div className="mb-8">
                        <div className="flex flex-col items-center">
                            <img className="h-[400px] w-[400px]" src={localStorage.getItem("currImg")} alt="Pet"/>
                        </div>
                        <p className="text-yellow-300 italic">{response}</p>
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

                <div className="right-column flex-center flex-col">
                    <div className="w-1/2 h-1/2 grid grid-cols-3 grid-rows-3 items-center">
                    {tttVisual.map((item, index) => {
                        return (
                            <div className="flex-center text-6xl border h-full" key={index}>
                                {item 
                                ? <div>{item}</div>
                                : <div></div>}
                            </div>
                        )
                    })}
                    </div>
                </div>

            </div>
            </main>
        </div>
    );
}