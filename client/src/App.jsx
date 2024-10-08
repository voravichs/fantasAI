import { PetClass } from './PetClass';
import { Feeding, Chat, PetGen, HomePage, NoPage, Game, TTT, Connect4, ImageSelect, Contest, PetDetails} from "./pages"
import { Route, Switch } from "wouter";

export default function App() {
    return (
        <PetClass>
            <div className='overflow-hidden'>
                <Switch>
                    <Route path="/" component={HomePage} />
                    <Route path="/chat" component={Chat} />
                    <Route path="/feeding" component={Feeding}/>
                    <Route path="/petgen" component={ImageSelect}/>
                    <Route path="/petgen/generate/" component={PetGen}/>
                    <Route path="/game" component={Game}/>
                    <Route path="/ttt" component={TTT}/>
                    <Route path="/Connect4" component={Connect4}/>
                    <Route path="/Contest" component={Contest}/>
                    <Route path='/debug' component={PetDetails}/>
                    {/* Default route in a switch */}
                    <Route><NoPage/></Route>
                </Switch>    
            </div>
        </PetClass>
    )
}