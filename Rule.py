# -*- coding: cp1256 -*-
## 2eme année cycle ingénieur ISAMM
## Module : Programmation Avancée
## @ 2014/2015
## Auteur :
## Binime :
## Messaoudi Takieddine
## Ferdaws Aouinti
from Fact import *
class Rule:

    ## Structure Object : Conditions : [Fact,...]
                        ##Consequences : [Fact,...]
    def __init__(self,ListConditions,ListConsequences):
        self.Conditions = []
        for i in range(len(ListConditions)):
            if ListConditions[i].isInList(self.Conditions) == False:
                self.Conditions.append(ListConditions[i])
        self.Consequences = []
        for i in range(len(ListConsequences)):
            if ListConsequences[i].isInList(self.Consequences) == False:
                self.Consequences.append(ListConsequences[i])

    ## Fact1,Fact2,.... -> Fact1,Fact2,....
    def __str__(self):
        Cd = "%s" % self.Conditions[0].get("ID")
        Cs = "%s" % self.Consequences[0].get("ID")
        for i in range(1,len(self.Conditions)):
            Cd += ",%s" % self.Conditions[i].get("ID")
        for i in range(1,len(self.Consequences)):
            Cs += ",%s" % self.Consequences[i].get("ID")
        return "%s -> %s" % (Cd,Cs)

    ## get Conditions or Consequences Or Object.__str__
    def get(self,What):
        if What == "Consequences" or What == 2 or What == "cs":
            return self.Consequences
        elif What == "Conditions" or What == 1 or What == "cd":
            return self.Conditions
        elif What == "" or What == 0:
            return self

    ## Afficher une liste de regle (pour le teste)
    @classmethod
    def show(cla,ListRules):
        for i in range(len(ListRules)):
            print ListRules[i]

    ## Afficher la liste des liste de regle separer (une condition se trouve une seul fois dans une liste)
    ## ListeRules : [[Rule,...],...] on a obtenu cette liste par la methode breakRules()        
    @classmethod
    def showPrepared(cla,ListRules):
        for i in range(len(ListRules)):
            print "\nList %s \n" % (i+1)
            for j in range(len(ListRules[i])):
                print ListRules[i][j]

    ## separer les regle d'une façon que chaque condition donne une seul variable
    ## ex si on a A,B->C,D ça devient A,B->C et A,B->D
    def breakRule(self):
        self.broken = []
        for i in range(len(self.Consequences)):
            self.broken.append(Rule(self.Conditions,[self.Consequences[i]]))
        return self.broken

    ## on applique breakRules sur une liste de regle
    @classmethod
    def breakRules(cla,ListRules):
        broken = []
        for i in range(len(ListRules)):
            ListRules[i].breakRule()
            for j in range(len(ListRules[i].broken)):
                broken.append(ListRules[i].broken[j])
        return broken

    ## teste si les condition d'une regle donnée = les condition de cette objet
    def isConditionsEqual(self,This):
        if len(self.get(1)) == len(This.get(1)):
            Found = True
            j = 0
            while Found == True and j < len(self.get(1)):
                if self.get(1)[j].isInList(This.get(1)) == False:
                    Found = False
                j+=1
            if Found == True:
                return True
        return False

    ## teste si les consequence d'une regle donnée = les consequence de cette objet
    def isConsequencesEqual(self,This):
        if len(self.get(2)) == len(This.get(2)):
            Found = True
            j = 0
            while Found == True and j < len(self.get(2)):
                if self.get(2)[j].isInList(This.get(2)) == False:
                    Found = False
                j+=1
            if Found == True:
                return True
        return False

    ## teste si une regle donnée = cette objet
    def isEqual(self,This):
        if self.isConditionsEqual(This) and self.isConsequencesEqual(This):
            return True
        return False


    ## teste si des conditions sont dans une liste
    def isConditionsInList(self,ListRules):
        for i in range(len(ListRules)):
            if len(self.get(1)) == len(ListRules[i].get(1)):
                Found = True
                j = 0
                while Found == True and j < len(self.get(1)):
                    if self.get(1)[j].isInList(ListRules[i].get(1)) == False:
                        Found = False
                    j+=1
                if Found == True:
                    return True
        return False

    def isConsequencesInList(self,ListRules):
        for i in range(len(ListRules)):
            if len(self.get(2)) == len(ListRules[i].get(2)):
                Found = True
                j = 0
                while Found == True and j < len(self.get(2)):
                    if self.get(2)[j].isInList(ListRules[i].get(2)) == False:
                        Found = False
                    j+=1
                if Found == True:
                    return True
        return False

    def isMoreConditionsInList(self,ListRules):
        Found = 0
        for i in range(len(ListRules)):
            if self.isConditionsEqual(ListRules[i]):
                Found+=1
                if Found == 2:
                    return True
        return False

    def isInList(self,ListRules):
        if self.isConsequencesInList(ListRules) and self.isConditionsInList(ListRules):
            return True
        return False

    def isMoreInList(self,ListRules):
        Found = 0
        for i in range(len(ListRules)):
            if self.isEqual(ListRules[i]):
                Found += 1
                if Found == 2:
                    return True
        return False

    def isConditionsPartOf(self,Conditions):
        for x in self.Conditions:
            if x.isInList(Conditions) == False:
                return False
        return True

    ## donne une liste des combiniason unique d'une liste d'une taille donnée n
    @classmethod
    def combinationsUniques(cla,items, n):
        if n==0:
            yield[]
        else:
            for i in xrange( len(items) - n+1 ):
                for j in Rule.combinationsUniques( items[i+1:], n-1 ):
                    yield [items[i]] + j

    @classmethod
    def getComb(cla,items,n):
        res=[]
        brokenRules = Rule.breakRules(items)
        res += Rule.combinationsUniques(brokenRules,n)
        return res

    @classmethod
    def isConditionsUnique(cla,ListRules):
        for i in range(len(ListRules)):
            if ListRules[i].isMoreConditionsInList(ListRules):
                return False
        return True


    ## filtrer la resultat de combinationUnique d'une façon qu'une condition n'existe qu'une seul fois
    ## on aura jamais dans une liste deux regle comme ça : A,B->C et A,B->D
    ## la partie A,B ne doit pas apparaitre 2 foix dans une liste de regle
    @classmethod
    def FilterUnique(cla,ListRules,n):
        Ret = []
        preparedRules = Rule.getComb(ListRules,n)
        for i in range(len(preparedRules)):
            if Rule.isConditionsUnique(preparedRules[i]):
                Ret += [preparedRules[i]]
        return Ret
