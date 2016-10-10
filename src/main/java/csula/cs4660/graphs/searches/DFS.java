package csula.cs4660.graphs.searches;

import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Graph;
import csula.cs4660.graphs.Node;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

/**
 * Depth first search
 */
public class DFS implements SearchStrategy {
    boolean done = false;
    @Override
    public List<Edge> search(Graph graph, Node source, Node dist) {

        return DFS(graph, source, dist);
    }

    private List<Edge> DFS(Graph graph, Node start, Node dist){
        List<Edge> empty = new ArrayList<>();
        int i=0;
        return DFS(graph, start,dist, empty,i);
    }
    private List<Edge> DFS(Graph graph, Node from, Node finalD, List<Edge> parents, int length){

        List<Node> neighborsOfFrom = (graph.neighbors(from));
        Iterator<Node> iteratorOfNeighbors = neighborsOfFrom.iterator();
        Node node;
        if (!neighborsOfFrom.equals("")) {
            while (iteratorOfNeighbors.hasNext()){
                if (done){
                    break;
                }
                node = iteratorOfNeighbors.next();

                if (node.equals(finalD)) {
                    parents.add(new Edge(from, finalD, graph.distance(from, finalD)));
                    done=true;
                    break;

                }
                length++;
                parents.add(new Edge(from, node, graph.distance(from,node)));
                parents = DFS(graph, node, finalD, parents,length);
                if (done){
                    break;

                }
                parents.remove(length-1);
                length--;
            }
        }
        return parents;
    }
}
