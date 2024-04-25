import { motion } from "framer-motion";
import { Link } from "wouter";
import { useEffect, useState} from 'react';
import { useGlobalState } from '../PetClass';

export default function HomePage() {

    const {happiness, hunger} = useGlobalState();

    const pet = JSON.parse(localStorage.getItem("currPet"));

    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1,
                delayChildren: 0.2,
            },
        },
    }

    const titleLetter = {
        hidden: { scale: 0, top: 100 },
        show: { scale: 1, top: 30 },
    }

    const aiLetter = {
        hidden: { scale: 0, top: 100 },
        show: { scale: [0, 1.1, 1], top: [100,  30, 30] },
    }

    return (
        <>
            <div className="h-dvh flex-center flex-col gap-8 relative">
                <motion.div 
                    variants={container}
                    initial="hidden"
                    animate="show"
                    className="text-9xl text-yellow-300 font-bold antialiased flex-center">
                        <motion.span variants={titleLetter} className="font-title">F</motion.span>
                        <motion.span variants={titleLetter} className="font-title">a</motion.span>
                        <motion.span variants={titleLetter} className="font-title">n</motion.span>
                        <motion.span variants={titleLetter} className="font-title">t</motion.span>
                        <motion.span variants={titleLetter} className="font-title">a</motion.span>
                        <motion.span variants={titleLetter} className="font-title">s</motion.span> 
                        <motion.span variants={aiLetter} className="font-mono text-title tracking-tighter">
                            AI
                        </motion.span>
                </motion.div>
                <div className="flex gap-8">
                    <Link href="/petgen">
                        <button className="text-4xl py-4 px-8">Generate a Pet</button>
                    </Link>
                    <Link href="/chat">
                        <button className="text-4xl py-4 px-8">Chat</button>
                    </Link>
                    <Link href="/feeding">
                        <button className="text-4xl py-4 px-8">Feeding </button>
                    </Link>
                    <Link href="/game">
                        <button className="text-4xl py-4 px-8">Games</button>
                    </Link>
                </div>
                {pet && 
                <div className="absolute bottom-0 bg-header rounded-lg w-3/4 h-1/4 mb-8 flex">
                    <img className="h-full rounded-l-lg border-r-2" src={localStorage.getItem("currImg")}/>
                    <div className="w-full text-left p-8">
                        <div className="flex gap-8">
                            <p className="font-bold text-2xl text-yellow-300">{pet.identity.name}</p>
                            <p className="font-bold text-2xl text-yellow-300">Hunger: {hunger}</p>
                            <p className="font-bold text-2xl text-yellow-300">Happiness: {happiness}</p>
                        </div>
                        <p>{pet.identity.full_description}</p>
                        {hunger > 10 
                            ? <p className="text-xl">
                                {pet.identity.name} is feeling hungry!
                            </p> 
                            : ""}
                    </div>
                </div>
                }
                
                
            </div>
            
        </>
    );
}