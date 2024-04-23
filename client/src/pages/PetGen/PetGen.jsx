import { useGlobalState } from '../../PetClass';

import { TbCameraUp } from "react-icons/tb";
import { FaArrowAltCircleRight } from "react-icons/fa";
import { AiOutlineLoading } from "react-icons/ai";

import { useState } from 'react';
import { Link } from "wouter";
import { motion } from "framer-motion";

export default function PetGen() {
    const {selectedFile} = useGlobalState();

    const pet = {
        "identity": {
            "name": "Power-Up",
            "physical_details": "This virtual pet is a classic red mushroom with a white-spotted cap and a white stalk.",
            "full_description": "This virtual pet is an adorable and iconic red mushroom with white spots. It is commonly seen in video games as a power-up item, especially in the 'Super Mario' series."
        },
        "personality": {
            "conversationStyle": "Energetic",
            "talkative": true,
            "voice": 3,
            "fav_color": "red",
            "competitive": false,
            "likes_sweet": true,
            "quickly_hungry": false
        }
    }

    const [description, setDescription] = useState("")
    const [imgLink, setImgLink] = useState("");
    const [petJSON, setPetJSON] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleGenerateImage = () => {
        setImgLink("")
        setPetJSON(null)
        setDescription("Generating Pet...")
        setLoading(true);

        fetch('http://localhost:8000/api/generate_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: selectedFile.slice(1)
            })
        })
        .then(response => response.json())
        .then(data => {
            setDescription("")
            setLoading(false);
            setImgLink(data.link)
            setPetJSON(JSON.parse(data.json))
        })
        .catch(error => {
            setDescription("Something failed on the backend, please reboot the app!")
            console.error('Error:', error)

        });
    };

    return (
        <div className='h-dvh'>
            <div className="text-3xl w-full p-5 bg-header">
                <Link href="/">
                    <h1>FantasAI</h1>
                </Link>
            </div>
            <div className="text-3xl w-full p-4">
                <button onClick={handleGenerateImage}>Generate</button>
            </div>
            <div className='h-2/3 px-36 grid grid-cols-5 items-center justify-items-center gap-8'>
                <div className='col-span-2 w-full h-full flex-center flex-col gap-2'>
                    <div className='h-[400px] w-[400px] rounded-lg flex-center text-6xl text-gray-400'>
                        {selectedFile 
                            ? <img 
                                alt="preview image" 
                                className='h-full w-full object-contain rounded-lg'
                                src={selectedFile}/> 
                            : <TbCameraUp/>}
                    </div>
                </div>
                <FaArrowAltCircleRight className='text-7xl text-header bg-white rounded-full'/>
                <div className='col-span-2 p-8 flex-center flex-col gap-2'>
                    <div className='h-[400px] w-[400px] flex-center'>
                        {loading 
                            ? <div className='flex-center flex-col gap-4'>
                                <p>{description}</p>  
                                <motion.div 
                                    animate={{rotate: [0, 300, 360]}}
                                    transition={{
                                        ease: "linear",
                                        duration: 1,
                                        times: [0, 0.5, 1],
                                        repeat: Infinity
                                    }}    
                                    className='mx-auto'
                                >
                                    <AiOutlineLoading className='text-6xl'/>    
                                </motion.div>    
                            </div>
                            : null
                        }
                        {imgLink
                            ? 
                            <div>
                                <div className='h-[400px] w-[400px] rounded-lg flex-center text-6xl text-gray-400'>
                                    <img 
                                        alt="preview image" 
                                        className='h-full w-full object-contain rounded-lg border border-white'
                                        src={imgLink}/> 
                                </div>    
                                <div className='flex flex-col'>
                                    <p>Name: {petJSON.identity.name}</p>
                                    <p>{petJSON.identity.full_description}</p>
                                    <p></p>
                                </div>
                            </div>
                            : null} 
                    </div>
                    
                </div>
            </div>
            {imgLink
                ? <button className='text-3xl'>Save</button>
                : null}
           
        </div>
    );
}