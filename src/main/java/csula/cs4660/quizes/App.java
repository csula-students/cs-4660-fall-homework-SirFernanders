package csula.cs4660.quizes;

import csula.cs4660.graphs.Node;
import csula.cs4660.graphs.searches.BFS;
import csula.cs4660.quizes.models.State;

import java.util.*;



/**
 * Here is your quiz entry point and your app
 */

public class App {
    public static void main(String[] args) {
        // to get a state, you can simply call `Client.getState with the id`
        State initialState = Client.getState("10a5461773e8fd60940a56d2e9ef7bf4").get();
        State finalState = Client.getState("e577aa79473673f6158cc73e0e5dc122").get();

        PriorityQueue<State> frontier = new PriorityQueue<>();
        Set<State> exploredSet = new HashSet<>();
        Map<State, State> parents = new HashMap<>();
        Map<State,Integer> stateAndCurrentDistValue = new HashMap<>();
        boolean found= false;
        boolean queueIsReady =false;
        int currentValue;

        State current = initialState;
        State currentChild;

        frontier.add(0,initialState);
        stateAndCurrentDistValue.put(initialState,0);

        //BFS

        Queue<State> queue = new LinkedList<>();

        queue.add(initialState);

        while (!found){
             current = queue.poll();
            exploredSet.add(current);

            // for every possible action
            for (State neighbor: Client.getState(current.getId()).get().getNeighbors()) {
                // state transition
                if (neighbor.getId().equals("e577aa79473673f6158cc73e0e5dc122")) {
                    // construct actions from endTile
                    found=true;
                }
                if (!parents.containsKey(neighbor)) {
                    parents.put(neighbor, current);
                    queue.add(neighbor);
                }
            }
        }
        System.out.println( "\nBFS Path:\n");
        printOut(parents);

        exploredSet = new HashSet<>();
        parents = new HashMap<>();
        found= false;


    ////Dijkstra
        while (!frontier.isEmpty()) {


            while(!queueIsReady){
                currentValue = stateAndCurrentDistValue.get(frontier.peekObject());
                if(frontier.peekPriority()==currentValue){
                    queueIsReady= true;
                    if(frontier.peekObject().equals(finalState)){
                        found = true;
                    }
                }
                else{
                    currentChild = frontier.peekObject();
                    frontier.getObject();
                    frontier.add(currentValue,currentChild);
                }
            }
            queueIsReady =false;
            currentValue = frontier.peekPriority();
            current = frontier.getObject();
            exploredSet.add(current);


            // for every possible action
            for (State neighbor: Client.getState(current.getId()).get().getNeighbors()) {

                    // state transition
                    if (neighbor.getId().equals("e577aa79473673f6158cc73e0e5dc122")) {
                        found = true;
                    }
                    if (!exploredSet.contains(neighbor)) {

                        if (!stateAndCurrentDistValue.containsKey(neighbor)) {
                            parents.put(neighbor, current);
                            stateAndCurrentDistValue.put(neighbor,Client.stateTransition(current.getId(), neighbor.getId()).get().getEvent().getEffect() + currentValue);
                            if (found) {
                                break;
                            }
                            frontier.add(Client.stateTransition(current.getId(), neighbor.getId()).get().getEvent().getEffect() + currentValue, neighbor);
                        }
                        else if(stateAndCurrentDistValue.get(neighbor) > Client.stateTransition(current.getId(), neighbor.getId()).get().getEvent().getEffect() + currentValue){
                            stateAndCurrentDistValue.remove(neighbor);
                            stateAndCurrentDistValue.put(neighbor,Client.stateTransition(current.getId(), neighbor.getId()).get().getEvent().getEffect() + currentValue);
                            parents.remove(neighbor);
                            parents.put(neighbor, current);

                        }
                    }

            }

            if(found){
                break;
            }

        }
        System.out.println( "\nDijkstra Path:\n");
        printOut(parents);




    }

    public static void printOut(Map<State, State> parents){


        List<String> path = new LinkedList<>();
        int totalCost=0;

        State currentState = Client.getState("e577aa79473673f6158cc73e0e5dc122").get();
        State startState = Client.getState("10a5461773e8fd60940a56d2e9ef7bf4").get();


        while(!startState.equals(currentState)){
            totalCost = totalCost + Client.stateTransition(parents.get(currentState).getId(),currentState.getId()).get().getEvent().getEffect();
            path.add("\n"+parents.get(currentState).getLocation().getName()+":" +currentState.getLocation().getName()+":"+Client.stateTransition(parents.get(currentState).getId(),currentState.getId()).get().getEvent().getEffect());
            currentState = parents.get(currentState);
        }
        Collections.reverse(path);
        Iterator iterator = path.listIterator();

        System.out.println("Total Cost :" +totalCost);
        while (iterator.hasNext()){
            System.out.println(iterator.next());
        }


    }

}



class PriorityQueue<T> {

    private java.util.PriorityQueue<IntPriorityComparableWrapper<T>> queue;

    public PriorityQueue() {
        queue = new java.util.PriorityQueue<>();
    }

    public void add( int priority, T object ) {
        queue.add( new IntPriorityComparableWrapper<T>(object, priority) );
    }

    public T getObject() {
        return (queue.poll().getObject());
    }
    public T peekObject() {
        return (queue.peek().getObject());
    }
    public int peekPriority() {
        return (queue.peek().getPriority());
    }

    public boolean isEmpty(){
        return queue.isEmpty();
    }


    /**
     * A "wrapper" to impose comparable properties on any object placed in the
     * queue.
     */

    private static class IntPriorityComparableWrapper<T>
            implements Comparable<IntPriorityComparableWrapper<T>> {

        private T object;
        private int priority;

        public IntPriorityComparableWrapper( T object, int priority ) {
            this.object = object;
            this.priority = priority;
        }

        public int compareTo( IntPriorityComparableWrapper<T> anotherObject ) {

            return anotherObject.getPriority() -this.getPriority();


        }

        public int getPriority() {
            return priority;
        }

        public T getObject() {
            return object;
        }
    }

}
