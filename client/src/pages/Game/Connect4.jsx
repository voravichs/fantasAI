import Header from "../../components/Header"
import { useState, useRef, useEffect } from 'react';
import './Connect4.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';

import { PiPokerChipFill } from "react-icons/pi";

export default function Connect4() {
    const {name, setName,
        competitive, setCompetitive,
        physical, setPhysical,
        favColor, setFavColor} = useGlobalState();

    const [board, setBoard] = useState([[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]])
    const [response, setResponse] = useState("Let's Play Connect 4!")
    const [move, setMove] = useState('');
    const [c4Visual, setC4Visual] = useState([]);
    // const [uploadedImage, setUploadedImage] = useState(null);

    // const handleSetupGame = (key) => {
    //     fetch('http://localhost:8000/api/setup_games', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({ 
    //             name: name,
    //             physical_details: physical,
    //             fav_color: favColor,
    //             competitive: competitive
    //          })
    //     })
    //     .then(response => response.json())
    //     .catch(error => console.error('Error:', error));
    // };
    
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
                    


                {/* <div className="right-column">
                    <div>
                        {board[0][0]}{board[0][1]}{board[0][2]}{board[0][3]}{board[0][4]}{board[0][5]}{board[0][6]}
                    </div>
                    <div>
                        {board[1][0]}{board[1][1]}{board[1][2]}{board[1][3]}{board[1][4]}{board[1][5]}{board[1][6]}
                    </div>
                    <div>
                        {board[2][0]}{board[2][1]}{board[2][2]}{board[2][3]}{board[2][4]}{board[2][5]}{board[2][6]}
                    </div>
                    <div>
                        {board[3][0]}{board[3][1]}{board[3][2]}{board[3][3]}{board[3][4]}{board[3][5]}{board[3][6]}
                    </div>
                    <div>
                        {board[4][0]}{board[4][1]}{board[4][2]}{board[4][3]}{board[4][4]}{board[4][5]}{board[4][6]}
                    </div>
                    <div>
                        {board[5][0]}{board[5][1]}{board[5][2]}{board[5][3]}{board[5][4]}{board[5][5]}{board[5][6]}
                    </div>
                </div> */}

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