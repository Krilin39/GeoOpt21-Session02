from ast import For
from http.client import FORBIDDEN
from flask import Flask
import ghhops_server as hs

#notice, we import another file as a library
import geometry as geo

#we also import random library to generate some randomness 
import random as r

#finally we bring rhino3dm to create rhino geometry in python
import rhino3dm as rg

app = Flask(__name__)
hops = hs.Hops(app)


@hops.component(
    "/createRandomPoints",
    name = "Create Random Points",
    inputs=[
        hs.HopsInteger("Count", "C", "Number of Random Points", hs.HopsParamAccess.ITEM, default= 10),
        hs.HopsInteger("X range of randomness", "X", "Maximum randomness in X directon", hs.HopsParamAccess.ITEM, default= 10),
        hs.HopsInteger("Y range of randomness", "Y", "Maximum randomness in Y directon", hs.HopsParamAccess.ITEM, default= 10)

    ],
    outputs=[
       hs.HopsCurve("Random Points","RP","List of generated random points ", hs.HopsParamAccess.LIST)
    ]
)
def createRandomPoints(count,rX, rY):

    randomPts = []
    for i in range(count):

        #in each itereation generate some random points
        random_x = r.uniform(-rX, rX)
        random_y = r.uniform(-rY, rY)

        #create a point with rhino3dm
        #random_pt = rg.Point3d(random_x, random_y, 0)

        p1 = rg.Point3d(random_x,random_y,0)
        p2 = rg.Point3d(10,10,10)
        #random_pt = rg.Circle()
        line = rg.LineCurve(p1, p2)

        #add point to the list   random_pt
        randomPts.append(line)

    return randomPts



@hops.component(
    "/moreRandomPoints",
    name = "More Random Points",
    inputs=[
        hs.HopsInteger("Count", "C", "Number of Random Points", hs.HopsParamAccess.ITEM, default= 10),
        hs.HopsInteger("X range of randomness", "X", "Maximum randomness in X directon", hs.HopsParamAccess.ITEM, default= 10),
        hs.HopsInteger("Y range of randomness", "Y", "Maximum randomness in Y directon", hs.HopsParamAccess.ITEM, default= 10)

    ],
    outputs=[
       hs.HopsCurve("Random Points","RP","List of generated random points ", hs.HopsParamAccess.LIST)
    ]
)
def moreRandomPoints(count,rX, rY):

    randomPts = geo.createRandomPoints(count, rX, rY)
    return randomPts



@hops.component(
    "/mid_pt",
    name = "mid_pt",
    inputs=[
        hs.HopsLine("Lines", "Lines", "Number of Random Points", hs.HopsParamAccess.ITEM),
      

    ],
    outputs=[
       hs.HopsPoint("pts","LN","mid points", hs.HopsParamAccess.LIST)
    ]

)
def Linea_f(linea__ ):
    #ln = rg.Curve(linea__.PointAt(0.5))
    pt = linea__.PointAt(0.5)


    #Lineas_ = geo.Linea_func(linea__)
    return pt




if __name__== "__main__":
    app.run(debug=True)