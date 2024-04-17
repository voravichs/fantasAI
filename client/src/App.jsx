import { PetClass } from './PetClass';
import { Feeding, Chat, PetGen, HomePage, NoPage } from "./pages"
import { Route, Switch } from "wouter";

export default function App() {
    return (
        <PetClass>
            <div className='overflow-hidden'>
                <Switch>
                    <Route path="/" component={HomePage} />
                    <Route path="/chat" component={Chat} />
                    <Route path="/feeding" component={Feeding}/>
                    <Route path="/petgen" component={PetGen}/>
                    {/* Default route in a switch */}
                    <Route><NoPage/></Route>
                </Switch>    
            </div>
            
        </PetClass>
    )
}