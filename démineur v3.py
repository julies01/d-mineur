import time
import sqlite3
import pwinput
import random

#________________________________________________________________________
#__________________________________________________________________________

class Joueur :

   def __init__(self,pseudo):
         self.pseudo = pseudo
         self.msf = 0
         self.msm = 0
         self.msd = 0
         self.tmsf = 0
         self.tmsm = 0
         self.tmsd = 0
         self.nbp = 0
         self.ncasedeminee = 0

connexion = sqlite3.connect('demineurbd.db')
cur = connexion.cursor()

#on crée une base de donnée pour stocker les informations du joueur
cur.execute("CREATE TABLE IF NOT EXISTS demineurbd1(pseudo TEXT,mdp  TEXT, msf INT, msm INT,msd INT, tmsf TIME, tmsm TIME, tmsd TIME,nbparties INT)")


connexion.commit()
#cur.close()
#connexion.close()

#fonction qui verifie le format 
def verif_format(objet):
  while objet != 'O' and objet != 'N' :
      objet = str(input("Tu dois obligatoirement saisir 'O' ou 'N'\n"))
  return objet

#fonction d'ouevrture qui s'affiche au début du jeu 
def debut_jeu():
  print(" \n Bienvenue dans le jeu de demineur ! \n")
  qrapp = str(input("Veux-tu un rappel du principe et des règles du démineur ? Si oui, saisis 'O', sinon, saisis 'N'. \n"))
  qrapp = verif_format(qrapp)
  if qrapp == 'O' :
    afficher_regles()
  sauvegarder_progres()

#fonction qui permet d'afficher les règles du morpion
def afficher_regles ():
      print("\n Voici le principe et les règles du démineur : \n \n Le principe du démineur :\n")
      print("Le champ de mines du Démineur est représenté par une grille. Chaque case de la grille peut soit cacher une mine, soit être vide. Le but du jeu est de découvrir toutes les cases libres sans faire exploser les mines, c'est-à-dire sans cliquer sur les cases qui les dissimulent")
      print("\n Les règles du démineur : \n")
      print("Si tu choisis de déminer une case contenant une bombe tu perds, le jeu s'arrête. \nSi tu choisis de déminer une case libre et qu'au moins une de ses case avoisinantes contient une mine, alors un chiffre apparaît. \nSi en revanche toutes les cases adjacentes sont vides, une case vide est affichée et la même opération est répétée sur ces cases, et ce jusqu'à ce que la zone vide soit entièrement délimitée par des chiffres. \n")

#fonction qui demande au joueur si il veut sauvegarder ou pas son jeu 
def sauvegarder_progres() :
  global co
  co = str(input("\n Veux-tu te connecter ou créer un compte afin de sauvegarder tes progrès ? Si oui, saisis 'O', sinon, saisis 'N'.\n"))
  co = verif_format(co)
  if co == 'O' :
      choix_ci()
  else :
     global j1
     j1 = None
     LeDemineur.quefaire()
      
#fonction qui demande au joueur si il veut s'inscrire ou se connecter  
def choix_ci():
  global everco
  everco = str(input("\n Si tu as déjà un compte, saisis 'O' sinon, saisis 'N'.\n"))
  everco = verif_format(everco)
  if everco == 'O' :
      seconnecter()
  else :
      inscription()
  
#fonction qui permet au joueur de se connecter

def seconnecter():
  jpseudo  = str(input("Saisis ton pseudo : \n"))
  global lpseudo
  lpseudo = verif_exipseudo(jpseudo)
  if lpseudo != None :
    verif_mdp(lpseudo)  
  else :
    print("Ton pseudo n'est pas dans la base de donnée, peut être que tu l'as mal écris ou que tu n'as simplement pas de compte.")
    paspseudo = str(input("\n Si tu veux t'inscrire, saisis 'I', si tu veux retaper ton pseudo, saisis 'R'."))
    while paspseudo != 'I' and paspseudo != 'R' :
      paspseudo = str(input("Tu dois obligatoirement saisir 'I' ou 'R'\n"))
    if paspseudo == 'I':
       inscription()
    else :
       seconnecter()

#fonction qui vérifie si le pseudo existe dans la base de données
def verif_exipseudo(speudo) :
      cur.execute("SELECT pseudo FROM demineurbd1")
      connexion.commit()
      listepseudo = cur.fetchall()
      if (speudo,) in listepseudo :
        return speudo
      else :
        return None
      
#fonction pour saisir le mot de passe
def mini_mdp(pseudo):
      cur.execute("SELECT mdp FROM demineurbd1 WHERE pseudo = ?",(pseudo,))
      connexion.commit()
      listemdp = cur.fetchall()
      jmdp = pwinput.pwinput(prompt='\n Saisis ton mot de passe :\n', mask='*')
      if listemdp[0][0] == jmdp :
        return True 
      else :
        return False
  
#fonction qui vérifie si le mot de passe est bon 
def verif_mdp(lpseudo):
   if mini_mdp(lpseudo) == True :
       print ("\n Authentification réussie ! Bienvenue " + lpseudo + " !")
       global j1
       j1 = Joueur(lpseudo)
       LeDemineur.quefaire()
   else :
       resaisirv = str(input("Mot de passe incorrect ! Tu l'as peut-être mal saisi, si tu veux le resaisir, saisis 'R', sinon saisis 'N'."))
       while resaisirv != 'N' and resaisirv != 'R' :
            resaisirv = str(input("Tu dois obligatoirement saisir 'N' ou 'R'\n"))
       if resaisirv == "R" :
          verif_mdp(lpseudo)

#fonction qui permet à l'utilisateur de s'inscrire
def inscription():
    global kpseudo
    kpseudo = str(input("Saisis un pseudo : \n "))
    mpseudo = verif_exipseudo(kpseudo)
    if mpseudo != None :
        print("Ton pseudo est déjà dans la base de données, peut être que tu as déjà un compte ou ce pseudo est déjà utilisé")
        nouveaupseudo = str(input("\n Si tu veux te connecter, saisis 'C', si tu veux retaper ton pseudo, saisis 'R'."))
        while nouveaupseudo != 'C' and nouveaupseudo != 'R' :
          nouveaupseudo = str(input("Tu dois obligatoirement saisir 'C' ou 'R'\n"))
        if nouveaupseudo == 'C':
          seconnecter()
        else : 
           inscription()
    else :
      mdp = pwinput.pwinput(prompt="\n Saisis un mot de passe d'au moins 8 caractères : \n", mask='*')
      while len(mdp) < 8 :
         mdp =  pwinput.pwinput(prompt="\n Le moSaisis un mot de passe d'au moins 8 caractères : \n", mask='*')
      donnees = (kpseudo,mdp)
      cur.execute("INSERT INTO demineurbd1(pseudo, mdp, msf, msm, msd, tmsf, tmsm, tmsd, nbparties) VALUES (?,?, 0,0,0,'00:00:00','00:00:00','00:00:00',0)",donnees) 
      connexion.commit()
      print("Tu es inscrit/ inscrite. Bienvenue " + kpseudo + " !" )
      global j1
      j1 = Joueur(kpseudo)
      LeDemineur.quefaire()

def recupdata():
   j1.msf = cur.execute("SELECT msf FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   j1.msf = cur.execute("SELECT msf FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   j1.msm = cur.execute("SELECT msm FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   j1.msd = cur.execute("SELECT msd FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   j1.tmsf = cur.execute("SELECT tmsf FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   j1.tmsm = cur.execute("SELECT tmsm FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   j1.tmsd = cur.execute("SELECT tmsd FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   j1.nbp = cur.execute("SELECT nbparties FROM demineurbd1 WHERE pseudo = ?",(j1.pseudo,))
   
    
class Case :

  def __init__(self):
    self.bombe = False
    self.deminee = False
    self.bombesautour = 0 
    self.drapeau = False
    self.affichage = '🪨  '
    
class Grille :

   def __init__(self):
        self.tableau = [[Case() for i in range(LeDemineur.nbcase)] for i in range(LeDemineur.nbcase)]
    
   def cd2(self):
      if ndiffi == 'F' :
          return 10/100
      if ndiffi == 'M':
          return 20/100
      else :
          return 40/100
  
  #explication
  # A B C 
  # D ◍ E
  # F G H


   def put_bombes(self): 
      global nbcases
      nbcases = LeDemineur.nbcase**2
      global nbbombes
      nbbombes = round(nbcases*(self.cd2()))
      #on met un certain nombre de bombes dans le tableau
      for i in range(nbbombes):
         a = random.randint(0,(LeDemineur.nbcase-1))
         b = random.randint(0,(LeDemineur.nbcase-1))
         if self.tableau[(a)][(b)].bombe == True :
            a = random.randint(0,(LeDemineur.nbcase-1))
            b = random.randint(0,(LeDemineur.nbcase-1))
            self.tableau[(a)][(b)].bombe = True
            self.tableau[(a)][(b)].bombesautour = -9
            self.bombes_autour(a,b)
         else : 
            self.tableau[(a)][(b)].bombe = True
            self.tableau[(a)][(b)].bombesautour = -9
            self.bombes_autour(a,b)


   def bombes_autour(self,c,d):
         if c-1 >= 0 and d-1 >= 0 :
            self.tableau[c-1][d-1].bombesautour +=1 
         if c-1 >= 0 :  
            self.tableau[c-1][d].bombesautour +=1 
         if c-1 >= 0 and d+1 <= LeDemineur.nbcase-1 :    
            self.tableau[c-1][d+1].bombesautour +=1 
         
         if d-1 >= 0 :   
            self.tableau[c][d-1].bombesautour += 1
         if d+1 <= LeDemineur.nbcase-1 : 
            self.tableau[c][d+1].bombesautour +=1
         
         if c+1 <= LeDemineur.nbcase-1 and d-1 >= 0 :
            self.tableau[c+1][d-1].bombesautour +=1
         if c+1 <= LeDemineur.nbcase-1 :
            self.tableau[c+1][d].bombesautour +=1
         if c+1 <= LeDemineur.nbcase-1 and d+1 <= LeDemineur.nbcase-1 :
            self.tableau[c+1][d+1].bombesautour +=1
         self.affichesolu()
      
   def affiche(self): 
      c1 = "   " 
      for i in range(LeDemineur.nbcase):
         c1 += str(i+1) + "  "
      print(c1)
      for i in range(LeDemineur.nbcase):
         l = ""
         l += str(i+1) + " "
         for j in range(LeDemineur.nbcase):
               l += str(self.tableau[i][j].affichage)
         print(l)

   def affichesolu(self): 
      global solution 
      solution = ""
      c1 = "   " 
      for i in range(LeDemineur.nbcase):
         c1 += str(i+1) + "  "
      solution += str(c1) + '\n'
      for i in range(LeDemineur.nbcase):
         l = ""
         l += str(i+1) + " "
         for j in range(LeDemineur.nbcase):
               if self.tableau[i][j].bombe == True :
                  l += "💣 "
               else :
                  l += "🪨  "
         solution += str(l) + '\n'

   def affichebombes(self): 
      c1 = "   " 
      for i in range(LeDemineur.nbcase):
         c1 += str(i+1) + "  "
      print(c1)
      for i in range(LeDemineur.nbcase):
         l = ""
         l += str(i+1) + "  "
         for j in range(LeDemineur.nbcase):
               l += str(self.tableau[i][j].bombesautour)+ "  "
         print(l)
                  
   def posicase(self):
      rep = str(input("Veux-tu mettre un drapeau ou déminer ? Si tu veux déminer saisis 'D', sinon saisis 'DR': \n"))
      while rep != 'D' and rep != 'DR' :
         rep = str(input("Tu dois obligatoirement saisir 'D' ou 'DR'\n"))
      if rep == 'D':
         global vertical
         #on vérifie que c'est le bon format
         vertical= input("Quelle case veut-tu déminer ? Saisis son numéro de colonne :\n")
         while vertical.isnumeric() == False :
            vertical = input("Quelle case veut-tu déminer ? Saisis son numéro de colonne qui doit être un chiffre ! :\n")
         vertical = int(vertical)-1
         while vertical < 0 or vertical > LeDemineur.nbcase-1 :
            vertical = int(input("Tu dois saisir un nombre entre 1 et " + str(LeDemineur.nbcase) + ". Ressaisis la coordonée :\n"))-1

         global horizontal
         #on vérifie que c'est le bon format
         horizontal = input("Quelle case veut-tu déminer ? Saisis son numéro de ligne :\n")
         while horizontal.isnumeric() == False :
            horizontal = input("Quelle case veut-tu déminer ? Saisis son numéro de ligne qui doit être un chiffre ! :\n")
         horizontal = int(horizontal)-1
         while horizontal < -1  or horizontal > LeDemineur.nbcase-1 :
            horizontal = int(input("Tu dois saisir un nombre entre 1 et " + str(LeDemineur.nbcase) + ". Ressaisis la coordonée :\n"))-1
         if nbcoup > 0 :
            self.deminer(horizontal,vertical)
         else :
            self.deminerdebut()
      else : 
         vertical= int(input("Sur quelle case veut-tu mettre un drapeau ? Saisis son numéro de colonne :\n"))-1
         horizontal = int(input("Sur quelle case veut-tu mettre un drapeau ? Saisis son numéro de ligne :\n"))-1
         self.mettre_drapeau(horizontal,vertical)
      
   def mettre_drapeau(self,horizontal,vertical):
      self.tableau[horizontal][vertical].drapeau = False
      self.tableau[horizontal][vertical].affichage = "🚩  "
      self.affiche()
      LeDemineur.suitecoups()
   
   def deminerdebut(self) :
      global nbcoup
      global horizontal
      global vertical
      if self.tableau[horizontal][vertical].bombe == True :
         self.tableau[horizontal][vertical].chorizontal = horizontal
         self.tableau[horizontal][vertical].cvertical = vertical
         nbcoup += 1
         print("Tu es tombé/e sur une bombe dès le premier coup ! On a tous le droit à une deuxième chance, voici la tienne :")
         self.posicase()
      else :
         self.deminer(horizontal,vertical)

   def deminer(self,horizontal,vertical):
      global nbcoup
      nbcoup += 1
      #si ya une bombe dans la case ça fait la fonction nb bombes
      if self.tableau[horizontal][vertical].bombe == True :
         self.esttombesurbombe()
      #si la case a une valeur supérieure à 0 pour le nombre de bombes autour on affiche la valeur 
      elif self.tableau[horizontal][vertical].bombesautour > 0 : 
         self.tableau[horizontal][vertical].deminee = True
         self.tableau[horizontal][vertical].affichage = str(self.tableau[horizontal][vertical].bombesautour) + "  "
      #si la case a une valeur égale à 0 
      else :
         self.tableau[horizontal][vertical].affichage = '   '
         global lcasevisitee
         lcasevisitee = []
         self.lesvoisins(horizontal,vertical)
      self.affiche()
      LeDemineur.suitecoups()
         
   def lesvoisins(self,horizontal,vertical):
         global lcasevisitee 
         if self.tableau[horizontal][vertical] not in lcasevisitee :
            lcasevisitee.append(self.tableau[horizontal][vertical])
            if self.tableau[horizontal][vertical].bombesautour == 0 :
               self.tableau[horizontal][vertical].affichage = "  "
               if horizontal-1 >= 0 and vertical-1 >= 0 and self.tableau[horizontal-1][vertical-1].deminee == False :
                  print('OK')
                  self.tableau[horizontal-1][vertical-1].deminee = True
                  self.lesvoisins(horizontal-1,vertical-1)

               if horizontal-1 >= 0 and self.tableau[horizontal-1][vertical].deminee == False : 
                  self.tableau[horizontal-1][vertical].deminee = True
                  self.lesvoisins(horizontal-1,vertical)

               if horizontal-1 >= 0 and vertical+1 <= LeDemineur.nbcase-1 and self.tableau[horizontal-1][vertical+1].deminee == False : 
                  self.tableau[horizontal-1][vertical+1].deminee = True   
                  self.lesvoisins(horizontal-1,vertical+1)

               if vertical-1 >= 0 and self.tableau[horizontal][vertical-1].deminee == False :
                  self.tableau[horizontal][vertical-1].deminee = True 
                  self.lesvoisins(horizontal,vertical-1)

               if vertical +1 <= LeDemineur.nbcase-1 and self.tableau[horizontal][vertical+1].deminee == False : 
                  self.tableau[horizontal][vertical+1].deminee = True  
                  self.lesvoisins(horizontal,vertical+1)

               if horizontal+1 <= LeDemineur.nbcase-1 and vertical-1 >= 0 and self.tableau[horizontal+1][vertical-1].deminee == False: 
                  self.tableau[horizontal+1][vertical-1].deminee = True
                  self.lesvoisins(horizontal+1,vertical-1)

               if horizontal+1 <= LeDemineur.nbcase-1 and self.tableau[horizontal+1][vertical].deminee == False :
                  self.tableau[horizontal+1][vertical].deminee = True
                  self.lesvoisins(horizontal+1,vertical)

               if horizontal+1 <= LeDemineur.nbcase-1 and vertical+1 <= LeDemineur.nbcase-1 and self.tableau[horizontal+1][vertical-1].deminee == False  :
                  self.tableau[horizontal+1][vertical-1].deminee = True
                  self.lesvoisins(horizontal+1,vertical-1)

            elif self.tableau[horizontal][vertical].bombe == True :
               self.tableau[horizontal][vertical].affichage = '🪨   '

            else :
               self.tableau[horizontal][vertical].affichage = str(self.tableau[horizontal][vertical].bombesautour) + "  "
      

   def esttombesurbombe(self): 
      if self.tableau[horizontal][vertical].bombe == True :
         fin_temps = time.time()
         global tempsfinal
         tempsfinal = (fin_temps - debut_temps)/60
         print("Tu es tombé sur une bombe, tu as déminé " + str(LeDemineur.nbcasedemi()) + "cases  en " + str(tempsfinal) +" min ! La partie s'arrête ici !\n")
         print("Voici la solution :\n")
         print(solution)
         j1.nbp += 1
         if co == 'O':
            LeDemineur.transfertdata()
         vrejouer = str(input("Si tu veux rejouer, saisis 'R', sinon saisis 'N'.\n"))
         while vrejouer != 'R' and vrejouer != 'N' :
            vrejouer = str(input("Tu dois obligatoirement saisir 'R' ou 'N'\n"))
         if vrejouer == 'R':
            LeDemineur.en_cours()
         else : 
            print("Merci d'avoir joué, à la prochaine !")  
            quit()       
        
class Jeu :
   
   def __init__(self):
      self.nom = 'Le démineur'
      self.nbcase = 0
   
   def quefaire(self):
      qf = str(input("\n Veux tu jouer ou voir les 10 meilleurs joueurs pour les 3 différents niveaux ? Si tu veux jouer, saisis 'J', sinon saisis 'V' :\n"))
      while qf != 'J' and qf != 'V' :
         qf = str(input("Tu dois obligatoirement saisir 'J' ou 'V'\n"))
      if qf == 'J':
         self.en_cours()
      else :
         self.voirmeilleurs()

   def quefaire2(self):
      qf = str(input("\n Si tu veux jouer, saisis 'J', sinon saisis 'N'.\n"))
      while qf != 'J' and qf != 'N' :
         qf = str(input("Tu dois obligatoirement saisir 'J' ou 'N'\n"))
      if qf == 'J':
         LeDemineur.en_cours()
      else : 
         print("Merci d'avoir joué, à la prochaine !")  
         quit()       

   def espace(self,mot):
      space = "               "
      return space[0:(len(space)-len(mot))]

   def voirmeilleurs(self):
      cur.execute("SELECT pseudo,msf FROM demineurbd1 ORDER BY msf DESC LIMIT 10")
      connexion.commit()
      mf = cur.fetchall()
      print("\n Voici le classement des joueurs au niveau facile : \n")
      for i in range (len(mf)):
         print(str(i+1) + self.espace(str(i+1)) + mf[i][0]+ self.espace((mf[i][0]))+ str(mf[i][1]))
      cur.execute("SELECT pseudo,msm FROM demineurbd1 ORDER BY msm DESC LIMIT 10")
      connexion.commit()
      mm = cur.fetchall()
      print("\n Voici le classement des joueurs au niveau moyen : \n")
      for i in range (len(mm)):
         print(str(i+1) + self.espace(str(i+1)) + mm[i][0]+ self.espace((mm[i][0]))+ str(mm[i][1]))
      cur.execute("SELECT pseudo,msd FROM demineurbd1 ORDER BY msd DESC LIMIT 10")
      connexion.commit()
      md = cur.fetchall()
      print("\n Voici le classement des joueurs au niveau difficile : \n")
      for i in range (len(md)):
         print(str(i+1) + self.espace(str(i+1)) + md[i][0]+ self.espace((md[i][0]))+ str(md[i][1]))
      self.quefaire2()

   def choix_difficulte(self):
      global ndiffi
      print("\n Il y a trois niveaux de difficulté sur ce jeu de déminneur : facile, moyen, difficile. Choisis à quelle difficulté tu veux jouer.")
      ndiffi = str(input("Saisis 'F' pour 'facile', 'M' pour 'moyen' et 'D' pour 'difficile'.\n"))
      while ndiffi != 'F' and ndiffi != 'M' and ndiffi != 'D' :
        ndiffi = str(input("Tu dois obligatoirement saisir 'F' ou 'M' ou 'D'.\n"))

   def cmbcase(self) : 
      self.nbcase = input("\n Entre la racine carrée du nombre de case que tu veux. Exemple : tu auras 64 cases si tu saisis le chiffre 8. Il faut que le chiffre saisis soit au moins égal à 3.\n")
      while self.nbcase.isnumeric() == False :
        self.nbcase = input("\n Entre la racine carrée du nombre de case que tu veux. '8' -> 64 cases. Il saisir un chiffre :\n")
      self.nbcase = int(self.nbcase)
      while self.nbcase < 3  :
         self.nbcase = input("\n Entre la racine carrée du nombre de case que tu veux. '8' -> 64 cases. Il faut que le chiffre saisis soit au moins égal à 3.\n")
   
   def en_cours(self):
      global nbcoup
      nbcoup = 0
      LeDemineur.choix_difficulte()
      LeDemineur.cmbcase()
      global grilledemineur
      grilledemineur = Grille()
      grilledemineur.put_bombes()
      grilledemineur.affiche() 
      print("\n")
      print("Voici la grille de démineur, pour désigner une case, utilise les coordonnées de celle-ci, par exemple pour désigner la première case, saisis 1 pour la verticale et 1 pour l'horizontale.")
      global debut_temps
      debut_temps = time.time()
      grilledemineur.posicase()
    
   def nbcasedemi(self):
      self.nbcasedeminee = 0
      for i in range(LeDemineur.nbcase):
         for j in range(LeDemineur.nbcase):
            if grilledemineur.tableau[i][j].deminee == True :
               self.nbcasedeminee += 1
      return self.nbcasedeminee
      
   def suitecoups(self):
      if self.nbcasedemi() == ((nbcases)-nbbombes) :
         fin_temps = time.time()
         global tempsfinal
         tempsfinal = round(((fin_temps - debut_temps)/60),2)
         if j1 != None :
            j1.ncasedeminee = self.nbcasedemi()
         print("\n Tu as gagné, félicitations tu as déminé tout le terrain en " + str(tempsfinal) +" min !\n")
         print("Voici la solution :\n")
         print(solution)
         j1.nbp += 1
         if co == 'O':
            LeDemineur.transfertdata()
         vrejouer = str(input("Si tu veux rejouer, saisis 'R', sinon saisis 'N'.\n"))
         while vrejouer != 'R' and vrejouer != 'N' :
            vrejouer = str(input("Tu dois obligatoirement saisir 'R' ou 'N'\n"))
         if vrejouer == 'R':
            LeDemineur.en_cours()
         else : 
            print("Merci d'avoir joué, à la prochaine !")  
      else : 
         grilledemineur.posicase()

   def transfertdata(self):
      if ndiffi == 'F':
         if self.nbcasedemi() > j1.msf :
            j1.msf = self.nbcasedemi()
            cur.execute("UPDATE demineurbd1 SET msf = ? WHERE pseudo = ? ",(j1.msf,j1.pseudo) )
            j1.tmsf = tempsfinal
            cur.execute("UPDATE demineurbd1 SET tmsf = ? WHERE pseudo = ? ",(j1.tmsf,j1.pseudo) )
      elif ndiffi == 'M' :
         if self.nbcasedemi() > j1.msm :
            j1.msm = self.nbcasedemi()
            cur.execute("UPDATE demineurbd1 SET msm = ? WHERE pseudo = ? ",(j1.msm,j1.pseudo) )
            j1.tmsm = tempsfinal
            cur.execute("UPDATE demineurbd1 SET tmsm = ? WHERE pseudo = ? ",(j1.tmsm,j1.pseudo) )
            connexion.commit()
      elif ndiffi == 'D':
         if self.nbcasedemi() > j1.msd :
            j1.msd = self.nbcasedemi()
            cur.execute("UPDATE demineurbd1 SET msd = ? WHERE pseudo = ? ",(j1.msd,j1.pseudo) )
            j1.tmsd = tempsfinal
            cur.execute("UPDATE demineurbd1 SET tmsd = ? WHERE pseudo = ? ",(j1.tmsd,j1.pseudo) )
      cur.execute("UPDATE demineurbd1 SET nbparties = ? WHERE pseudo = ? ",(j1.nbp,j1.pseudo))
      connexion.commit()

LeDemineur = Jeu()

debut_jeu()