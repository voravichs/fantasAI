import Header from "../../components/Header"

import { useState, useRef, useEffect } from 'react';
import './Chat.css'; // Import your CSS file
import Modal from 'react-modal'; // Import Modal from react-modal library

export default function Chat() {
    const [selectedVoice, setSelectedVoice] = useState('Random');
    const [userDescription, setUserDescription] = useState('');
    const [conversation, setConversation] = useState([]);
    const [petText, setPetText] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);
    const [modalIsOpen, setModalIsOpen] = useState(false); // State to manage modal open/close
    const conversationRef = useRef(null);

    const pet = JSON.parse(localStorage.getItem("currPet"));

    useEffect(() => {
        conversationRef.current.scrollTop = conversationRef.current.scrollHeight;
    }, [conversation]);

    const handleGenerateMeditation = () => {
        fetch('http://localhost:8000/api/pet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ voice: selectedVoice, description: userDescription, image: uploadedImage })
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'user', content: userDescription }, { role: 'pet', content: data.petText }];
            setConversation(newConversation);
            setPetText(data.petText);
            setUserDescription('');
            setUploadedImage(null);
            setModalIsOpen(false); // Close the modal after generating pet response
        })
        .catch(error => console.error('Error:', error));
    };

    // const handleImageUpload = (event) => {
    //     const file = event.target.files[0];
    //     setUploadedImage(file);
    // };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior of form submission
            handleGenerateMeditation();
        }
    };

    return (
        <div className="App">
            <Header/>
            <main>
                <div className="flex flex-col gap-8">
                    <div className="flex-center gap-8">
                        <div className="flex flex-col items-center">
                            <h2 className="text-2xl font-bold">{pet.identity.name}</h2>
                            <img className="h-[400px] w-[400px]" src={localStorage.getItem("currImg")} alt="Pet"/>
                        </div>
                        <div className="conversation w-1/3" ref={conversationRef}>
                            {conversation.map((message, index) => (
                                <div key={index} className={`message ${message.role}`}>
                                    {message.content}
                                </div>
                            ))}
                        </div>
                    </div>
                    
                    <div className="input-group">
                        <label className="text-xl" htmlFor="description">Chat with {pet.identity.name}!</label>
                        <textarea
                            id="description"
                            rows="2"
                            value={userDescription}
                            onChange={(e) => setUserDescription(e.target.value)}
                            onKeyDown={handleKeyPress} // Call handleKeyPress on key down event
                            className="w-1/2"
                        ></textarea>
                        <button id="generate-btn" onClick={handleGenerateMeditation}>Submit</button>
                    </div>
                    {/* <button onClick={() => setModalIsOpen(true)}>Create New Pet</button>
                    <Modal
                        isOpen={modalIsOpen}
                        onRequestClose={() => setModalIsOpen(false)}
                        className="custom-modal"
                        overlayClassName="custom-overlay"
                    >
                        <h2>Upload Your Pet's Image</h2>
                        <input type="file" accept="image/*" onChange={handleImageUpload} />
                        <button onClick={() => setModalIsOpen(false)}>Done</button>
                    </Modal> */}
                </div>
            </main>
        </div>
    );
}