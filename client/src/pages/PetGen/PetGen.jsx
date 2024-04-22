import { useState } from 'react';
import { Link } from "wouter";
import { FaUpload } from "react-icons/fa6";
import { TbCameraUp } from "react-icons/tb";
import { FaArrowAltCircleRight } from "react-icons/fa";
import { saveAs } from 'file-saver';
import beertower from "../../assets/images/beertower.jpg"
import redpanda from "../../assets/images/redpanda.jpg"

export default function PetGen() {

    const [description, setDescription] = useState("")
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDescImage = () => {
        setDescription("Generating fun description...")

        fetch('http://localhost:8000/api/describe_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: "client" + selectedFile
            })
        })
        .then(response => response.json())
        .then(data => {
            setDescription(data.description)
        })
        .catch(error => console.error('Error:', error));
    };

    // const handleFileChange = (event) => {
    //     if (event.target.files && event.target.files[0]) {
    //         setSelectedFile(URL.createObjectURL(event.target.files[0]));
    //         const imageBlob = fetch(selectedFile).then(response => response.blob());
    //         imageBlob.then(blob => {
    //             saveAs(blob, 'image.jpg');
    //         });
    //     }
    // };

    return (
        <div className='h-dvh'>
            <div className="text-3xl w-full p-5 bg-header">
                <Link href="/">
                    <h1>FantasAI</h1>
                </Link>
            </div>
            <div className="text-3xl w-full p-8 flex-center flex-col gap-4">
                <h1 className='text-4xl'>Choose an image</h1>
                <div className='flex gap-2'>
                    <div onClick={() => setSelectedFile(beertower)}
                        className=' bg-gray-500 h-[200px] w-[200px] rounded-lg flex-center text-6xl text-gray-400 cursor-pointer'>
                        <img 
                            alt="preview image" 
                            className='h-full w-full object-contain rounded-lg'
                            src={beertower}/> 
                    </div>
                    <div onClick={() => setSelectedFile(redpanda)}
                        className=' bg-gray-500 h-[200px] w-[200px] rounded-lg flex-center text-6xl text-gray-400 cursor-pointer'>
                        <img 
                            alt="preview image" 
                            className='h-full w-full object-contain rounded-lg'
                            src={redpanda}/> 
                    </div>
                </div>
            </div>
            {/* <div className="text-3xl w-full p-8 flex-center flex-col ">
                <div className="w-1/3 border-2 rounded-xl p-8 bg-white text-black">
                    <div className="flex-center gap-2 flex-col border-2 border-dashed rounded-lg p-8 relative">
                        <FaUpload className='text-5xl opacity-60'/>
                        <h3 className='opacity-60'>Click box to upload</h3>
                        <input 
                            type="file" 
                            onChange={handleFileChange}
                            className='absolute top-0 left-0 w-full h-full opacity-0 cursor-pointer'/>
                    </div>
                </div>
            </div> */}
            <div className='h-1/2 px-12 flex-center gap-8'>
                <div className=' bg-gray-500 h-[500px] w-[500px] rounded-lg flex-center text-6xl text-gray-400'>
                    {selectedFile 
                        ? <img 
                            alt="preview image" 
                            className='h-full w-full object-contain rounded-lg'
                            src={selectedFile}/> 
                        : <TbCameraUp/>}
                </div>
                <FaArrowAltCircleRight className='text-6xl'/>
                <div className='w-1/2 p-8'>
                    {description 
                        ? <p>{description}</p>
                        : null}
                </div>
            </div>
            <div className="text-3xl w-full p-8">
                <button onClick={handleDescImage}>Generate</button>
            </div>
            
        </div>
    );
}