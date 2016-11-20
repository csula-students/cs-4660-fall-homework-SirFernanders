package csula.cs4660.graphs.representations;

import csula.cs4660.games.models.MiniMaxState;
import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Node;

import java.io.File;

import java.io.FileNotFoundException;
import java.util.*;

import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;

/**
 * Object oriented representation of graph is using OOP approach to store nodes
 * and edges
 */
public class ObjectOriented implements Representation {
    private Collection<Node> nodes = new ArrayList<>();
    private Collection<Edge> edges = new ArrayList<>();

    //had to add hashmap because collection to slow when using it for a*
    private HashMap <Node, Collection<Edge>> hashyTheHashMap = new HashMap<>();

    public ObjectOriented(File file) {
        int numberOfNodes;
        String nextLine;
        String[] split;
        int placeHolder;
        Node fromNode;
        Node toNode;
        int edgeValue;
        Edge edge;

        try {
            Scanner s = new Scanner(file);
            nextLine = s.nextLine();
            numberOfNodes = Integer.parseInt(nextLine);

            //adds the nodes locally to avoid looking through the whole list everytime since we already know each value will be unique.
            for(int i=0; i<numberOfNodes;i++){
                addNode(new Node(i));
            }
            //adds edges to linked list locally to avoid looking for node list everytime.
            while(s.hasNextLine()){
                nextLine = s.nextLine();
                split = nextLine.split(":");
                placeHolder = Integer.parseInt(split[0]);
                fromNode = new Node<>(placeHolder);
                placeHolder = Integer.parseInt(split[1]);
                toNode = new Node<>(placeHolder);
                edgeValue = Integer.parseInt(split[2]);
                edge = new Edge(fromNode,toNode,edgeValue);
                addEdge(edge);
            }


        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public ObjectOriented() {

    }

    @Override
    public boolean adjacent(Node x, Node y) {
        if(nodes.contains(x)&&nodes.contains(y)) {
            Iterator<Edge> iterator = edges.iterator();
            Edge tempEdge;
            while (iterator.hasNext()) {
                tempEdge = iterator.next();
                if (tempEdge.getFrom().equals(x) && tempEdge.getTo().equals(y)) {
                    return true;
                }
            }
        }
        return false;

    }

    @Override
    public List<Node> neighbors(Node x) {
        List tempList = new LinkedList();
        if(nodes.contains(x)) {
            Iterator<Node> iterator = nodes.iterator();
            Node tempNode;
            while (iterator.hasNext()) {
                tempNode = iterator.next();
                if (adjacent(x, tempNode)) {
                    tempList.add(tempNode);
                }
            }
            return tempList;
        }

        return null;
    }

    @Override
    public boolean addNode(Node x) {
        if(hashyTheHashMap.containsKey(x)){
            return false;
        }
        nodes.add(x);
        hashyTheHashMap.put(x, new ArrayList<>());
        return true;

    }

    @Override
    public boolean removeNode(Node x) {
        if(nodes.contains(x)) {
            Iterator<Edge> edgeIterator = edges.iterator();
            List<Edge> toRemove = new LinkedList<>();
            Edge tempEdge;
            nodes.remove(x);
            hashyTheHashMap.remove(x);
            while (edgeIterator.hasNext()) {
                tempEdge = edgeIterator.next();
                if (tempEdge.getTo().equals(x) || tempEdge.getFrom().equals(x)) {
                        toRemove.add(tempEdge);
                }
            }

            toRemove.forEach(edge -> {
                removeEdge(edge);
            });
            return true;
        }
        return false;
    }

    @Override
    public boolean addEdge(Edge x) {

        if(hashyTheHashMap.containsKey(x.getFrom()) && hashyTheHashMap.containsKey(x.getTo())){
            Collection<Edge> temp = hashyTheHashMap.get(x.getFrom());
            for(Edge e:temp){
                if(e.equals(x)){
                    return false;
                }
            }
            edges.add(x);
            temp.add(x);
            hashyTheHashMap.put(x.getFrom(), temp);
            return true;
        }
        return false;
    }

    @Override
    public boolean removeEdge(Edge x) {

        return edges.remove(x);
    }

    @Override
    public int distance(Node from, Node to) {
        if(nodes.contains(from)&&nodes.contains(to)) {
            Edge tempEdge;
            Iterator<Edge> iterator = edges.iterator();
            while (iterator.hasNext()) {
                tempEdge = iterator.next();
                if (tempEdge.getFrom().equals(from) && tempEdge.getTo().equals(to)) {
                    return tempEdge.getValue();

                }
            }
        }
        return 0;
    }

    @Override
    public Optional<Node> getNode(int index) {
        return null;
    }

    @Override
    public Optional<Node> getNode(Node node) {
        Iterator<Node> iterator = nodes.iterator();
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
