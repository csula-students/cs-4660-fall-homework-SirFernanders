package csula.cs4660.graphs.utils;

import csula.cs4660.games.models.Tile;
import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Graph;
import csula.cs4660.graphs.Node;
import csula.cs4660.graphs.representations.Representation;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileReader;

/**
 * A quick parser class to read different format of files
 */

public class Parser {
    static HashMap<xyDirection,Tile> tiles = new HashMap<>();

    public static Graph readRectangularGridFile(Representation.STRATEGY graphRepresentation, File file) {

        Graph graph = new Graph(Representation.of(graphRepresentation));

        BufferedReader buffer;

        List<String> lines = new ArrayList<String>();
        try{
            buffer = new BufferedReader(new FileReader(file));
            String line;
            while((line=buffer.readLine())!=null){
                lines.add(line.substring(1, line.length()-1));
            }
            lines.remove(0);
            lines.remove(lines.size()-1);
        }catch(FileNotFoundException fe){
            System.out.println("File not found.");
        }catch(IOException io){
            System.out.println("could not find IO");
        }
        for(int i = 0;i<lines.size();i++){
            int pointer = 0;
            for(int j = 0;j<lines.get(i).length()/2;j++){
                String eachTile = lines.get(i).substring(pointer, pointer+2);
                pointer+=2;
                tiles.put(new xyDirection(j, i), new Tile(j,i,eachTile));
                graph.addNode(new Node<>(new Tile(j,i,eachTile)));
            }
        }
        for(Map.Entry<xyDirection, Tile> eachTile:tiles.entrySet()){
            Tile north = getNextTile(eachTile.getValue(), 'N');
            Tile east = getNextTile(eachTile.getValue(), 'E');
            Tile west = getNextTile(eachTile.getValue(), 'W');
            Tile south = getNextTile(eachTile.getValue(), 'S');

            makeEdge(graph,eachTile.getValue(),north);
            makeEdge(graph,eachTile.getValue(),east);
            makeEdge(graph,eachTile.getValue(),west);
            makeEdge(graph,eachTile.getValue(),south);
        }
        return graph;
    }


    private static void makeEdge(Graph graph,Tile eachTile ,Tile tile) {

        if(tile!=null){
            graph.addEdge(new Edge(new Node<>(eachTile),new Node<>(tile),1));
        }
    }

    private static Tile getNextTile(Tile prevTile,Character direction) {
        Tile tile;
            if(direction.equals("N")) {
                tile = gettingTile(prevTile.getX(), prevTile.getY() - 1);
            }
            else if (direction.equals("S")) {
                tile = gettingTile(prevTile.getX(), prevTile.getY() + 1);
            }
            else if (direction.equals("E")) {
                tile = gettingTile(prevTile.getX() + 1, prevTile.getY());
            }
            else {
                tile = gettingTile(prevTile.getX() - 1, prevTile.getY());
            }


        return tile;
    }

    private static Tile gettingTile(int x, int y) {
        xyDirection xy = new xyDirection(x,y);
        return tiles.get(xy);
    }

    public static String converEdgesToAction(Collection<Edge> edges) {
        Collection<Edge> tempColl = new ArrayList<>();
        tempColl = edges;
        String direction = "";
        Edge temp = null;
        Node<Tile> from;
        Node<Tile> to;
        
        
        for(Edge each:edges) {
            from = each.getFrom();
            to = each.getTo();
            if (from.getData().getX() < to.getData().getX()) {
                direction += "E";
            } else if (from.getData().getX() > to.getData().getX()) {
                direction += "W";
            } else if (from.getData().getY() < to.getData().getY()) {
                direction += "S";
            } else {
                direction += "N";
            }

        }

        return direction;
    }
}

class xyDirection {
    final int x;
    final int y;

    public xyDirection(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + x;
        result = prime * result + y;
        return result;
    }
    @Override
    public boolean equals(Object incomming) {
        if (this == incomming) {
            return true;
        }
        if (incomming == null) {
            return false;
        }
        if (getClass() != incomming.getClass()) {
            return false;
        }
        xyDirection input  = (xyDirection) incomming;
        if (x != input.x)
            return false;
        if (y != input.y)
            return false;
        return true;
    }
}