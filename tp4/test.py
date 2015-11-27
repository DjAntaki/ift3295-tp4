#!/usr/bin/env python
# -*- coding: utf-8 -*-

class node:
    next_unique_id = 0

    def __init__(self,content=None,parent=None,childrens=[]):
        
        if parent is not None:
            parent.childrens.append(self)
        self.parent = parent
        
        self.id = node.next_unique_id
        node.next_unique_id += 1
        self.content = content
        self.childrens = childrens


class binary_tree:
    def __init__(self, newick_expr):
        self.leafs = []
        self.root = self._parse_newick(newick_expr)        
        self.reset()

    def _parse_newick(self, expr, parent=None):
        """parse a newick tree to this representation"""
        print('i',expr)
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
	        print("a et b:")
	        print(a)
	        print(b)
            a,b = self._parse_newick(a,e), self._parse_newick(b,e)        
            return e
        else :
            e = node(expr,parent)
            self.leafs.append(e)
            return e 
        
    def reset(self):
        """ Lorsque appelé, cette fonction retourne la fringe à son état initial et ne considère aucun noeud comme étant visité. """
        self.search_fringe = self.leafs.copy()
        self.checked = set() 
    
    def __next__(self):
    """ renvoit le prochain noeud, """
        if self.last is not None :
            if all(i.id in self.checked for i in self.last.parent.childrens):
                self.search_fringe.append(self.last.parent)
                
        if len(self.search_fringe) == 0 :
            raise StopIteration
        else :
            self.last = self.search_fringe.pop(0)
            self.checked.add(self.last.id)
            yield self.last        

newick_trees = []

if __name__ == '__main__':

    import sys
    print("arguments :")
    print(sys.argv)
    f = open(sys.argv[1], 'rb')
    for line in f:
        if all(i in line for i in '(',',',')'):  
            line = line[:-2] #Stripping the line of ; and /n
            print('aa', line)
            newick_trees.append(binary_tree(line))            
            
print(newick_trees)
#    w = sys.argv[2]

