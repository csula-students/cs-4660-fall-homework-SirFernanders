package csula.cs4660.graphs.representations;


import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Node;

import java.io.File;

import java.io.FileNotFoundException;
import java.util.*;

import java.util.List;
import java.util.Optional;


/**
 * Adjacency matrix in a sense store the nodes in two dimensional array
 */
public class AdjacencyMatrix implements Representation {
    private Node[] nodes = new Node[0];
    private int[][] adjacencyMatrix = new int[0][0];
    int numberOfNodes = 0;

    public AdjacencyMatrix(File file) {


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
        Node<Integer> xInt = x;
        Node<Integer> yInt = y;
        if(adjacencyMatrix[xInt.getData()][yInt.getData()]!=0)
            return true;
        return false;
    }

    @Override
    public List<Node> neighbors(Node x) {
        int column = 0;
        int index = -1;
        for(int i = 0 ;i<nodes.length;i++){
            if(nodes[i]!=null){
                if(nodes[i].equals(x)){
                    index = i;
                    break;
                }
            }
        }
        List<Node> neighborsNodes = new ArrayList<>();
        for(int i :adjacencyMatrix[index]){
            if(i>0){
                neighborsNodes.add(nodes[column]);
            }
            column+=1;
        }
        if(neighborsNodes.contains(null)){
            neighborsNodes.remove(neighborsNodes.indexOf(null));
        }
        return neighborsNodes;
    }

    @Override
    public boolean addNode(Node x) {
        if(java.util.Arrays.asList(nodes).indexOf(x)==-1) {

            Node[] tempArray = nodes;
            nodes = new Node[nodes.length + 1];
            System.arraycopy(tempArray, 0, nodes, 0, tempArray.length);
            nodes[nodes.length-1]= x;
            int[][] tempMatrix = adjacencyMatrix;
            adjacencyMatrix = new int[nodes.length][nodes.length];
            System.arraycopy(tempMatrix,0,adjacencyMatrix,0,tempMatrix.length);


            return true;
        }
            return false;

    }

    @Override
    public boolean removeNode(Node x) {

        if(java.util.Arrays.asList(nodes).indexOf(x)==-1){
            return false;
        }


        for(int i=0;i<adjacencyMatrix.length;i++) {
            adjacencyMatrix[i][java.util.Arrays.asList(nodes).indexOf(x)]=0;
        }
        nodes[java.util.Arrays.asList(nodes).indexOf(x)]=null;
        return true;
    }

    @Override
    public boolean addEdge(Edge x) {

        try{
            Node from = x.getFrom();
            Node to = x.getTo();
            if(adjacencyMatrix[java.util.Arrays.asList(nodes).indexOf(from)][java.util.Arrays.asList(nodes).indexOf( to)]==0)
            {
                adjacencyMatrix[java.util.Arrays.asList(nodes).indexOf( from)][java.util.Arrays.asList(nodes).indexOf( to)]=x.getValue();
                return true;
            }
        }catch(Exception e){
            return false;
        }
        return false;

    }

    @Override
    public boolean removeEdge(Edge x) {

        //todo CHANGES THIS TO WORK WITH TILES TOO
        if(java.util.Arrays.asList(nodes).indexOf(x.getTo())==-1 || java.util.Arrays.asList(nodes).indexOf(x.getFrom()) == -1) {
                return false;

        }
        if(adjacencyMatrix[java.util.Arrays.asList(nodes).indexOf(x.getFrom())][java.util.Arrays.asList(nodes).indexOf(x.getTo())]==0) {
            return false;
        }
        adjacencyMatrix[java.util.Arrays.asList(nodes).indexOf(x.getFrom())][java.util.Arrays.asList(nodes).indexOf(x.getTo())]=0;
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




    //method to make parsing data easier.
    private int parseData (Node x){

        return Integer.parseInt(x.getData().toString());


    }



    @Override
    public Optional<Node> getNode(int index) {
        return null;
    }

    @Override
    public Optional<Node> getNode(Node node) {
        Iterator<Node> iterator = Arrays.asList(nodes).iterator();
        Optional<Node> result = Optional.empty();
        while (iterator.hasNext()) {
            Node next = iterator.next();
            if (next.equals(node)) {
                result = Optional.of(next);
            }
        }
        return result;
    }
}

