import Header from '../components/Header';

export default function PetDetails() {

    const pet = JSON.parse(localStorage.getItem("currPet"));

    return (
        <div>
            <Header/>
            <div className="text-lg text-yellow-300 antialiased flex-center flex-col gap-8">
                <p>Img Link: {localStorage.getItem("currImg")}</p>
                <p>Pet JSON: {localStorage.getItem("currPet")}</p>
                <div className='flex flex-col'>
                    <div className='flex-center'>
                        <img className="h-[400px] w-[400px]" src={localStorage.getItem("currImg")} alt="Pet"/>
                    </div>
                    <div className='flex'>
                        <div className='w-1/2'>
                            <p className='font-bold'>Identity</p>
                            <p>Name: {pet.identity.name}</p>
                            <p>Physical Details: {pet.identity.physical_details}</p>
                            <p>Full Description: {pet.identity.full_description}</p>    
                        </div>
                        <div className='w-1/2'>
                            <p className='font-bold'>Personality</p>
                            <p>Conversation Style: {pet.personality.conversationStyle}</p>
                            {pet.personality.talkative
                                ? <p>Talktative: true</p> 
                                : <p>Talkative: false</p>}
                            <p>Voice: {pet.personality.voice}</p>
                            <p>Favorite Color: {pet.personality.fav_color}</p>
                            {pet.personality.competitive
                                ? <p>Competitive: true</p> 
                                : <p>Competitive: false</p>}
                            {pet.personality.likes_sweet
                                ? <p>Likes Sweets: true</p> 
                                : <p>Likes Sweets: false</p>}
                            {pet.personality.quickly_hungry
                                ? <p>Quickly Hungry: true</p> 
                                : <p>Quickly Hungry: false</p>}
                            
                        </div>
                    </div>
                    
                    
                </div>
            </div>
        </div>
    );
}