import { motion } from "framer-motion";
import { Link } from "wouter";
import { useEffect, useState} from 'react';
import { useGlobalState } from '../PetClass';

export default function HomePage() {

    const {name, setName,
        cheerful, setCheerful,
        talkative, setTalkative,
        quicklyHungry, setQuicklyHungry,
        happiness, setHappiness, 
        hunger, setHunger, 
        likesSweet, setLikesSweet} = useGlobalState();

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
            <div className="h-dvh flex-center flex-col gap-8">
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
                    <Link href="/chat">
                        <button className="text-4xl py-4 px-8">Chat</button>
                    </Link>
                    <Link href="/feeding">
                        <button className="text-4xl py-4 px-8">Feeding </button>
                    </Link>
                    <Link href="/petgen">
                        <button className="text-4xl py-4 px-8">PetGen</button>
                    </Link>
                </div>

                <div>
                    {hunger > 10 ? "Pet feeling hungry" : ""}
                </div>
                
            </div>
            
        </>
    );
}