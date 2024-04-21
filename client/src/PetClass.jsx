import { createContext, useEffect, useState, useContext } from 'react';

// Create a context
const GlobalStateContext = createContext();

// Custom hook to access the global state
export const useGlobalState = () => useContext(GlobalStateContext);

// Provider component to wrap your app and provide the global state
export const PetClass = ({ children }) => {

  const [name, setName] = useState("");
  
  const [competitive, setCompetitive] = useState(false);
  const [cheerful, setCheerful] = useState(true);
  const [talkative, setTalkative] = useState(true);

  const [quicklyHungry, setQuicklyHungry] = useState(false);

  const [happiness, setHappiness] = useState(6);
  const [hunger, setHunger] = useState(5);
  const [likesSweet, setLikesSweet] = useState(false);


  const [count, setCount] = useState(0);

  var time = 30000;

  if (quicklyHungry){
    time = 20000;
  };

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
      name, setName,
      competitive, setCompetitive,
      cheerful, setCheerful,
      talkative, setTalkative,
      quicklyHungry, setQuicklyHungry,
      happiness, setHappiness, 
      hunger, setHunger, 
      likesSweet, setLikesSweet 
      }}>
      {children}
    </GlobalStateContext.Provider>
  );
};