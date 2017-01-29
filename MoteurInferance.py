# -*- coding: cp1252 -*-
## 2eme année cycle ingénieur ISAMM
## Module : Programmation Avancée
## @ 2014/2015
## Auteur :
## Binime :
## Messaoudi Takieddine
## Ferdaws Aouinti
from Rule import *
import os.path
import re
import copy
class MoteurInferance:
    rEString = "(.*)->(.*)"
    sepCdCs = "->"
    allowedChar = [",","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    typeChainage = ["1","2"]
    
    def __init__(self,FileName):
        self.getInput(FileName)

    def show(self):
        ##Fact.show(self.Facts)
        print "This M.I. has %s Rules " % self.NumberOfRules
        for i in self.Rules:
            print i

    ## recupere les regle du fichier
    ##structure  Object :
            ## NumberOfRules : nombre de regle
            ## InputFileName ; nom de fichier
            ## InputFile : fichier input
            ## Rules : liste de Regle
            ## Facts : liste des variables
    def getInput(self,FileName):
        if os.path.exists(FileName):
            self.InputFileName = FileName
            self.InputFile = open(self.InputFileName, "r")
            self.NumberOfRules = sum(1 for line in self.InputFile)
            self.InputFile = open(self.InputFileName, "r")
            self.getRules()
            self.getDistinctFacts()
            self.InputFile.close()
        else:
            print "Input File is absent %s" % FileName
            return None

    ## recupere la liste des regle
    def getRules(self):
        RuleCount = 1
        self.Rules = []
        while RuleCount<=self.NumberOfRules:
            CurrentRule = self.InputFile.readline()
            if self.sepCdCs not in CurrentRule:
                print "InputFile Format Error Line %s in Rule %s -> is Absent" % (RuleCount,CurrentRule)
                return None
            else:
                MatchRules = re.match(self.rEString,CurrentRule)
                Conditions = self.filterInput(MatchRules.group(1))
                Consequences = self.filterInput(MatchRules.group(2))
                if Conditions == None or Consequences == None:
                    if Conditions == None:
                        print "Rule %s in Conditions" % RuleCount
                    if Consequences == None:
                        print "Rule %s in Consequences" % RuleCount
                    print "Please Correct you file and try again"
                    exit(1)
                self.Rules.append(Rule(Conditions,Consequences))
                RuleCount+=1


    def getDistinctFacts(self):
        self.Facts = []
        for R in self.Rules:
            for Cd in R.get(1):
                if Cd.isInList(self.Facts) == False:
                    self.Facts.append(Cd)
            for Cs in R.get(2):
                if Cs.isInList(self.Facts) == False:
                    self.Facts.append(Cs)

    ## entree chaine de forme : A,B,C
    ## sortie liste de fact  [Fact(A),Fact(B),...]
    def filterInput(self,In):
        Conditions = []
        for Cd in In.split(","):
            Cd = Cd.upper()
            for x in Cd:
                if x not in self.allowedChar:
                    print "Input Format Error in \"%s\"" % (x)
                    return None
            F = Fact(Cd,"")
            if F.isInList(Conditions) == False:
                Conditions.append(F)
        return Conditions
    
    def chainageAvant(self):
        In = None
        while In == None:
            In=raw_input("Saisissez d’où vous voulez partir ?\n")
            In = self.filterInput(In)
        self.chainageAvantWithGivenConditions(In)

    def chainageAvantWithGivenString(self,Input):
        In = None
        In = self.filterInput(Input)
        self.chainageAvantWithGivenConditions(In)

    ## on cree la liste des liste de regle unique d'une seul consequence
    ## et on applique le chainage avant sur chaque sous liste
    ## le output et le output de chaque sous liste separer avec un "ou"
    def chainageAvantWithGivenConditions(self,Input):
        self.Filtered = Rule.FilterUnique(self.Rules,self.NumberOfRules)
        self.OutPutAvant = []
        Count = 0
        for x in self.Filtered:
            Start = Input[:]
            End = False
            Temp = []
            while End == False:
                Test = Start[:]
                for y in x:
                    if y.isConditionsPartOf(Start):
                        if (y.get(2)[0]).isInList(Start) == False:
                            Start.append(y.get(2)[0])
                            Temp.append(y.get(2)[0])
                if self.listToString(Test) == self.listToString(Start):
                    self.OutPutAvant.append([])
                    if Fact.isListInOutPutList(Temp,self.OutPutAvant) == False:
                        for z in Temp:
                            self.OutPutAvant[Count].append(z)
                    End = True
            Count += 1
        Full = []
        for a in range(len(self.OutPutAvant)):
            if (len(self.OutPutAvant[a]) > 0):
                Full.append(self.OutPutAvant[a])
        self.OutPutAvant = Full[:]

    def listToString(self,ListFacts):
        Ret = ""
        for i in ListFacts:
            Ret += i.get(1)
        return Ret
    
    def printOutPutAvant(self):
        print "Vous pouvez déduire : "
        Ret = ""
        for x in range(len(self.OutPutAvant)):
            if (x > 0):
                Ret += " Ou "
            for y in range(len(self.OutPutAvant[x])):
                if y > 0:
                    Ret += ",%s" % self.OutPutAvant[x][y].get(1)
                else:
                    Ret += "%s" % self.OutPutAvant[x][y].get(1)
        if Ret == "":
            Ret = "Rien"
        print Ret

    ## on applique le chainage avant sur tous les conditions des regles
    ## si le output du chainage avant de cette condition contient la variable cherche
    ## on l'affiche separer avec un "ou"
    def chainageArriere(self):
        In = None
        while In == None:
            In=raw_input("Saisissez que voulez vous avoir ?\n")
            In = self.filterInput(In)
        self.Filtered = Rule.FilterUnique(self.Rules,self.NumberOfRules)
        self.OutPutArriere = []
        Count = 0
        for x in self.Rules:
            self.chainageAvantWithGivenConditions(x.get(1))
            if Fact.isListPartOfOutPutList(In,self.OutPutAvant):
                if Fact.isListInOutPutList(x.get(1),self.OutPutArriere) == False:
                    self.OutPutArriere.append([])
                    self.OutPutArriere[Count] = x.get(1)
                    Count += 1

    def printOutPutArriere(self):
        print "Vous devez avoir : "
        Ret = ""
        for x in range(len(self.OutPutArriere)):
            if (x > 0):
                Ret += " Ou "
            for y in range(len(self.OutPutArriere[x])):
                if y > 0:
                    Ret += ",%s" % self.OutPutArriere[x][y].get(1)
                else:
                    Ret += "%s" % self.OutPutArriere[x][y].get(1)
        if Ret == "":
            Ret = "Rien"
        print Ret

In = None
print "****************** 2eme Année cycle ingénieur ******************"
print "*********************** ISAMM 2014/2014 ************************"
print "****************  Module : Programmation Avancée ***************"
print "********************* Moteur d'inférance v5.0 ******************"
print "****** Réealisé par Messaoudi Takieddine et Aounti Ferdaws *****"
while In == None:
    In = raw_input("Voulez vous faire un chainage avant ou arrière (1,2)\n")
    if In not in MoteurInferance.typeChainage:
        In = None
        print "Input Format Error! Please Choose betwenn 1 and 2"
    if In == "1":
        MI = MoteurInferance("Input.txt")
        MI.show()
        MI.chainageAvant()
        MI.printOutPutAvant()
    elif In == "2":
        MI = MoteurInferance("Input.txt")
        MI.show()
        MI.chainageArriere()
        MI.printOutPutArriere()
    In = None
