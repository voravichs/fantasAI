import Header from "../../components/Header"

import './Game.css'; // Import your CSS file
import { Link } from "wouter";

export default function Game(){
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
                        <Link href="/Contest">
                            <button className="text-4xl py-4 px-8">Magic Contest</button>
                        </Link>
                    </div>
                </div>
            </div>
            
        </>
    );
}