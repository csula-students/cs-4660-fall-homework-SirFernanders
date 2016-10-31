package csula.cs4660.graphs.searches;

import csula.cs4660.games.models.Tile;
import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Graph;
import csula.cs4660.graphs.Node;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

/**
 * Perform A* search
 */
public class AstarSearch implements SearchStrategy {

    List<Node<Tile>> frontier;
    List<Node<Tile>> exploredSet;
    HashMap<Node<Tile>,Edge> parent;
    HashMap<Node<Tile>,Integer> gScore;
    HashMap<Node<Tile>,Integer> fScore;
    List<Edge> path;

    public AstarSearch(){
        frontier = new ArrayList<Node<Tile>>();
        exploredSet = new ArrayList<Node<Tile>>();
        parent = new HashMap<Node<Tile>,Edge>();
        gScore = new HashMap<Node<Tile>,Integer>();
        fScore = new HashMap<Node<Tile>,Integer>();
        path = new ArrayList<Edge>();
    }
    @Override
    public List<Edge> search(Graph graph, Node source, Node dist) {
        frontier.add(source);
        gScore.put(source,0);
        fScore.put(source,heuristicCost(source,dist));
        while(!frontier.isEmpty()){
            Node<Tile> currentNode = findNodeWithLowestFScore();
            if(currentNode.equals(dist)){
                //return constructPath(currentNode);
                while(dist!=source){
                    path.add(parent.get(dist));
                    dist = parent.get(dist).getFrom();
                }
                Collections.reverse(path);
                return path;
            }
            frontier.remove(currentNode);
            exploredSet.add(currentNode);
            List<Node> neighbors = graph.neighbors(currentNode);
            for(Node<Tile> eachNeighbor:neighbors){
                if(!eachNeighbor.getData().getType().equals("##")){
                    if(exploredSet.contains(eachNeighbor)){
                        continue;
                    }
                    int tempGScore = gScore.get(currentNode) + 1;
                    if(!frontier.contains(eachNeighbor)){
                        frontier.add(eachNeighbor);
                    }
                    else if(tempGScore>=gScore.get(eachNeighbor)){
                        continue;
                    }
                    parent.put(eachNeighbor,new Edge(currentNode,eachNeighbor,1));
                    gScore.put(eachNeighbor,tempGScore);
                    fScore.put(eachNeighbor,gScore.get(eachNeighbor)+heuristicCost(eachNeighbor,dist));
                }
            }
        }
        return null;
    }
    private Node<Tile> findNodeWithLowestFScore() {
        // TODO Auto-generated method stub
        int min = fScore.get(frontier.get(0));
        int temp = min;
        Node<Tile> shortestNode = null;
        for(Node<Tile> n : frontier){
            if(fScore.containsKey(n)){
                if(fScore.get(n)<min){
                    min = fScore.get(n);
                    shortestNode = n;
                }
            }
        }
        if(temp==min){
            shortestNode = frontier.get(0);
        }
        return shortestNode;
    }
    private Node<Tile> findNodeWithLowestFScore(Node<Tile> neighbor) {
        // TODO Auto-generated method stub
        int min = fScore.get(neighbor);
        int temp = min;
        Node<Tile> shortestNode = null;
        for(Node<Tile> n : frontier){
            if(fScore.containsKey(n)){
                if(fScore.get(n)<min){
                    min = fScore.get(n);
                    shortestNode = n;
                }
            }
        }
        if(temp==min){
            shortestNode = frontier.get(0);
        }
        return shortestNode;
    }
    private int heuristicCost(Node source, Node dist) {
        // TODO Auto-generated method stub
        Tile sourceTile = (Tile)source.getData();
        Tile destTile = (Tile)dist.getData();
        int dx = Math.abs(sourceTile.getX()-destTile.getX());
        int dy = Math.abs(sourceTile.getY()-destTile.getY());
        return 1*(dx+dy);
    }

}
