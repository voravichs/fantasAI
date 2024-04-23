import Header from "../../components/Header"

import './Game.css'; // Import your CSS file
import { Link } from "wouter";
import { useGlobalState } from '../../PetClass';

export default function Game(){

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
            <div className="h-dvh">
                <Header/>
                <div className="h-full flex-center flex-col gap-8">
                    <h1 className="text-5xl">Games</h1>
                    <div className="flex-center gap-8">
                        <Link href="/ttt">
                            <button className="text-4xl py-4 px-8">Tic Tac Toe</button>
                        </Link>
                        <Link href="/Connect4">
                            <button className="text-4xl py-4 px-8">Connect 4</button>
                        </Link>
                    </div>
                    
                </div>

                <div>
                    {hunger > 10 ? "Pet feeling hungry" : ""}
                </div>
                
            </div>
            
        </>
    );
}