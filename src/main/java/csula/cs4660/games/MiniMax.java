package csula.cs4660.games;

import csula.cs4660.games.models.MiniMaxState;
import csula.cs4660.graphs.Edge;
import csula.cs4660.graphs.Graph;
import csula.cs4660.graphs.Node;
import csula.cs4660.games.models.SuperNode;

import java.util.HashMap;
import java.util.List;
import java.util.Stack;
import java.util.Map;

public class MiniMax {
    public static Node getBestMove(final Graph graph, Node root, Integer depth, Boolean max) {
        // TODO: implement minimax to retrieve best move
        // NOTE: you should mutate graph and node as you traverse and update value
        Stack<SuperNode> stack = new Stack();
        Node<MiniMaxState> currentParent= root;
        Node<MiniMaxState> currentNode;
        Node<MiniMaxState> start = root;


        SuperNode temp;
        List<Node> kids;
        Node<MiniMaxState> returnNode = root;
        final Map<Node,Node<MiniMaxState>> childOf = new HashMap<>();
        final Map<Node,Integer> nodeValue = new HashMap<>();
        Map<Node,Boolean> changed = new HashMap<>();



        //this might seem strange. To invert the current turn. This makes sense when evaluating the nodes. It is more intuitive. At least for me.
        //Let me explain. If Node says it is a max is true. It means the node above it looking for the highest value.
        //Otherwise if a node says max is false. The node above it is looking for the least value.
        max = !max;



        //add root to stack
        stack.add(new SuperNode(currentParent,0,false,max));
        nodeValue.put(currentParent ,currentParent.getData().getValue());
        changed.put(currentParent, false);

        for (int i=1; i <depth+1; i++){
            //gets current parent from stack then marks that the children of the node have been found if any exist. It is then added back to stack.
            temp = stack.pop();
            currentParent = temp.node;
            temp.kidsFound = true;
            max = !max;
            stack.add(temp);


            //for uneven graph breaks if no more children to the right
            if(graph.neighbors(currentParent)==null){

                break;
            }
            kids = graph.neighbors(currentParent);
            for (Node<MiniMaxState> n:kids){
                if (i!=depth) {
                    stack.add(new SuperNode(n, i, false, max));
                    nodeValue.put(n,n.getData().getValue());
                    childOf.put(n, currentParent);
                    changed.put(n,false);
                }
                else{
                    //the children found is set to true in order to avoid looking further in tree.
                    stack.add(new SuperNode(n,i,true, max));
                    nodeValue.put(n,n.getData().getValue());
                    childOf.put(n, currentParent);
                    changed.put(n,true);
                }
            }
        }
        //to avoid interference in loop below.
        currentParent = root;

        while (!stack.isEmpty()){



            //System.out.println("Current index: "+stack.peek().node.getData().getIndex()+"\n"+"current value :" + nodeValue.get(stack.peek().node)+"\n current changed status:"+changed.get(stack.peek().node)+"\n\n");




            //this is for when we are at the end of the stack the best choice is picked and final value in stack is poped.
            if(stack.peek().node.equals(root)){
                stack.pop();
            }
            //if a node still hasnt been checked for children it will be checked and any children found will be added to stack.
            else if (!stack.peek().kidsFound){
                temp = stack.pop();
                temp.kidsFound = true;
                currentParent = temp.node;
                kids = graph.neighbors(currentParent);
                stack.add(temp);
                for (Node<MiniMaxState> n:kids){
                    //if the child is at max depth mark its children as found.
                    if(temp.depth==(depth-1)){
                        stack.add(new SuperNode(n,depth,true,!temp.maxTurn));
                        nodeValue.put(n,n.getData().getValue());
                        changed.put(n,true);
                        childOf.put(n,currentParent);
                    }
                    else{
                        changed.put(n,false);
                        stack.add(new SuperNode(n,temp.depth+1,false, !temp.maxTurn));
                        nodeValue.put(n,n.getData().getValue());
                        childOf.put(n,currentParent);
                    }
                }
                //this is to avoid interference from parent in next else if when it loops back.
                currentParent = root;
            }
            //takes care of max turn
            else if (stack.peek().maxTurn){

                temp = stack.pop();
                currentNode = temp.node;
                //sets current parent node if parent node of of current node is different than the current node's parent.
                currentParent = childOf.get(currentNode);

                //if parent node has never been changed before
                if(!changed.get(currentParent)){
                    nodeValue.replace(currentParent,nodeValue.get(currentNode));
                    if(currentParent.equals(start)){
                        returnNode = new Node<>(new MiniMaxState(currentNode.getData().getIndex(),nodeValue.get(currentNode)));
                    }
                    changed.replace(currentParent, true);
                }
                //if parent node has a lower value than current node its value is replaced. Then it changes the value in nodeValue Map.
                else if(nodeValue.get(currentParent) < nodeValue.get(currentNode)){
                    nodeValue.replace(currentParent,nodeValue.get(currentNode));
                    if(currentParent.equals(start)){
                        returnNode = new Node<>(new MiniMaxState(currentNode.getData().getIndex(),nodeValue.get(currentNode)));
                    }

                }

            }
            //takes care of min turn
            else if(!stack.peek().maxTurn){
                temp = stack.pop();
                currentNode = temp.node;
                //sets current parent node if parent node of of current node is different than the current node's parent.
                currentParent = childOf.get(currentNode);


                if(!changed.get(currentParent)){
                    nodeValue.replace(currentParent,nodeValue.get(currentNode));
                    if(currentParent.equals(start)){
                        returnNode = new Node<>(new MiniMaxState(currentNode.getData().getIndex(),nodeValue.get(currentNode)));
                    }
                    changed.replace(currentParent, true);
                }
                //if parent node has a lower value than current node its value is replaced. Then it changes the value in nodeValue Map.
                if(nodeValue.get(currentParent) > nodeValue.get(currentNode)){
                    nodeValue.replace(currentParent,nodeValue.get(currentNode));
                    if(currentParent.equals(start)){
                        returnNode = new Node<>(new MiniMaxState(currentNode.getData().getIndex(),nodeValue.get(currentNode)));
                    }
                }

            }


        }

        nodeValue.forEach((n,v)-> {
                   Node<MiniMaxState> noder = n;
                    graph.removeNode(n);
                    graph.addNode(new Node<>(new MiniMaxState(noder.getData().getIndex(),v)));
                    if(childOf.containsKey(n)){
                        graph.addEdge(new Edge(new Node<>(new MiniMaxState(childOf.get(n).getData().getIndex(), nodeValue.get(childOf.get(n)))), new Node<>(new MiniMaxState(noder.getData().getIndex(),v)), 1));
            }

        });
        return returnNode;
    }
}

