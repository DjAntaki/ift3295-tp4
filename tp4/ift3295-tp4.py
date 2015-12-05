#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class node:
    next_unique_id = 0

    def __init__(self,content=None,parent=None,childrens=[]):
        self.parent = parent
        self.id = node.next_unique_id
        node.next_unique_id += 1
        self.content = content
        self.childrens = childrens
        self.sequence=[]

           
    def __str__(self):
        if self.content is None:
            return str(self.id) 
        else :
            return str(self.id) + " " + str(self.content)
            
    def sankoff(self):
        if self.childrens=[]:
            pass
        else:
            sankoffList=[]
            for c in self.childrens:
                sankoffList.append(c.sankoff())
            assert len(sankoffList)==2
            sank=np.zeros(len(characters))
            for i in range(len(sank)):                
                #min_left=-1
                #definir fonction qui retourne le vecteur de transitions
                min_left=np.min(sankoffList[0]+mutations[i])            
            

class binary_tree:
    def __init__(self, newick_expr):
        self.leafs = []
        self.root = self._parse_newick(newick_expr)        
        self.reset()

    def _parse_newick(self, expr, parent=None):
        """parse a newick tree to this representation"""
        if expr[0] == '(':
            assert expr[-1] == ')',"Erreur de parentheses"
            e = node(parent=parent)
            parCount=0
            for i in range(len(expr)):
                if(parCount==1 and expr[i]==','):
                    virgPos=i
                    break
                if(expr[i]=='('):
                    parCount+=1
                elif(expr[i]==')'):
                    parCount-=1
            a = expr[1:virgPos] #Trouver la virgule du milieu et se debarasser des parentheses.
            b = expr[virgPos+1:-1]
            print('b',b)
            a,b = self._parse_newick(a,e), self._parse_newick(b,e)        
            e.childrens = [a,b]
            return e
        else :
            e = node(expr,parent)
            self.leafs.append(e)
            return e 
        
    def reset(self):
        """ Lorsque appelé, cette fonction retourne la fringe à son état initial et ne considère aucun noeud comme étant visité. """
        self.search_fringe = list(self.leafs)
        self.checked = set() 
        self.last = None
    
    def __iter__(self):
        """ """
        return self

    def __next__(self):
        return self.next
    
    def next(self):
        """ renvoit le prochain noeud, """
        if self.last is not None and self.last.parent is not None:
        
            if all(i.id in self.checked for i in self.last.parent.childrens):
                self.search_fringe.append(self.last.parent)
                
        
        if len(self.search_fringe) == 0 :
            raise StopIteration
        else :
            self.last = self.search_fringe.pop(0)
            self.checked.add(self.last.id)
            return self.last        

    def pullSequences(self):
        i=0
        sequences=[]
        for leaf in self.leafs:
            strSeq=leaf.content
            sequences.append(getSequence(strSeq,p))
        return sequences

#def getSequence(string,p) :
#    """Kescéça?"""
#	p.seek(0)	
#	seq=''
#	take=False
#	for line in p:
#		print(line)
#		if line[0]=='>':
#			if line[1:-1]==string:
#				take=True
#			else:
#				take=False
#		elif(take):
#			seq+=line[:-1]
#	return seq

newick_trees = []

def getSequence(string,p):
	p.seek(0)	
	seq=''
	take=False
	for line in p:
		print(line)
		if line[0]=='>':
			if line[1:-1]==string:
				take=True
			else:
				take=False
		elif(take):
			seq+=line[:-1]
	return seq


def getMutations():
	m = open('mutations.txt','rb')
	print(f[0])	


if __name__ == '__main__':

    import sys
    print("arguments :")
    print(sys.argv)
    f = open(sys.argv[1], 'rb')
    for line in f:

        if all([i in line for i in '(',',',')']):  
            line = line[:-3] #Stripping the line of ; and /n
            line = line.replace(' ','')

            print('aa', line)
            newick_trees.append(binary_tree(line))            
#Début du traitement des données
#    for l in newick_trees[0].leafs:
#	l.sequence=getSequence(
    print('-------ooo---------')
    for x in newick_trees[0]:
	print(x)      
    
