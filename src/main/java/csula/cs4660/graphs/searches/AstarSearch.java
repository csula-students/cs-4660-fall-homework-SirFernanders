package csula.cs4660.graphs.searches;

import csula.cs4660.games.models.Tile;
import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Graph;
import csula.cs4660.graphs.Node;

import java.util.*;
import java.util.PriorityQueue;

/**
 * Perform A* search
 */
public class AstarSearch implements SearchStrategy {
    List<NodeExtended> explored = new LinkedList<>();
    Map<Node<Tile>,Node<Tile>> parent = new HashMap<>(); //Map Layout is <<Child>, <Parent>>
    List path = new ArrayList<>();


    NodeExtended current;
    NodeExtended currentChild = new NodeExtended();
    NodeExtended isInQueue = new NodeExtended();
    int tempG;


    NodeExtended start = new NodeExtended();

    Queue<NodeExtended> placeholder = new LinkedList<>();


    @Override
    public List<Edge> search(Graph graph, Node source, Node dist) {

        start.node = source;
        start.f_scores = heuristicValue(source,dist);
        start.g_scores = 1;


        java.util.PriorityQueue<NodeExtended> queue = new PriorityQueue<>(20, (i, j) -> {
            if(i.f_scores > j.f_scores){
                return 1;
            }

            else if (i.f_scores < j.f_scores){
                return -1;
            }

            else{
                return 0;
            }
        }
        );


        queue.add(start);




        while (!queue.isEmpty()){
            current = queue.poll();
            if(current.node.equals(dist)){
                break;
            }
            explored.add(current);
            List<Node> neighbors = graph.neighbors(current.node);
            Iterator<Node> iterator = neighbors.iterator();
            while(iterator.hasNext()){
                currentChild.node = iterator.next();
                if(currentChild.node.getData().getType().equals("##")){
                    System.out.println(currentChild.node);
                    if(!explored.contains(currentChild.node)) {
                        tempG = current.g_scores + 1;
                        if (!queue.contains(currentChild)) {
                            currentChild.f_scores = heuristicValue(currentChild.node, dist);
                            currentChild.g_scores = tempG;
                            parent.put(currentChild.node, current.node);
                            queue.add(currentChild);

                        }
                        else {
                            while (!queue.isEmpty()) {
                                isInQueue = queue.poll();
                                if (isInQueue.node.equals(currentChild.node)) {
                                    break;
                                } else {
                                    placeholder.add(isInQueue);
                                }
                            }
                            while (!placeholder.isEmpty()) {
                                queue.add(placeholder.poll());
                            }
                            if (tempG >= isInQueue.g_scores) {
                                isInQueue.g_scores = tempG;
                                isInQueue.f_scores = heuristicValue(isInQueue.node, dist);
                                parent.put(isInQueue.node, current.node);
                                queue.add(isInQueue);
                            }
                        }
                    }
                }
            }
            System.out.println(queue.size());
        }
        if (parent.containsKey(dist)) {
            return getPath(parent, source, dist);
        }

        return null;
    }
    private int heuristicValue(Node from, Node to){
        Tile fromTile = (Tile)from.getData();
        Tile toTile = (Tile)to.getData();
        int dx = Math.abs(fromTile.getX()-toTile.getX());
        int dy = Math.abs(fromTile.getY()-toTile.getY());
        int d = 1;

        return d*(dx+dy);
    }

    private List<Edge> getPath (Map<Node<Tile>,Node<Tile>> parents, Node<Tile> start, Node<Tile> end){
        List<Edge> path = new ArrayList<>();

        while(!end.getData().equals(start.getData())){
            path.add(new Edge(parents.get(end),end,1));
            end = parents.get(end);
        }
        Collections.reverse(path);
        return path;
    }
}

class NodeExtended {
    Node<Tile> node;
    int g_scores = 0;
    int f_scores = 0;
}

