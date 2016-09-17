package csula.cs4660.graphs.representations;

import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Node;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

/**
 * Adjacency matrix in a sense store the nodes in two dimensional array
 *
 * TODO: please fill the method body of this class
 */
public class AdjacencyMatrix implements Representation {
    private Node[] nodes;
    private int[][] adjacencyMatrix;

    public AdjacencyMatrix(File file) {

        int numberOfNodes;
        String nextLine;
        Node tempNode;
        String[] split;
        int placeHolder;
        int fromNode;
        int toNode;
        int edgeValue;


        try {
            Scanner s = new Scanner(file);
            nextLine = s.nextLine();
            numberOfNodes = Integer.parseInt(nextLine);

            //Declares a Node Array with length for initial nodes.
            nodes = new Node[numberOfNodes];

            //Declares a  2D Array with lentgh on both sides of initial nodes.
            adjacencyMatrix = new int[numberOfNodes][numberOfNodes];

            //adds nodes to array locally to avoid making a new array every time I need to add a node.
            for (int n = 0; n < numberOfNodes; n++) {
                tempNode = new Node(n);
                nodes[n] = tempNode;
            }

            //adds edges to 2D arry locally to avoid making a couple array every time I add a Edge.
            while (s.hasNextLine()) {
                nextLine = s.nextLine();
                split = nextLine.split(":");
                placeHolder = Integer.parseInt(split[0]);
                fromNode = placeHolder;
                placeHolder = Integer.parseInt(split[1]);
                toNode = placeHolder;
                edgeValue = Integer.parseInt(split[2]);
                adjacencyMatrix[fromNode][toNode] = edgeValue;


            }


        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public AdjacencyMatrix() {
    }

    @Override
    public boolean adjacent(Node x, Node y) {
        if(nodes[parseData(x)]==null||nodes[parseData(y)]==null) return false;
        if(parseData(x)>nodes.length||parseData(y)>nodes.length||adjacencyMatrix[parseData(x)][parseData(y)]==0) {
            return false;
        }
        return true;
    }

    @Override
    public List<Node> neighbors(Node x) {
        List<Node> friends = new LinkedList<>();

        for(int i=0; i < adjacencyMatrix.length; i++){
            if(adjacent(x,new Node(i))){
                friends.add(new Node(i));
            }
        }

        return friends;
    }

    @Override
    public boolean addNode(Node x) {
        if (nodes.length < parseData(x) + 1) {
            Node[] tempArray = nodes;
            nodes = new Node[parseData(x) + 1];
            System.arraycopy(tempArray, 0, nodes, 0, tempArray.length);
            nodes[Integer.parseInt(x.getData().toString())] = x;
            int[][] tempMatrix = adjacencyMatrix;
            adjacencyMatrix = new int[parseData(x)+1][parseData(x)+1];
            System.arraycopy(tempMatrix,0,adjacencyMatrix,0,tempMatrix.length);


            return true;
        }
        return false;

    }

    @Override
    public boolean removeNode(Node x) {

        if(nodes.length<parseData(x)||nodes[parseData(x)]==null){
            return false;
        }

        nodes[parseData(x)]=null;
        for(int i=0;i<adjacencyMatrix.length;i++) {
            adjacencyMatrix[i][parseData(x)]=0;
        }
        return true;
    }

    @Override
    public boolean addEdge(Edge x) {
        if(parseData(x.getFrom())+1>nodes.length||parseData(x.getTo())+1>nodes.length||adjacencyMatrix[parseData(x.getFrom())][parseData(x.getTo())]!=0) {
            return false;
        }
        else{
            adjacencyMatrix[parseData(x.getFrom())][parseData(x.getTo())]=x.getValue();
            return true;
        }
    }

    @Override
    public boolean removeEdge(Edge x) {
        if(nodes.length<parseData(x.getFrom())||nodes.length<parseData(x.getTo())||adjacencyMatrix[parseData(x.getFrom())][parseData(x.getTo())]==0) {
            return false;
        }
        adjacencyMatrix[parseData(x.getFrom())][parseData(x.getTo())]=0;
        return true;
    }

    @Override
    public int distance(Node from, Node to) {
        if(nodes.length<parseData(from)||nodes.length<parseData(to)||nodes[parseData(from)]==null||nodes[parseData(to)]==null) {
            return 0;
        }
        else{
           return adjacencyMatrix[parseData(from)][parseData(to)];
        }
    }

    @Override
    public Optional<Node> getNode(int index) {
        return null;
    }

    private int parseData (Node x){
        return Integer.parseInt(x.getData().toString());
    }

}