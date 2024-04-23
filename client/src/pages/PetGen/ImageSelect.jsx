import beertower from "../../assets/images/beertower.jpg"
import redpanda from "../../assets/images/redpanda.jpg"
import cursedmodron from "../../assets/images/cursedmodron2.png"
import plasticredpandas from "../../assets/images/plasticredpandas.jpg"
import pixellink from "../../assets/images/pixellink.png"
import mushroom from "../../assets/images/mushroom.png"
import alien from "../../assets/images/alien.png"
import holyparrot from "../../assets/images/holyparrot.png"
import bddog from "../../assets/images/bddog.jpg"
import bdrobot from "../../assets/images/bdrobot.jpg"
import redtree from "../../assets/images/redtree.jpg"
import hairycheese from "../../assets/images/hairycheese.jpg"
import turtleonturtle from "../../assets/images/turtleonturtle.png"
import markersword from "../../assets/images/markersword.png"
import littlebeetle from "../../assets/images/littlebeetle.png"
import cocoapuffs from "../../assets/images/cocoapuffs.jpg"

import { FaChevronCircleRight, FaChevronCircleLeft} from "react-icons/fa";

import Header from "../../components/Header"
import { useGlobalState } from '../../PetClass';

import { Link } from "wouter";
import { useState } from "react"

export default function ImageSelect() {

    const images1 = [
        {src: beertower, alt: "an image of a beer tower"}, 
        {src: redpanda, alt: "an image of a red panda"},
        {src: cursedmodron, alt: "an image of a 3d shape with emoji faces, 3 forks, and 2 emoji feet"},
        {src: plasticredpandas, alt: "an image of a 3d printed plastic red panda"},
        {src: pixellink, alt: "an image of a blonde pixel character in green garb"},
        {src: mushroom, alt: "an image of a pixel art mushroom man"},
        {src: alien, alt: "an image of a starfish alien with 6 arms and 4 eyes"},
        {src: holyparrot, alt: "an image of a parrot priest"},
    ]

    const images2 = [
        {src: bddog, alt: "an image of a robotic dog"}, 
        {src: bdrobot, alt: "an image of a robot posing"},
        {src: redtree, alt: "an image of a red tree growing out of a concrete block"},
        {src: hairycheese, alt: "an image of a modern art sculpture of a block of cheese with hair"},
        {src: turtleonturtle, alt: "an image of an emoji of a turtle with a smaller turtle on top of it"},
        {src: markersword, alt: "an image of a stick figure with a long sword made of connected markers"},
        {src: littlebeetle, alt: "an image of a little beetle on a leaf"},
        {src: cocoapuffs, alt: "an image of a bowl of cocoa puffs"},
    ]

    const {selectedFile, setSelectedFile} = useGlobalState();

    const [page, setPage] = useState(1);

    return (
        <div className='h-dvh relative'>
            <Header/>
            <div className="text-3xl w-full p-8 flex flex-col items-center gap-4 h-4/5">
                <h1 className='text-4xl'>Choose an image</h1>
                <div className='grid grid-cols-4 grid-rows-2 gap-2'>
                    {page === 1
                        ? <>
                            {images1.map((image, index) => (
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
                            <div
                                onClick={() => setPage(2)}
                                className="absolute inset-y-0 right-0 flex-center px-4"
                            >
                                <FaChevronCircleRight className="text-6xl text-header bg-white rounded-full cursor-pointer"/>
                            </div>
                        </>
                    : page === 2 
                        ? <>
                            {images2.map((image, index) => (
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
                            <div 
                                onClick={() => setPage(1)}
                                className="absolute inset-y-0 left-0 flex-center px-4"
                            >
                                <FaChevronCircleLeft className="text-6xl text-header bg-white rounded-full cursor-pointer"/>
                            </div>
                        </>
                    : null}
                </div>
            </div>
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