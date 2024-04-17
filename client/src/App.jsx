import { PetClass } from './PetClass';
import { Feeding, Chat } from "./pages"

export default function App() {
    return (
        <PetClass>
            <Chat />
            <Feeding />
        </PetClass>
    )
}