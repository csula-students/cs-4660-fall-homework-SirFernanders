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
        System.out.println(initialState);
        // to get an edge between state to its neighbor, you can call stateTransition
        System.out.println(Client.stateTransition(initialState.getId(), initialState.getNeighbors()[0].getId()));

        Queue<State> frontier = new LinkedList<>();
        Set<State> exploredSet = new HashSet<>();
        Map<State, State> parents = new HashMap<>();
        frontier.add(initialState);

        while (!frontier.isEmpty()) {
            State current = frontier.poll();
            exploredSet.add(current);

            // for every possible action
            for (State neighbor: Client.getState(current.getId()).get().getNeighbors()) {
                // state transition
                if (neighbor.getId().equals("e577aa79473673f6158cc73e0e5dc122")) {
                    // construct actions from endTile
                    System.out.println("found solution with depth of " + findDepth(parents, current, initialState));
                }
                if (!exploredSet.contains(neighbor)) {
                    parents.put(neighbor, current);
                    frontier.add(neighbor);
                }
            }
        }

        System.out.println("Not found solution");
    }

    public static int findDepth(Map<State, State> parents, State current, State start) {
        State c = current;
        int depth = 0;

        while (!c.equals(start)) {
            depth ++;
            System.out.println(c.getLocation().getName()+" from "+ parents.get(c).getLocation().getName());
            c = parents.get(c);
        }

        return depth;
    }
}

/**
 * Here is your quiz entry point and your app

public class App {
    public static void main(String[] args) {
        // to get a state, you can simply call `Client.getState with the id`
        State initialState = Client.getState("10a5461773e8fd60940a56d2e9ef7bf4").get();
        System.out.println(initialState);

        // to get an edge between state to its neighbor, you can call stateTransition
        System.out.println("*********************");
        System.out.println(Client.stateTransition(initialState.getId(), initialState.getNeighbors()[0].getId()));
        System.out.println("*********************");

        PriorityQueue<State> frontier = new PriorityQueue<>();
        Set<State> exploredSet = new HashSet<>();
        Map<State, State> parents = new HashMap<>();
        boolean BFSbreak= false;


        frontier.add(Client.stateTransition(initialState.getId(), initialState.getNeighbors()[0].getId()).get().getEvent().getEffect(),initialState);


        //BFS
        while (!frontier.isEmpty()) {
            State current = frontier.peekObject();
            exploredSet.add(current);
            System.out.println("*****************************");
            System.out.println(frontier.peekPriority());


            // for every possible action
            for (State neighbor: Client.getState(current.getId()).get().getNeighbors()) {
                // state transition
                if (neighbor.getId().equals("e577aa79473673f6158cc73e0e5dc122")) {
                    System.out.println("CHECK   2");
                    BFSbreak = true;
                }
                if (!exploredSet.contains(neighbor)) {
                    System.out.println(Client.stateTransition(current.getId(), neighbor.getId()).get().getEvent().getEffect()+frontier.peekPriority());
                    parents.put(neighbor, current);
                    frontier.add(Client.stateTransition(current.getId(), neighbor.getId()).get().getEvent().getEffect()+frontier.peekPriority(),neighbor);
                }
            }

            frontier.getObject();
            if(BFSbreak){
                break;
            }

        }
        System.out.println(BFSstring(parents));
        System.out.println("Not found solution");
    }
    public static String BFSstring(Map<State, State> parents){
        String output = "BFS Path: \n";

        List<String> path = new LinkedList<>();

        State currentState = Client.getState("e577aa79473673f6158cc73e0e5dc122").get();
        State startState = Client.getState("10a5461773e8fd60940a56d2e9ef7bf4").get();
        while(!startState.equals(currentState)){
           path.add("\n"+parents.get(currentState).getLocation().getName()+":" +currentState.getLocation().getName()+":"+Client.stateTransition(parents.get(currentState).getId(),currentState.getId()).get().getEvent().getEffect());
        }
        Collections.reverse(path);
        path.forEach(s -> {
            output.concat(s);
        });

        return output;
    }

    public static int findDepth(Map<State, State> parents, State current, State start) {
        State c = current;
        int depth = 0;

        while (!c.equals(start)) {
            depth ++;
            c = parents.get(c);
        }

        return depth;
    }
}



class PriorityQueue<T> {

    private java.util.PriorityQueue<IntPriorityComparableWrapper<T>> queue;

    public PriorityQueue() {
        queue = new java.util.PriorityQueue<IntPriorityComparableWrapper<T>>();
    }

    public void add( int priority, T object ) {
        queue.add( new IntPriorityComparableWrapper<T>(object, priority) );
    }

    public T getObject() {
        return (null != queue.peek())? queue.poll().getObject() : null;
    }
    public T peekObject() {
        return (null != queue.peek())? queue.peek().getObject() : null;
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

    private static class IntPriorityComparableWrapper<T>
            implements Comparable<IntPriorityComparableWrapper<T>> {

        private T object;
        private int priority;

        public IntPriorityComparableWrapper( T object, int priority ) {
            this.object = object;
            this.priority = priority;
        }

        public int compareTo( IntPriorityComparableWrapper<T> anotherObject ) {
            return anotherObject.getPriority() - this.getPriority();
        }

        public int getPriority() {
            return priority;
        }

        public T getObject() {
            return object;
        }
    }

}
 */