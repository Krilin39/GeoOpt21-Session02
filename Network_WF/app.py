from tkinter import Scale
from flask import Flask
import ghhops_server as hs
import rhino3dm as rg
import geometry as geo
import networkx as nx

app = Flask(__name__)
hops = hs.Hops(app)



@hops.component(
    "/createGraph",
    name = "Create Graph",
    inputs=[
        hs.HopsInteger("Count X", "X", "Number of node in X", hs.HopsParamAccess.ITEM, default= 5),
        hs.HopsInteger("Count Y", "Y", "Number of node in Y", hs.HopsParamAccess.ITEM, default= 5),
        hs.HopsInteger("Layout", "L", "Layout to order Nodes", hs.HopsParamAccess.ITEM, default= 5),


    ],
    outputs=[
       hs.HopsPoint("Nodes","N","List of Nodes ", hs.HopsParamAccess.LIST),
       hs.HopsCurve("Edges","E","List of Edges ", hs.HopsParamAccess.LIST)
      

    ]
)
def createGraph(X, Y, layout):

    G = geo.createGridGraph(X, Y)
    GW = geo.addRandomWeigrhs(G)

    nodes = geo.getNodes(GW, layout)
    edges = geo.getEdges(GW, layout) 

    return nodes, edges


@hops.component(
    "/GH_graph",
    name = "GH_graph",
    inputs=[
        hs.HopsPoint("Nodes", "Nodes", "List of Nodes",hs.HopsParamAccess.LIST),
        hs.HopsCurve("Edges", "Edges", "List of Edges", hs.HopsParamAccess.LIST),
        hs.HopsInteger("Layout", "Type", "Layout to order Nodes", hs.HopsParamAccess.ITEM, default= 5),
        hs.HopsInteger("Scaler", "Scaler", "Scaler", hs.HopsParamAccess.ITEM, default= 5)
    ],
    outputs=[
        hs.HopsPoint("Nodes","N","List of Nodes ", hs.HopsParamAccess.LIST),
        hs.HopsCurve("Edges","E","List of Edges ", hs.HopsParamAccess.LIST)
    ]
)

def GH_graph(nodes, edges, layout, Scaler):

    G = nx.Graph()
    nds =[]

    for node in nodes:
        G.add_node(node)
        nds.append((node.X, node.Y, node.Z))

    
    for edge in edges:
       pstart= nds.index((edge.PointAtStart.X, edge.PointAtStart.Y, edge.PointAtStart.Z))
       pend = nds.index((edge.PointAtEnd.X, edge.PointAtEnd.Y, edge.PointAtEnd.Z)) 
       G.add_edge(pstart, pend)
    
    GW = geo.addRandomWeigrhs(G)
    
    nodes = geo.getNodes(Scaler , GW, layout)
    edges = geo.getEdges(Scaler, GW, layout)

    

    return nodes, edges

if __name__== "__main__":
    app.run(debug=True)