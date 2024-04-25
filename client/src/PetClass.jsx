import { createContext, useEffect, useState, useContext } from 'react';

// Create a context
const GlobalStateContext = createContext();

// Custom hook to access the global state
export const useGlobalState = () => useContext(GlobalStateContext);

// Provider component to wrap your app and provide the global state
export const PetClass = ({ children }) => {

  // Selected File
  const [selectedFile, setSelectedFile] = useState("")

  // PetJSON
  const [pet, setPet] = useState(null);

  // name and physical
  const [name, setName] = useState("Mr Whiskers");
  const [physical, setPhysical] = useState("A colorful basketball");
  
  // preferences 
  const [favColor, setFavColor] = useState("blue");
  
  // personality
  const [competitive, setCompetitive] = useState(false);
  const [talkative, setTalkative] = useState(true);

  // conversation style
  const [voice, setVoice] = useState(0);
  const [conversationStyle, setConversationStyle] = useState("yoda"); // poetic, yoda, baby, goofy

  // preferences for feeding 
  const [quicklyHungry, setQuicklyHungry] = useState(false);
  const [likesSweet, setLikesSweet] = useState(false);

  // mood indicators 
  const [happiness, setHappiness] = useState(6);
  const [hunger, setHunger] = useState(5);

  const [count, setCount] = useState(0);

  var time = 30000;

  if (quicklyHungry){
    time = 20000;
  }

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(prevCount => prevCount + 1);
      setHunger(prevHunger => prevHunger + 1);
      setHappiness(prevHappiness => prevHappiness - 1);
    }, time);
    return () => clearInterval(interval);
  });


  return (
    <GlobalStateContext.Provider value={{ 
      selectedFile, setSelectedFile,
      name, setName,
      physical, setPhysical,
      favColor, setFavColor,
      competitive, setCompetitive,
      talkative, setTalkative,
      voice, setVoice,
      quicklyHungry, setQuicklyHungry,
      happiness, setHappiness, 
      hunger, setHunger, 
      likesSweet, setLikesSweet,
      conversationStyle, setConversationStyle
      }}>
      {children}
    </GlobalStateContext.Provider>
  );
};