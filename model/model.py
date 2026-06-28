import networkx as nx

from database.DAO import DAO
import copy


class Model:
    def __init__(self):
        self.grafo=nx.DiGraph()
        self.idMapN={}
        self._bestC = []
        self.sommaPesi = 0

    def getDateRange(self):
        return DAO.getDateRange()
    def getCategorie(self):
        return DAO.getCategorie()
    def buildGraph(self,d_min,d_max,categoria):
        nodi=DAO.getAllNodes(categoria.category_id)
        for n in nodi:
            self.idMapN[n.product_id]=n
        self.grafo.add_nodes_from(nodi)
        self.addEdges(d_min,d_max,categoria.category_id,self.idMapN)
        return len(self.grafo.nodes),len(self.grafo.edges)
    def addEdges(self,d_min,d_max,id_cat,idMap):
        archi=DAO.getAllEdges(d_min,d_max,id_cat,idMap)
        for a in archi:
            self.grafo.add_edge(a.p1,a.p2,weight=a.peso)
    def bestProdotti(self):
        best=[]
        for n in self.grafo.nodes:
            somma=0
            for e in self.grafo.successors(n):
                somma-=self.grafo[n][e]['weight']
            for u in self.grafo.predecessors(n):
                somma+=self.grafo[u][n]['weight']
            best.append((n.product_name,somma))
        ordinati=sorted(best,key=lambda x: x[1],reverse=True)
        return ordinati[:5]

    def bestPath(self,start,end,lun):
        self._bestC=[]
        self.sommaPesi=0

        parziale=[start]
        self.ricorsione(parziale,end,lun)
        return self._bestC,self.sommaPesi

    def ricorsione(self,parziale,end,lun):
        if parziale[-1]==end and len(parziale)==lun:
            if self.calcolaPesi(parziale)>self.sommaPesi:
                self.sommaPesi=self.calcolaPesi(parziale)
                self._bestC=copy.deepcopy(parziale)
            return

        for n in self.grafo.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale,end,lun)
                parziale.pop()

    def calcolaPesi(self,parziale):
        pesi=0
        for i in range(0,len(parziale)-1):
            pesi+=self.grafo[parziale[i]][parziale[i+1]]['weight']
        return pesi
    def getNodi(self):
        return list(self.grafo.nodes())

