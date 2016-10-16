package csula.cs4660.graphs.searches;

import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Graph;
import csula.cs4660.graphs.Node;

import java.util.*;


/**
 * As name, dijkstra search using graph structure
 */
public class DijkstraSearch implements SearchStrategy {
    @Override
    public List<Edge> search(Graph graph, Node source, Node dist) {

        List<Edge> path = new ArrayList<>();
        PriorityQueue<Node> queue = new PriorityQueue<>();
        Map<Node,Integer> nodeDistance = new HashMap<>();
        Map<Node,Node> childAndParent = new HashMap<>();
        Node currentNode = source;
        Node currentChild;
        Node currentParent;
        Integer distance;
        Integer distanceOfCurrentQueueNode;
        boolean done =false;
        boolean queueIsReady= false;
        queue.add(0,currentNode);


        while (!done){

            List<Node> neighbors = graph.neighbors(currentNode);
            Iterator<Node> iterator = neighbors.iterator();
            while(iterator.hasNext()){
                currentChild = iterator.next();
                distanceOfCurrentQueueNode = queue.peekPriority();
                distance = graph.distance(currentNode,currentChild);
                if(!nodeDistance.containsKey(currentChild)) {
                    nodeDistance.put(currentChild, distance);
                    childAndParent.put(currentChild, currentNode);
                    queue.add((distance + distanceOfCurrentQueueNode), currentChild);
                    childAndParent.put(currentChild,currentNode);
                }
                else if (nodeDistance.get(currentChild)>distance+distanceOfCurrentQueueNode){
                    nodeDistance.remove(currentChild);
                    nodeDistance.put(currentChild,distance+distanceOfCurrentQueueNode);
                    queue.add(distance+distanceOfCurrentQueueNode,currentChild);
                    childAndParent.remove(currentChild);
                    childAndParent.put(currentChild,currentNode);
                }


            }
            queue.getObject();
            while(!queueIsReady){
                distance= nodeDistance.get(queue.peekObject());
                if(distance.equals(queue.peekPriority())){
                    queueIsReady= true;
                    if(queue.peekObject().equals(dist)){
                        done = true;
                    }
                }
                else{
                    currentChild = queue.peekObject();
                    queue.getObject();
                    queue.add(distance,currentChild);
                }
            }
            queueIsReady =false;


            currentNode = queue.peekObject();
        }




        currentChild = dist;
        while (!currentChild.equals(source)){
            currentParent= childAndParent.get(currentChild);
            path.add(new Edge(currentParent, currentChild, graph.distance(currentParent,currentChild)));
            currentChild = currentParent;
        }
        Collections.reverse(path);


        return path;
    }
}
//Found how to do this at http://stackoverflow.com/questions/4011560/priority-queue-in-java
  class PriorityQueue<T> {

    private java.util.PriorityQueue<IntPriorityComparableWrapper<T>> queue;

    public PriorityQueue() {
        queue = new java.util.PriorityQueue<IntPriorityComparableWrapper<T>>();
    }

    public void add( Integer priority, T object ) {
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
     */
    private static class IntPriorityComparableWrapper<T>
            implements Comparable<IntPriorityComparableWrapper<T>> {

        private T object;
        private Integer priority;

        public IntPriorityComparableWrapper( T object, Integer priority ) {
            this.object = object;
            this.priority = priority;
        }

        public int compareTo( IntPriorityComparableWrapper<T> anotherObject ) {
            return this.priority+1 - anotherObject.priority;
        }

        public int getPriority() {
            return priority;
        }

        public T getObject() {
            return object;
        }
    }

}

