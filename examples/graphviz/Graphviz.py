# -*- coding: ISO-8859-15 -*-
'''
version         = "0.0."
date            = "2007.01.15"
environnement   = "Windows XP"
graphic         = "écran 17 - 1152x854"
ide             = "Python Scripter V 1.7.2.6  (http://www.mmm-experts.com/)"
author          = "lespinx (http://www.pythonfrance.com/)"
'''

import pyclbr, tokenize, os, sys
from operator import itemgetter

class Graphviz_dot:
    '''
    o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
    But          Genérer le fichier parametre en entrée de Graphviz
    Paramètres   aucun
    Appelée par :
    o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
    '''
    def __init__(self):
        self.lst_ligne_code = []    #Liste du code épuré
                                    #[0]Nom_class
                                    #[1]Nom_def (appelante)
                                    #[3]Code

        self.lst_class = []         #Liste des noms de classes
                                    #[0]Nom_class

        self.lst_def = []           #Liste des noms de "def"
                                    #[0]Nom_def

        self.dic_class_def = {("", "n000", "<Main>") : []}
                                    #-Key : Liste   [0]Classe
                                    #               [1]Node
                                    #               [2]Def
                                    #-Data: Liste contenant les "node" des
                                    #       fonctions appelées

        self.dic_node = {"<Main>" : "n000"}
                                    #-Key : Classe + Def
                                    #-Data: Node
                                    
        self.node = 0               #Compteur pour incrément numéro de node
        self.lst_dot = []           #Liste des parametres pour Graphviz
        self.lst_anomalies = []     #Liste des anomalies
        
    def add_dic(self, nom_class, nom_def):
        '''
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        But            Controle d'unicité avant ajout dans le dictionnaire
        Paramètres     <nom_class> <nom_def>
        Appelée par :
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        '''
        if not self.dic_node.has_key(nom_class + nom_def):
            self.node += 1
            node = "n" + str(self.node).rjust(3,"0")
            self.dic_class_def[nom_class, node, nom_def] = []
            self.dic_node[nom_class + nom_def] = node
        
        #Stockage des noms de def
        if nom_def not in self.lst_def and nom_def != "":
            self.lst_def.append(nom_def)
        
    def anomalies(self, parm, pos, nom_class, nom_def,
                    lst_token = "", tokval = ""):
        '''
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        But            Mise en forme des anomalies
        Paramètres     
        Appelée par :
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        '''
        mot1 = str(parm) + "-ligne=" + str(pos[0]).ljust(5) + "col=" + \
                str(pos[1] + 1).ljust(3)
        if parm == 1:
            l1 = mot1 + "class=" + nom_class.ljust(20) + " def=" + \
                nom_def.ljust(20)
            self.lst_anomalies.append(l1)
            
        if parm == 2:
            l1 =  mot1 + "class=" + nom_class.ljust(20)+ " def=" \
                + nom_def.ljust(20)

            if len(lst_token) > 0:
                l2 =  ">>"+ (lst_token[-1] + "."  + tokval + "<<").ljust(26)
            else: l2 = (">>" + tokval + "<<").ljust(28)

            self.lst_anomalies.append(l1 + l2)

    def pyclbr_class_def(self, fic):
        '''
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        But            Rechercher les noms de classes, methodes et fonctions
                       dans le module Python.
        Paramètres     <fic> Nom du module à analyser(sans extension)
        Appelée par :
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        '''
        #Récupération via "pyclbr" des noms de classes, méthodes et fonctions
        dict = pyclbr.readmodule_ex(fic, [os.getcwd()])

        objs = dict.values()
        objs.sort(lambda a, b: cmp(getattr(a, 'lineno', 0),
                                   getattr(b, 'lineno', 0)))
        for obj in objs:
            
            #Sélection des objets du module(exclusion des import)
            if obj.module == fic:
                if isinstance(obj, pyclbr.Class):
                    
                    #Stockage des noms de classe
                    if obj.name not in self.lst_class:
                        self.lst_class.append(obj.name)

                    #Extraction et tri des méthodes de classe
                    methods = sorted(obj.methods.iteritems(), key=itemgetter(1))
                    
                    #Si la classe n'a pas de méthode
                    if len(methods) == 0: self.add_dic(obj.name, "")
                    else:
                        #Stockage des méthodes
                        for name, _ in methods:
                            if name != "__path__":
                                self.add_dic(obj.name, name)
                            
                #Stockage des fonctions
                elif isinstance(obj, pyclbr.Function):
                    self.add_dic("", obj.name)

    def tokenize_class_def(self, mon_module):
        '''
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        But         Epurer, stucturer et analyser le module source Python
                    résultat dans fichier: <"mon_module"_ligne_code.txt>
        Paramètres  <mon_module> Nom du module Python à analyser(avec extension)
        Appelée par :
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        '''
        #Dictionnaire des mots clés utilisés par "tokenize"
        for cle in tokenize.tok_name:
            if tokenize.tok_name[cle] == "NAME": NAME = cle
            if tokenize.tok_name[cle] == "NEWLINE": NEWLINE = cle
            if tokenize.tok_name[cle] == "ENDMARKER": ENDMARKER = cle

        nom_class = ""
        nom_def = "<Main>"
        flag_class = False          #Switch pour lecture ligne suivant "class"
        flag_def = False            #Switch pour lecture ligne suivant "def"
        pos_rupt = 0                #Gestion des fin de class, def ou <Main>
        lst_token = []              #Liste des instructions significatives
        c_bind = ""                 #Si appel par bind => [style=dotted]
        dic_instance = {}           #Stockage des instance de classes 

        fic_source = open(mon_module, "r")
        ligne_code = tokenize.generate_tokens(fic_source.readline)

        for tokcle, tokval, tokpos, _, tokcode  in ligne_code:

            if tokcle == NAME:
                if tokval == "class":
                    flag_class = True
                    nom_def = ""
                    continue

                if flag_class:
                    nom_class = tokval
                    #Ajout des classes qui n'ont pas été vues par pyclbr
                    if nom_class not in self.lst_class:
                        self.lst_class.append(nom_class)
                    flag_class = False
                    continue

                if tokval == "def":
                    pos_rupt = tokpos[1]
                    #Si "def" est en col 0, on est plus dans une classe
                    if pos_rupt == 0: nom_class = ""
                    flag_def = True
                    continue

                if flag_def:
                    nom_def = tokval
                    #Ajout des fonctions qui n'ont pas été vues par pyclbr
                    if nom_def not in self.lst_def:
                        self.add_dic(nom_class, nom_def)
                    flag_def = False
                    continue
                
#-o-o-o-o Détection rupture class ou def
                if tokpos[1] == 0:
                    nom_class = ""
                    nom_def = "<Main>"
                    
                if tokpos[1] <= pos_rupt:
                    if nom_class == "": nom_def = "<Main>"
                    else: nom_def = ""
                    
#-o-o-o-o Recherche instance de classe : Si on trouve dans le code un mot
          #contenant un nom de classe, "lst_token[-1]" est l'instance de la classe
                if tokval in self.lst_class:
                    if len(lst_token) > 0 and lst_token[-1] != "raise":
                        dic_instance.setdefault(lst_token[-1], tokval)

#-o-o-o-o Recherche appel par "bind"
                if tokval in ("bind", "bind_all", "bind_class", "bindtags",
                            "tag_bind"):
                    c_bind = " [style=dotted]"
                    
#-o-o-o-o Recherche appel fonction ou méthode
                if tokval in self.lst_def:
                    #Y-a t-il une instance de classe?
                    if len(lst_token) > 0:
                        if lst_token[-1] == "self": nomclass = nom_class
                        else: nomclass = dic_instance.get(lst_token[-1], "")
                    else: nomclass = ""
                        
                    #Récupération du node de la fonction appelante
                    if self.dic_node.has_key(nom_class + nom_def):
                        node1 = self.dic_node.get(nom_class + nom_def)
                    else:
                        if self.dic_node.has_key(tokval):
                            node1 = self.dic_node.get(tokval)
                        else: self.anomalies(1, tokpos, nom_class, nom_def)

                    #Récupération du node de la fonction appelée
                    if self.dic_node.has_key(nomclass + tokval):
                        node2 = self.dic_node.get(nomclass + tokval)

                        #Ajout de la fonction appelée à la fonction appelante
                        cle = (nom_class, node1, nom_def)
                        if self.dic_class_def.has_key(cle):
                            self.dic_class_def[cle].append(" -> " + node2 +
                                c_bind + " /*" + tokval + "*/")
                            c_bind = ""
                    else: self.anomalies(2, tokpos, nom_class, nom_def, lst_token, tokval)

#-o-o-o-o Stockage du code
                lst_token.append(tokval)
                continue

#-o-o-o-o Nouvelle ligne
            if tokcle == NEWLINE and len(lst_token) > 0:
                self.lst_ligne_code.append([nom_class, nom_def, " ".join(lst_token)])
                lst_token = []

#-o-o-o-o Dernière ligne
        if tokcle == ENDMARKER:
            self.lst_ligne_code.append([nom_class, nom_def, " ".join(lst_token)])

        fic_source.close()

    def genere_DOT(self, mon_module):
        '''
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        But         Constituer le fichier parametre en entrée de Graphviz :
                    -Constitution des blocs "Cluster"
                    -Constitution des relations appelants -> appelés
        Paramètres  <mon_module> Nom du module Python à analyser(avec extension)
        Appelée par :
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        '''
        parenthese = ""             #Parenthese fermante vide la 1ère fois
        cluster = 0                 #Incrément numéro de Cluster
        rupture = "999"             #Test de rupture sur nom de classe
        
        #Extraction dans une liste des couples key/data
        lst_items = self.dic_class_def.items()
        lst_items.sort()

        self.lst_dot.append("digraph G        {node [shape=box, fontsize=10];\n")
        self.lst_dot.append("/*Fonctions appelantes*/\n")
        
        for item in lst_items:
            nom_class = item[0][0]
            node      = item[0][1]
            nom_def   = item[0][2]

            if nom_class != rupture:
                rupture = nom_class
                
                #Si on traite la procédure principale ==> Cluster Module
                if nom_class == "":
                    self.lst_dot.append("subgraph cluster"  + str(cluster) +
                        '{label="Module ' + mon_module + '";')
                #Sinon ==> Cluster Class
                else:
                    self.lst_dot.append(parenthese)
                    parenthese = " " * 17 + "}"
                    self.lst_dot.append("subgraph cluster"  + str(cluster) +
                    '{label="Class ' + nom_class + ' ";')
                cluster += 1
                
            #Si nom_def est vide, la classe n'as pas de méthodes
            if nom_def == "":
                self.lst_dot.append(" " * 18 + node +
                    ' [label = "No def", fontcolor = red2];')
                continue
            
            #Traitement des fonctions appelantes
            if nom_def == "<Main>":
                label = ' [label = "' + nom_def + '", fontcolor = blue2];'
            else:
                label = ' [label = "' + nom_def + '"];'
            self.lst_dot.append(" " * 18 + node + label)
                
        #Traitement des fonctions appelées
        self.lst_dot.append(parenthese)
        self.lst_dot.append("\n/*Fonctions appelees*/\n")
        
        for item in lst_items:
            node = item[0][1]       #Node de la fonction appelante
            item[1].sort()          #Tri liste des nodes/fonctions appelées
            nb_appels = 1           #Nombre d'appels (occurence d'un meme node)
            occurence = ""          #Si aucune occurence le champ reste vide
            x = 0                   #Index de poste
            nb_postes = len(item[1])

            for appel in item[1]:
                if (x + 1) == nb_postes:   #Dernier poste de la liste?
                    self.lst_dot.append(" " * 18 + node + appel + occurence + ";")
                else:
                    if item[1][x] == item[1][x + 1]:
                        nb_appels += 1
                        occurence = ' [label=" ' + str(nb_appels) + ' appels",fontsize=10]'
                    else:
                        self.lst_dot.append(" " * 18 + node + appel + occurence + ";")
                        nb_appels = 1
                        occurence = ""
                x += 1
                    
        self.lst_dot.append(" " * 17 + "}")
        self.lst_dot.append(" " * 17 + "}")

    def ecriture_fichiers(self, fic, chemin_Graphviz):
        '''
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        But         Ecriture des fichiers résultat:
                    -1- Ecriture du fichier lignes code epuré (optionnel)
                    -2- Ecriture du fichier debug (optionnel)
                    -3- Ecriture du fichier parametres pour Graphviz
                    -4- Ecriture du fichier de commande Windows ".cmd"
                        (ligne de commande pour exécution de Graphviz sous Windows))

        Paramètres  <fic> Nom du module Python à analyser(sans extension)
        Appelée par :
        o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        '''
#-o-o-o-o -1-
##        fic_code = open(fic + "_ligne_code.txt", "w")
##        for ligne in self.lst_ligne_code:
##            fic_code.write(ligne[0].ljust(28) + ligne[1].ljust(28) + ligne[2] + "\n")
##        fic_code.close()
        
#-o-o-o-o -2-
##        fic_debug = open(fic + "_debug.txt", "w")
##
##        if len(self.lst_anomalies) > 0:
##            fic_debug.write("#-o-o-Liste des anomalies o-o-o-o-o-o-o-o-" + "\n")
##            fic_debug.write('erreur 1 = Ne figure pas dans "dic_node"' + "\n")
##            fic_debug.write("erreur 2 = les >>critères<< n'ont pu être détectés." + "\n")
##            fic_debug.write("\n")
##        else:
##            fic_debug.write("Aucune anomalies détectées\n")
##
##        for ligne in self.lst_anomalies:
##            fic_debug.write(ligne + "\n")
##
##        fic_debug.write("\n#-o-o-Liste des classes detectées o-o-o-o-o-o" + "\n")
##        self.lst_class.sort()
##        for ligne in self.lst_class: fic_debug.write(ligne + "\n")
##
##        fic_debug.write("\n#-o-o-Liste des fonctions detectées o-o-o-o-o" + "\n")
##        self.lst_def.sort()
##        for ligne in self.lst_def: fic_debug.write(ligne + "\n")
##
##        fic_debug.write("\n#-o-o-Liste du dictionnaire appelant/appelés " + "\n")
##        lst_dic = self.dic_class_def.items()
##        lst_dic.sort()
##        for cle, data in lst_dic:
##            fic_debug.write(("".join(cle)).ljust(32) + " ".join(data) +"\n")
##
##        fic_debug.close()
        
#-o-o-o-o -3-
        fic_dot = open(fic + "_dot.txt", "w")
        for ligne in self.lst_dot:
            fic_dot.write(ligne + "\n")
        fic_dot.close()
        
#-o-o-o-o -4-
        fic_cmd = open(fic + "_Graphviz.cmd", "w")
        #Ecriture paramètres Graphviz
        fic_cmd.write(chemin_Graphviz + "  " + fic + "_dot.txt  -Tpng -o "
            + fic + ".png \n")
        if sys.platform == "win32":
            fic_cmd.write("pause \n")
            fic_cmd.write(fic + ".png \n")   #Affichage de l'image/graphe
        fic_cmd.close()
        
        if sys.platform == "win32":
            os.system(fic + "_Graphviz.cmd") #Execute fichier commande

if __name__ == "__main__":
    try:
        mon_module = sys.argv[1]    #Appel via un script
    except:
        mon_module = "dr2xml_total.py"
        
    chemin_mon_module = "/Users/moine/Codes/MyDevel_Codes/CMIP6_DATA_SUITE/DR2XML/dr2pub_mpmoine/graphviz"
    chemin_Graphviz = "/usr/local/bin/dot"
    os.chdir(chemin_mon_module)

    C = Graphviz_dot()
    #fic = nom du module Python sans extension
    fic = mon_module[0:mon_module.find(".")]
    #Appel des fonctions
    C.pyclbr_class_def(fic)
    C.tokenize_class_def(mon_module )
    C.genere_DOT(mon_module)
    C.ecriture_fichiers(fic, chemin_Graphviz)
