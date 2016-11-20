package csula.cs4660.games.models;

import csula.cs4660.graphs.Node;

/**
 * Created by SirFernanders on 11/19/16.
 */
public class SuperNode {
    public Node<MiniMaxState> node;
    public int depth;
    public boolean kidsFound;
    public boolean maxTurn;
    public SuperNode( Node<MiniMaxState> node, int depth, boolean kidsFound, boolean maxTurn) {
        this.node = node;
        this.depth = depth;
        this.kidsFound = kidsFound;
        this.maxTurn = maxTurn;

    }
}
