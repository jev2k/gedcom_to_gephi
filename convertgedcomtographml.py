#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Works with Python2 and Python3
#
# It requires:
#
# - networkx package for graph handling
# - gedcompy package to parse gedcom file
#
# python -m pip install networkx
# python -m pip uninstall python-gedcom
# python -m pip install gedcompy
#
# Be careful, this package may collide with python-gedcom; uninstall python-gedcom

import networkx as nx
import os
import six
import sys
import gedcom
import tqdm

def getPassedAway(p):
    # try:
    deathinfo = p['DEAT']
        
    # if deathinfo != None and deathinfo != []:
    
    try:
        deathdate = deathinfo['DATE'].value
    except:
        deathdate = ""
    try:
        deathloc = deathinfo['PLAC'].value
    except:
        deathloc = ""
    return deathdate,deathloc 
    

def getBirth(p):
    # try:
    birthinfo = p['BIRT']
        
    # if birthinfo != None and birthinfo!= []:
        
    try:
        birthdate = birthinfo['DATE'].value
    except:
        birthdate = "UNK"
    try:
        birthloc = birthinfo['PLAC'].value
    except:
        birthloc = "UNK"
    return birthdate,birthloc 
        
def getName(ourname):
    try:
        rawName = ourname['NAME'].value
        getName = rawName.replace("/","")
    except:
        try:
            rawName = ourname['NAME'][0].value
            getName = rawName.replace("/","")
        except:
            # print("\nourname['name']=",ourname['NAME'],'\n')
            # print("item with noname")
            getName = "Nope no name"
    return getName

def getFamilyName(p):
    familyName = p.name[1]
    if familyName == 'None':
        # print(p,"p!")
        # print('\n fam name=',familyName)
        return "noFamName"
    else:
        return familyName
            
#def gedcom2gephi(gedcomFilename=str('C:/Users/vollm/Westphal.ged'), gephiFilename=None):
def gedcom2gephi(gedcomFilename='', gephiFilename=None):
    
    gedcomFilename=str('C:/Users/vollm/OneDrive/Documents\Family Tree Maker/cw2_2023-03-13.ged')
    
    #lambdas
 
    getId = lambda n: n.id[1:-1]


    print("gedcom file name",gedcomFilename)
    g = gedcom.parse(gedcomFilename)
    dg = nx.DiGraph()
    for p in tqdm.tqdm(g.individuals):
        birthdate,birthloc = getBirth(p)
        deathdate,deathloc = getPassedAway(p)
        if p.id not in dg:
            # print(getId(p),"IDNUM")
            # try:
            #     print(getId(p))
            #     print(getName(p))
            #     print(getFamilyName(p))
            # except:
            #     print('uhoh')
            dg.add_node(getId(p), label=getName(p), name=getName(p), familyName=getFamilyName(p),
                        birthdate=birthdate,birthloc=birthloc,deathdate = deathdate,deathloc = deathloc)
            # print("added a node - now up to",len(dg))
    for p in tqdm.tqdm(g.individuals):
        countnum = 0
        if p.father:
            countnum +=1
            # print(countnum)
            dg.add_edge(getId(p.father), getId(p))
        if p.mother:
            countnum +=1
            # print(countnum)
            dg.add_edge(getId(p.mother), getId(p))
    if gephiFilename is None:
        gephiFilename = os.path.splitext(gedcomFilename)[0] + '.gexf'
    nx.write_gexf(dg, gephiFilename)

if __name__ == '__main__':
    import argparse
    print("ok goin")
    parser = argparse.ArgumentParser(
        description = 'This script converts a gedcom file to a gexf file')
    pa = parser.add_argument
    pa('-g','--gedcom', type = str, default = 'my_gedcom_file.ged',
       help = 'Gedcom filename')
    pa('-o','--outputGexf', type = str, default = None,
       help='optional output name. If not provided, a filename will be generated from the gedcom filename')
    args = parser.parse_args()
    gedcom2gephi(gedcomFilename=args.gedcom, gephiFilename=args.outputGexf)