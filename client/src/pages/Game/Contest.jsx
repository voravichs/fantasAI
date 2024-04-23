import Header from "../../components/Header"

import { useState, useRef, useEffect } from 'react';
import './Contest.css'; // Import your CSS file
import { useGlobalState } from '../../PetClass';
import { Link } from "wouter";

export default function Contest(){

    return (
        <>
            <div className="h-dvh">
                <Header/>
                <div className="h-full flex-center flex-col gap-8">
                    <h1 className="text-5xl">Coming Soon!</h1>                    
                </div>
                
            </div>
            
        </>
    );
}