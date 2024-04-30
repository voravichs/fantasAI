import Header from "../../components/Header"
import { useState, useRef, useEffect } from 'react';
import './Connect4.css'; // Import your CSS file

import { PiPokerChipFill } from "react-icons/pi";

export default function Connect4() {

    const [board, setBoard] = useState([[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]])
    const [response, setResponse] = useState("Let's Play Connect 4!")
    const [move, setMove] = useState('');
    const [c4Visual, setC4Visual] = useState([]);
    
    const handleMakeConnect4Board = (key) => {
        setResponse("Ok, Let's start a new game!")
        fetch('http://localhost:8000/api/new_c4', {
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

    const handleMakeConnect4Move = (key) => {
        setResponse("Thinking...")
        fetch('http://localhost:8000/api/move_c4', {
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
                    tttArray.push(<PiPokerChipFill className="text-red-500"/>)
                } else if (board[i][j] === -1) {
                    tttArray.push(<PiPokerChipFill className="text-yellow-500"/>)
                } else {
                    tttArray.push("")
                }
            }
        }
        setC4Visual(tttArray)
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
                    <button id="generate-btn" onClick={handleMakeConnect4Board}>Start a New Game</button>
                    <label htmlFor="next_move">Type where you want to make a move</label>
                    <textarea
                        id="next_move"
                        rows="2"
                        value={move}
                        onChange={(e) => setMove(e.target.value)}
                    ></textarea>
                    <button id="generate-btn" onClick={handleMakeConnect4Move}>Make Your Move</button>
                </div>

                <div className="right-column flex-center flex-col">
                    <div className="w-3/5 h-3/5 grid grid-cols-7 grid-rows-7 items-center">
                    <div>0</div>
                    <div>1</div>
                    <div>2</div>
                    <div>3</div>
                    <div>4</div>
                    <div>5</div>
                    <div>6</div>
                    {c4Visual.map((item, index) => {
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