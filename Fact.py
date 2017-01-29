# -*- coding: cp1256 -*-
## 2eme année cycle ingénieur ISAMM
## Module : Programmation Avancée
## @ 2014/2015
## Auteur :
## Binime :
## Messaoudi Takieddine
## Ferdaws Aouinti
class Fact:

    ##Object : ID,Value
    def __init__(self,Id,value):
        self.ID = Id
        self.Value = value

    ## Key or ID = Designation or Value
    def __str__(self):
        return "%s = %s" % (self.ID,self.Value)

    ## get ID or Value Or Object.__str__
    def get(self,What):
        if What == "ID" or What == 1 or What == "i":
            return self.ID
        elif What == "Value" or What == 2 or What == "v":
            return self.Value
        elif What == "" or What == 0:
            return self

    ## Afficher une list de fact
    ## Structure InPut : ListFact = [Fact("","")...]
    @classmethod
    def show(cla,ListFact):
        for i in range(len(ListFact)):
            print ListFact[i]

    ## Cherche si un ID or Key est dans une liste
    ## Structure InPut : ListFact = [Fact("","")...]
    def isIDInList(self,ListFact):
        for i in range(len(ListFact)):
            if ListFact[i].ID == self.ID:
                return True
        return False


    ## Cherche si un Value or Designation est dans une liste
    ## Structure InPut : ListFact = [Fact("","")...]
    def isValueInList(self,ListFact):
        for i in range(len(ListFact)):
            if ListFact[i].Value == self.Value:
                return True
        return False

    ## Cherche si un Fact((Key or ID) et (Value or Designation)) est dans une liste
    ## Structure InPut : ListFact = [Fact("","")...]
    def isIDAndValueInList(self,ListFact):
        for i in range(len(ListFact)):
            if ListFact[i].Value == self.Value and ListFact[i].ID == self.ID:
                return True
        return False

    ## Cherche si un Fact((Key or ID) et (Value or Designation)) or Fact(ID) est dans une liste
    ## Structure InPut : ListFact = [Fact("","")...]
    def isInList(self,ListFact):
        if self.isIDAndValueInList(ListFact):
            return True
        elif self.isIDInList(ListFact):
            return True
        else:
            return False

    ## Cherche si un ID d'un Fact donnée "This" est egal a l'ID cet instance
    ## Structure InPut : Fact("","")
    def isIDEqual(self,This):
        if self.get(1) == This.get(1):
            return True
        return False

    ## Cherche si la valeur or Designation d'un Fact donné est egal à Value de cette instance
    ## Structure InPut : Fact("","")
    def isValueEqual(self,This):
        if self.get(2) == This.get(2):
            return True
        return False


    ## Cherche un Fact Donnée est egal à cet instance
    ## Structure InPut : Fact("","")
    def isEqual(self,This):
        if self.isIDEqual(This) and self.isValueEqual(This):
            return True
        elif self.isIDEqual(This):
            return True
        return False


    ## Cherche si un Fact se trouve plusieur Fois dans une liste
    ## Structure InPut : ListFact : [Fact("","")...]
    def isMoreInList(self,ListFact):
        Found = 0
        for i in range(len(ListFact)):
            if self.isIDEqual(ListFact[i]):
                Found += 1
                if Found == 2:
                    return True
        return False


    ## Cherche si une liste de fact se trouve dans une liste de liste de fact
    ## Structure InPut : ListFact : [[Fact("","")...],...]
                       ##List : [Fact("","")...]
    @classmethod
    def isListInOutPutList(cla,List,OutPut):
        for i in range(len(OutPut)):
            if len(List) == len(OutPut[i]):
                Found = True
                j = 0
                while Found == True and j < len(List):
                    if List[j].isInList(OutPut[i]) == False:
                        Found = False
                    j+=1
                if Found == True:
                    return True
        return False

    ## Cherche si une liste de fact est une partie d'une liste dans une liste de liste de fact
    ## Structure InPut : ListFact : [[Fact("","")...],...]
                       ##List : [Fact("","")...]
    @classmethod
    def isListPartOfOutPutList(cla,List,OutPut):
        for i in range(len(OutPut)):
            Found = True
            j = 0
            while Found == True and j < len(List):
                if List[j].isInList(OutPut[i]) == False:
                    Found = False
                j+=1
            if Found == True:
                return True
        return False
