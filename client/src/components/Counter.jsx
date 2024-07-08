import { useDispatch, useSelector } from "react-redux"
import { counterActions } from "../store-redux"

const Counter = () => {
    const dispatch = useDispatch()
    const counter = useSelector(state => state.counter)

    const toggleCounterHandler = (e) => {

        
    }

    const incrementHandler = () => {
        dispatch(counterActions.increment(5))
        
    }

    const decrementHandler = () => {
        dispatch(counterActions.decrement(6))
    }

    return (
        <main>
            <h1>Redux Counter</h1>
            <div>{counter}</div>
            <div>
                <button onClick={incrementHandler}>Increment</button>
                <button onClick={decrementHandler}>Decrement</button>
            </div>
            <button onClick={toggleCounterHandler}>Toggle Counter</button>

        </main>
    )
}

export default Counter