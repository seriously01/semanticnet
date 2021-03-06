#!/usr/bin/env python
import sys
import os
import argparse
from xml.dom import minidom #for parsing XML Document Object Models 
import semanticnet as sn #this is the library for creating the JSON graphs 

parser = argparse.ArgumentParser()
parser.add_argument("VCML_File", help="Ener a VCML file to convert")
parser.add_argument("outfile",help="Enter an output file name with .json extension")
args = parser.parse_args()

g=sn.Graph()

xmldoc=minidom.parse(args.VCML_File) 

mathmodel1=xmldoc.getElementsByTagName("Model")[0]

localCompounds= mathmodel1.getElementsByTagName("LocalizedCompound")

for compound in localCompounds:
    compoundName = compound.getAttribute("Name")
    compoundID = compound.getAttribute("KeyValue")
    compoundNode = g.add_node({"label":compoundName, "key val":compoundID,"type":"Compound"})
    g.set_node_attribute(compoundNode, "og:space:color", [0.640, 0.313, 0.746, 1.0])
    g.set_node_attribute(compoundNode, "og:space:icon", "shapes/hexagon")
    print("Read compound: ", compoundName)

#Now to get reactions which will be reaction nodes. Then we will link reaction and compound nodes.  It might also be good to look at reactions as nodes and species as edges  
reactions = mathmodel1.getElementsByTagName("SimpleReaction")
for reaction in reactions:
    rname = reaction.getAttribute("Name")
    rKeyVal= reaction.getAttribute("KeyValue")
    
    # save the list of reaction nodes locally for making edges 
    reactionNode = g.add_node({"label":rname, "key val":rKeyVal,"type":"Reaction"})
    g.set_node_attribute(reactionNode, "og:space:color", [1.0, 0.0, 0.0, 1.0])
    g.set_node_attribute(reactionNode, "og:space:icon", "shapes/star")
    print ("Read reaction: ",rname)

#Add edges: Go through reactions to add reactants and products as edges
#Run between reaction node and corrosponding compound nodes   
g.cache_nodes_by("label")
for reaction in reactions:
    reactants = reaction.getElementsByTagName("Reactant")  
    #for each reaction, run through the compounds in that reaction 
    reactionName = reaction.getAttribute("Name")

    
    reactionNode= g.get_nodes_by_attr("label",reactionName)
    #reactionNode ends up as a one element list where the element is a dict data type
    
    reactionNode_ID=reactionNode[0]['id']
    for compound in reactants:
        compoundName=compound.getAttribute("LocalizedCompoundRef")  
        compoundNode=g.get_nodes_by_attr("label",compoundName)
        compoundNode_ID=compoundNode[0]['id'] 
        print ("In reaction: {} added reactant: {}".format(reactionName, compoundName))
       
        g.add_edge(compoundNode_ID, reactionNode_ID)

    #Now add connetions between reaction nodes and product nodes 
    products = reaction.getElementsByTagName("Product")
    for product in products:
        productName = product.getAttribute("LocalizedCompoundRef")
        productNode = g.get_nodes_by_attr("label",productName)
        productNode_ID = productNode[0]['id'] 
        g.add_edge(productNode_ID, reactionNode_ID)
        print ("In reaction: {} added product: {}".format(reactionName,productName))
g.save_json(args.outfile)
 
 
