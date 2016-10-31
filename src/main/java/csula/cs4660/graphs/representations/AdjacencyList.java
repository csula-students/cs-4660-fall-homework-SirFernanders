package csula.cs4660.graphs.representations;



import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Node;

import java.io.File;

import java.io.FileNotFoundException;
import java.util.*;
import java.util.List;

/**
 * Adjacency list is probably the most common implementation to store the unknown
 * loose graph
 *
 * TODO: please implement the method body
 */
public class AdjacencyList implements Representation {
    private Map<Node, Collection<Edge>> adjacencyList = new HashMap<>();


    public AdjacencyList(File file) {


        int numberOfNodes;
        int placeHolder;
        Node fromNode;
        Node toNode;
        int edgeValue;
        Edge edge;
        String nextLine;
        String[] split;
        Node tempNode;


        //scanner to read the file. Try & Caught to avoid a exception.
        try {
            Scanner s = new Scanner(file);
            numberOfNodes = Integer.parseInt(s.nextLine());


            //Pulls how many nodes are in the graph then initiates the map with that many.
            for (int g = 0; g < numberOfNodes; g++) {
                tempNode = new Node(g);
                //adds nodes/keys
                addNode(tempNode);

            }


            //Gets the following lines and splits them into an array then puts the information in corresponding locations
            //then calls the add edge function to add the edge to the graph
            while (s.hasNextLine()) {
                nextLine = s.nextLine();
                split = nextLine.split(":");
                placeHolder = Integer.parseInt(split[0]);
                fromNode = new Node<>(placeHolder);
                placeHolder = Integer.parseInt(split[1]);
                toNode = new Node<>(placeHolder);
                edgeValue = Integer.parseInt(split[2]);
                edge = new Edge(fromNode, toNode, edgeValue);


                //add edge/values
                addEdge(edge);
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }


    }

    public AdjacencyList() {

    }

    @Override
    public boolean adjacent(Node x, Node y) {
        if (adjacencyList.get(x).toString().contains(y.toString())){
            return true;
        }
     //   else if(adjacencyList.get(y).toString().contains(x.toString())){
     //       return true;
     //   }

        return false;
    }

    @Override
    public List<Node> neighbors(Node x) {

        List<Node> temp = new LinkedList<>() ;
        if (adjacencyList.containsKey(x)) {
            Iterator<Edge> edges = adjacencyList.get(x).iterator();
            while(edges.hasNext()){
                temp.add(edges.next().getTo());
            }
        }
        return temp;

    }

    @Override
    public boolean addNode(Node x) {
        //add key

        if (adjacencyList.get(x)==null) {
            adjacencyList.put(x, new ArrayList<>());
            return true;
        }
        else {
            return false;
        }
    }

    @Override
    public boolean removeNode(Node x) {
        //looks through every edge in the collection looking for calls to the node being removed
        //then removes any edge going to the node being removed.
        boolean g=false;
        List<Edge> stuff= new ArrayList<>();
        if(adjacencyList.containsKey(x)) {
            g=true;
            adjacencyList.remove(x);
            adjacencyList.forEach((node, edges) -> {
                if(adjacent(node,x)) {
                    adjacencyList.get(node).forEach(edge -> {
                        if (edge.getTo().equals(x)) {
                            stuff.add(edge);
                        }
                    });
                }
                    });
            /*************
            adjacencyList.remove(x);
            adjacencyList.forEach((node, edges) -> {
                adjacencyList.get(node).forEach(edge -> {
                    if (edge.getTo().equals(x)) {
                        stuff.add(edge);
                    }
                });
            });
            *******************/
        }
        stuff.forEach(edge -> {
            removeEdge(edge);
        });

        return g;
    }

    @Override
    public boolean addEdge(Edge x) {
        Edge temp;
        boolean i= false;

        if(adjacencyList.containsKey(x.getFrom())) {
            Iterator<Edge> edges = adjacencyList.get(x.getFrom()).iterator();

            while (edges.hasNext()) {
                temp = edges.next();
                if (temp.getTo().equals(x.getTo())) {
                    if (temp.getFrom().equals(x.getFrom())) {
                        i = false;
                        break;
                    }
                } else {

                    i = true;
                }

            }

            if (!edges.hasNext() || i == true) {
                adjacencyList.get(x.getFrom()).add(x);
                i = true;
            }
        }

        return i;
    }

    @Override
    public boolean removeEdge(Edge x) {
        Edge temp;
        boolean i= false;

        Iterator<Edge> edges = adjacencyList.get(x.getFrom()).iterator();

        while(edges.hasNext()) {
            temp = edges.next();
            if(temp.getTo().equals(x.getTo())){
                if(temp.getFrom().equals(x.getFrom())) {
                    i = true;
                    edges.remove();
                    break;
                }
            }
            else{
                i = false;
            }

        }



        return i;
    }


    @Override
    public int distance(Node from, Node to) {

        Edge temp;
        Iterator<Edge> edges = adjacencyList.get(from).iterator();
        while (edges.hasNext()){
            temp = edges.next();
            if(temp.getTo().equals(to)){
                return temp.getValue();
            }

        }

        return 0;
    }

    @Override
    public Optional<Node> getNode(int index) {
        return null;
    }
}
