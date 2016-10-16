package csula.cs4660.graphs.searches;

import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Graph;
import csula.cs4660.graphs.Node;

import java.util.*;

/**
 * Breadth first search
 */
public class BFS implements SearchStrategy {

    Node startNode;
    Node goalNode;

    @Override
    public List<Edge> search(Graph graph, Node source, Node dist) {
        //map tracks parent and child. Child is the KEY element.
        Map<Node,Node> adjacencyList = new HashMap<>();

        List<Edge> path = new ArrayList<>();
        boolean found= false;
        Node currentNode = source;
        Queue<Node> queue = new LinkedList<>();
        Node currentChild;
        Node currentParent;

        while (!found){
            if(currentNode!=null){
                List<Node> neighbors = graph.neighbors(currentNode);
                Iterator<Node> iterator = neighbors.iterator();
                while(iterator.hasNext()){
                    currentChild = iterator.next();
                    if(!adjacencyList.containsKey(currentChild)) {
                        queue.add(currentChild);
                        adjacencyList.put(currentChild, currentNode);
                        if (currentChild.equals(dist)) {
                            found = true;
                        }
                    }
                }

            }
            currentNode = queue.poll();
        }
        currentChild = dist;
        while (!currentChild.equals(source)){
            currentParent= adjacencyList.get(currentChild);
            path.add(new Edge(currentParent, currentChild, graph.distance(currentParent,currentChild)));
            currentChild = currentParent;
        }
        Collections.reverse(path);


        return path;
    }

}
