import { createContext, useState, useContext } from 'react';

// Create a context
const GlobalStateContext = createContext();

// Custom hook to access the global state
export const useGlobalState = () => useContext(GlobalStateContext);

// Provider component to wrap your app and provide the global state
export const PetClass = ({ children }) => {
  const [happiness, setHappiness] = useState(6);
  const [hunger, setHunger] = useState(5);
  const [likesSweet, setLikesSweet] = useState(true);

  return (
    <GlobalStateContext.Provider value={{ hunger, setHunger, happiness, setHappiness, likesSweet, setLikesSweet }}>
      {children}
    </GlobalStateContext.Provider>
  );
};