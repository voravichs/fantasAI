import beertower from "../../assets/images/beertower.jpg"
import redpanda from "../../assets/images/redpanda.jpg"
import cursedmodron from "../../assets/images/cursedmodron2.png"
import plasticredpandas from "../../assets/images/plasticredpandas.jpg"
import pixellink from "../../assets/images/pixellink.png"
import mushroom from "../../assets/images/mushroom.png"
import Header from "../../components/Header"
import { useGlobalState } from '../../PetClass';

import { Link } from "wouter";

export default function ImageSelect() {

    const images = [
        {src: beertower, alt: "an image of a beer tower"}, 
        {src: redpanda, alt: "an image of a red panda"},
        {src: cursedmodron, alt: "an image of a 3d shape with emoji faces, 3 forks, and 2 emoji feet"},
        {src: plasticredpandas, alt: "an image of a 3d printed plastic red panda"},
        {src: pixellink, alt: "an image of a blonde pixel character in green garb"},
        {src: mushroom, alt: "an image of a pixel art mushroom man"},
    ]

    const {selectedFile, setSelectedFile} = useGlobalState();

    return (
        <div className='h-dvh'>
            <Header/>
            <div className="text-3xl w-full p-8 flex flex-col items-center gap-4 h-4/5">
                <h1 className='text-4xl'>Choose an image</h1>
                <div className='grid grid-cols-4 grid-rows-2 gap-2'>
                    {images.map((image, index) => (
                        <div key={index} 
                            onClick={() => setSelectedFile(image.src)}
                            className='h-[300px] w-[300px]'
                        >
                            <img
                                src={image.src}
                                alt={image.alt || "Gallery Image"}
                                className={`h-full w-full object-contain rounded-lg active cursor-pointer
                                ${selectedFile === image.src ? 'ring-2 ring-offset-2 ring-blue-500' : 'hover:ring-1 hover:ring-gray-300'}`}
                            />
                        </div>
                        
                    ))}
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
            <div className="w-full flex-center">
                {selectedFile
                    ?<Link href={`/petgen/generate/`}>
                        <button className="text-2xl">Confirm</button>
                    </Link>
                    : null}
            </div>
            
            
        </div>
    )
}