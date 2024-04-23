import Header from "../../components/Header"
import { useState, useRef, useEffect } from 'react';
import './TTT.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';

export default function Connect4() {
    const {name, setName,
        competitive, setCompetitive,
        cheerful, setCheerful,
        talkative, setTalkative,
        quicklyHungry, setQuicklyHungry,
        happiness, setHappiness, 
        hunger, setHunger, 
        likesSweet, setLikesSweet} = useGlobalState();

    const [board, setBoard] = useState([[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]])
    const [response, setResponse] = useState("Default Response")

    const [move, setMove] = useState('');
    const [conversation, setConversation] = useState([]);
    const [foodOptions, setFoodOptions] = useState({});
    const [foodTypeOptions, setFoodTypeOptions] = useState({});
    const [uploadedImage, setUploadedImage] = useState(null);
    const conversationRef = useRef(null);

    useEffect(() => {
        conversationRef.current.scrollTop = conversationRef.current.scrollHeight;
    }, [conversation]);

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior of form submission
        }
    };

    
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
                move: move, 
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
        <div>
            <Header/>
            <main>
            <div className="column-div">
                <div className="left-column">
                    <div>
                        <img src={uploadedImage ? URL.createObjectURL(uploadedImage) : '/Frog.gif'} alt="Pet" className="pet-image" />
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
                    


                <div className="right-column">
                    <div className="conversation" ref={conversationRef}>
                        {conversation.map((message, index) => (
                            <div key={index} className={`message ${message.role}`}>
                                {message.content}
                            </div>
                        ))}
                    </div>
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
                    <div>
                        {response}
                    </div>
                </div>

            </div>
            </main>
        </div>
    );
}