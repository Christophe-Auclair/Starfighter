import random
from tkinter import *
from helper import *

# --------------------- VUE ------------------------- #

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.title("STARFIGHTER V 1.0")
        self.root.iconbitmap('Images\starcraft_macos_bigsur_icon_189700.ico')
        # ****** Variables texte ******
        self.text_niveau = StringVar(value="Niveau: ")
        self.text_hp = StringVar(value="HP: ")
        self.text_mines = StringVar(value="Mines: ")
        self.text_score = StringVar(value="Score: ")
        self.text_highscores = StringVar()
        bg = PhotoImage(file='Images\\Background.png', width=600, height=750)
        self.root.bg = bg  # Previent le garbage collector d'effacer l'image
        self.creercadreprincipale()

    def back(self):
        self.highscores.grid_forget()
        self.menu.grid(column=0, row=0)

    def creercadreprincipale(self):

        self.cadre = Frame(self.root)

        self.menu = LabelFrame(self.cadre, text="Menu", width=600, height=750, font=("Arial", 24))

        self.btnjouer = Button(self.menu, text="Démarrer Partie", font=("Arial", 16))
        self.btnjouer.bind("<Button-1>", self.demarrerpartie)

        self.btnscores = Button(self.menu, text="Afficher High Scores", font=("Arial", 16))
        self.btnscores.bind("<Button-1>", self.showhighscoresbutton)

        self.menu.grid(column=0, row=0)
        self.btnjouer.grid(column=0, row=0, padx=50, pady=50)
        self.btnscores.grid(column=0, row=1, padx=50, pady=50)
        self.cadre.pack()


    def demarrerpartie(self, evt):

        self.menu.destroy()
        self.canevas = Canvas(self.cadre, width=600, height=750, bg="black")
        self.canevas.grid(column=0, row=0, sticky=NW)
        self.statwindow = LabelFrame(self.cadre, text="Stats", font=("Arial", 24))
        self.stat_niveau = Label(self.statwindow, textvariable=self.text_niveau, font=("Arial", 18))
        self.stat_hp = Label(self.statwindow, textvariable=self.text_hp, font=("Arial", 18))
        self.stat_mines = Label(self.statwindow, textvariable=self.text_mines, font=("Arial", 18))
        self.stat_score = Label(self.statwindow, textvariable=self.text_score, font=("Arial", 18))

        self.statwindow.grid(column=1, row=0, ipadx=10)
        self.stat_niveau.grid(ipadx=10, ipady=10, sticky=W)
        self.stat_hp.grid(ipadx=10, ipady=10, sticky=W)
        self.stat_mines.grid(ipadx=10, ipady=10, sticky=W)
        self.stat_score.grid(ipadx=10, ipady=10, sticky=W)

        self.parent.demarrerpartie()

    def afficherpartie(self, partie):
        self.canevas.delete(ALL)

        self.text_niveau.set("Niveau: " + str(self.parent.partie.niveau))
        self.text_hp.set("HP: " + str(self.parent.partie.vaisseau.hp))
        self.text_mines.set("Mines: " + str(self.parent.partie.vaisseau.minesdisponibles))
        self.text_score.set("Score: " + str(self.parent.partie.points))
        self.canevas.create_image(0, 0, image=self.root.bg, anchor=NW)

        vais = partie.vaisseau
        vaisseauimg = PhotoImage(file='Images\\Vaisseau.png', width=vais.taille, height=vais.taille)
        self.root.vaisseauimg = vaisseauimg  # Previent le garbage collector d'effacer l'image
        self.canevas.create_image(vais.x, vais.y, image=vaisseauimg, anchor=CENTER)

        bossimg = PhotoImage(file='Images\\Boss.png', width=150, height=150)
        self.root.bossimg = bossimg

        ufoimg = PhotoImage(file='Images\\Ufos.png', width=30, height=30)
        self.root.ufoimg = ufoimg

        obusimg = PhotoImage(file='Images\\Obus.png', width=10, height=20)
        self.root.obusimg = obusimg

        torpilleimg = PhotoImage(file='Images\\Torpille.png', width=10, height=20)
        self.root.torpilleimg = torpilleimg

        mineimg = PhotoImage(file='Images\\mine.png', width=30, height=30)
        self.root.mineimg = mineimg

        ufos = partie.ufos
        mines = partie.vaisseau.mines

        for i in vais.obus:
            self.canevas.create_image(i.x, i.y, image=obusimg, anchor=CENTER)

        for i in ufos:
            if isinstance(i, Ufo):
                self.canevas.create_image(i.x, i.y, image=ufoimg, anchor=CENTER)
            elif isinstance(i, Boss):
                self.canevas.create_image(i.x, i.y, image=bossimg, anchor=CENTER)
                self.canevas.create_line(i.x - 50, i.y - 75, (i.x - 50) + (i.hp * 5), i.y - 75, width=10, fill="red")

        for i in ufos:
            for j in i.torpille:
                self.canevas.create_image(j.x, j.y, image=torpilleimg, anchor=CENTER)

        for i in mines:
            self.canevas.create_image(i.x, i.y, image=mineimg, anchor=CENTER)

    def initpartie(self):
        self.canevas.bind("<Motion>", self.coordvaisseau)
        self.canevas.bind("<Button>", self.creerobus)
        self.canevas.bind("<Button-3>", self.creermines)

    def creerobus(self, evt):
        self.parent.creerobus()

    def creermines(self, evt):
        self.parent.creermines()

    def coordvaisseau(self, evt):
        x = evt.x
        y = evt.y
        self.parent.coordvaisseau(x, y)

    def inputhighscores(self, points):
        self.gameoverwindow = LabelFrame(self.cadre, text="GG WP", font=("Arial", 24))

        self.gameover = StringVar(value='GAME OVER\nPoints : ' + str(points))
        self.points = StringVar(value=str(points))

        self.gameoverwindow.grid(column=0, row=0, padx=10, sticky=NW)
        self.scores = Label(self.gameoverwindow, textvariable=self.gameover, font=("Arial", 18))

        self.nom = Label(self.gameoverwindow, text="Votre nom :", font=("Arial", 12))
        self.nomjoueur = Entry(self.gameoverwindow)
        self.savescore = Button(self.gameoverwindow, text="Enregistrer", command=self.savescore)
        self.scores.grid(column=1, row=1, padx=10, pady=10)
        self.nom.grid(column=0, row=2, padx=10, pady=10)
        self.nomjoueur.grid(column=1, row=2, padx=10, pady=10)
        self.savescore.grid(column=2, row=2, padx=10, pady=10)

    def savescore(self):
        nom = self.nomjoueur.get()
        print("save", self.points.get(), nom)
        fichier = open("score.txt", "a")
        info = self.points.get() + ", " + nom + "\n"
        fichier.write(info)

        self.showhighscores()
        self.canevas.destroy()
        self.statwindow.destroy()
        self.gameoverwindow.destroy()
        self.cadre.destroy()
        self.creercadreprincipale()

    def showhighscoresbutton(self, evt):
        scores = []
        with open("score.txt", "r") as fichier:
            for line in fichier:
                strippedline = line.strip('\n')
                score = int(strippedline.split(", ")[0])
                nom = strippedline.split(", ")[1]
                newline = score, nom
                scores.append(newline)

        scores.sort(key=lambda x:x[0], reverse=True)

        # scores = open("score.txt", "w")

        self.menu.grid_forget()

        self.highscores = LabelFrame(self.cadre, text="Highscores", width=600, height=750, font=("Arial", 24))

        for i in scores:
            self.text_highscores.set(str(i) + "\n")
            self.label_highscores = Label(self.highscores, textvariable=self.text_highscores, font=("Arial", 18))

        self.btnback = Button(self.cadre, text="Back", font=("Arial", 16), command=self.back)

        self.highscores.grid(column=0, row=0)
        if scores:
            self.label_highscores.grid()
        self.btnback.grid()


        print("highscores")
        print(scores)

    def showhighscores(self):
        scores = []
        with open("score.txt", "r") as fichier:
            for line in fichier:
                strippedline = line.strip('\n')
                score = int(strippedline.split(", ")[0])
                nom = strippedline.split(", ")[1]
                newline = score, nom
                scores.append(newline)

        scores.sort(key=lambda x: x[0], reverse=True)
        print("Highscores")
        print(scores)

# --------------------- MODELE ----------------------- #

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.partie = None
        self.dimX = 600
        self.dimY = 750
        self.nbrufosparniveau = 5

    def demarrerpartie(self):
        self.partie = Partie(self)

    def coordvaisseau(self, x, y):
        self.partie.coordvaisseau(x, y)

    def gameover(self, points):
        self.parent.gameover(points)

class Partie():
    def __init__(self, parent):
        self.parent = parent
        x = self.parent.dimX / 2
        y = self.parent.dimY * 0.8
        self.vaisseau = Vaisseau(self, x, y)
        self.ufos = []
        self.niveau = 0
        self.points = 0
        self.ufosmorts = set()
        self.creerniveau()
        self.coordvaisseauX = 0
        self.coordvaisseauY = 0

    def creerniveau(self):
        self.niveau += 1
        if self.vaisseau.minesdisponibles < 9:
            self.vaisseau.minesdisponibles += 2
        elif self.vaisseau.minesdisponibles == 9:
            self.vaisseau.minesdisponibles += 1
        print("Niveau : " + str(self.niveau))
        print("Mines disponibles : " + str(self.vaisseau.minesdisponibles))
        nbrufos = self.niveau * self.parent.nbrufosparniveau
        nbrpos = []
        self.vaisseau.mines = []

        if self.niveau % 5 == 0:
            nbrufos = self.niveau / 5

        while len(nbrpos) < nbrufos:
            posx = random.randrange(self.parent.dimX)
            posy = random.randrange(-300, -10)
            if [posx, posy] not in nbrpos:
                nbrpos.append([posx, posy])

        for i in nbrpos:
            if self.niveau % 5 == 0:
                self.ufos.append(Boss(self, i[0], i[1]))
            else:
                self.ufos.append(Ufo(self, i[0], i[1]))

    def coordvaisseau(self, x, y):
        self.coordvaisseauX = x
        self.coordvaisseauY = y

    def jouercoup(self):
        if self.vaisseau.invincible > 0:
            self.vaisseau.invincible -= 1
        self.vaisseau.deplacer(self.coordvaisseauX, self.coordvaisseauY)
        self.vaisseau.deplacerobus()
        for i in self.ufos:
            for j in i.torpille:
                j.deplacer()
        for i in self.ufos:
            for j in i.torpillemorts:
                i.torpille.remove(j)
        for i in self.ufos:
            i.torpillemorts = set()
        for i in self.ufos:
            i.deplacer()
        for i in self.vaisseau.obusmorts:
            self.vaisseau.obus.remove(i)
        self.vaisseau.obusmorts = set()
        for i in self.vaisseau.minesmorts:
            self.vaisseau.mines.remove(i)
        self.vaisseau.minesmorts = set()
        for i in self.ufosmorts:
            if i in self.ufos:
                self.ufos.remove(i)
        self.ufosmorts = set()
        if not self.ufos:
            self.creerniveau()
        if self.vaisseau.hp <= 0:
            self.parent.gameover(self.points)

    def creerobus(self):
        self.vaisseau.creerobus()

    def creermines(self):
        self.vaisseau.creermines()

class Vaisseau():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 50
        self.x = x
        self.y = y
        self.vitesse = 10
        self.obus = []
        self.obusmorts = set()
        self.hp = 10
        self.invincible = 0
        self.minesdisponibles = 0
        self.mines = []
        self.minesmorts = set()

    def deplacer(self, x, y):
        if self.x > x:
            self.x -= self.vitesse
        if self.x < x:
            self.x += self.vitesse
        if self.y > y:
            self.y -= self.vitesse
        if self.y < y:
            self.y += self.vitesse
        for i in self.parent.ufos:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille:
                if self.invincible == 0:
                    self.hp -= 1
                    self.invincible = 20
                    print("HP Remaining : " + str(self.hp))
        for i in self.parent.ufos:
            for j in i.torpille:
                distancerestante = Helper.calcDistance(self.x, self.y, j.x, j.y)
                if distancerestante < self.taille / 2:
                    i.torpillemorts.add(j)
                    if self.invincible == 0:
                        self.hp -= 1
                        self.invincible = 20
                        print("HP Remaining : " + str(self.hp))

    def creerobus(self):
        self.obus.append(Obus(self, self.x, self.y))

    def creermines(self):
        if self.minesdisponibles > 0:
            self.minesdisponibles -= 1
            print("Mines disponibles : " + str(self.minesdisponibles))
            self.mines.append(Mines(self, self.x, self.y))

    def deplacerobus(self):
        for i in self.obus:
            i.deplacer()
        for i in self.obusmorts:
            self.obus.remove(i)
        self.obusmorts = set()

class Mines():
   def __init__(self, parent, x, y):
       self.parent = parent
       self.taille = 30
       self.x = x
       self.y = y

class Obus():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 8
        self.vitesse = 10
        self.x = x
        self.y = y

    def deplacer(self):
        self.y -= self.vitesse
        if self.y < 0:
            self.parent.obusmorts.add(self)

class Torpille():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.dimY = self.parent.parent.parent.dimY
        self.taille = 8
        self.vitesse = 12
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.parent.dimX)
        self.cibleY = self.parent.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def deplacer(self):
        if self.parent.parent.niveau % 5 == 0:
            self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        else:
            self.y += self.vitesse
        if self.y > self.dimY:
            self.parent.torpillemorts.add(self)

class Ufo():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 30
        self.vitesse = 4
        self.hp = 1
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()
        self.torpille = []
        self.torpillemorts = set()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.dimX)
        self.cibleY = self.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def creertorpille(self):
        self.random = random.randrange(100)                         # randomise un numero de 0 a 100
        if self.random < 2:                                         # si 0 ou 1 on tire une torpille
            self.torpille.append(Torpille(self, self.x, self.y))

    def deplacer(self):
        self.creertorpille()                                                             # 2% chance par appel de tirer une torpille
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y) # choisi un target random sur laxe x
        distancerestante = Helper.calcDistance(self.x, self.y, self.cibleX, self.cibleY) #
        if distancerestante < self.vitesse:
            self.parent.ufosmorts.add(self)
        for i in self.parent.vaisseau.obus:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille / 2:
                self.hp -= 1
                if self.hp <= 0:
                    self.parent.points += 5
                    print("Points : " + str(self.parent.points))
                    self.parent.ufosmorts.add(self)
                self.parent.vaisseau.obusmorts.add(i)
        for i in self.parent.vaisseau.mines:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille + 3:
                self.parent.points += 5
                print("Points : " + str(self.parent.points))
                self.parent.ufosmorts.add(self)
                for j in self.parent.ufos:
                    if self != j:
                        distancerestante = Helper.calcDistance(self.x, self.y, j.x, j.y)
                        if distancerestante < 75:
                            j.hp -= 3
                            if j.hp <= 0:
                                self.parent.points += 5
                                print("Points : " + str(self.parent.points))
                                self.parent.ufosmorts.add(j)
                self.parent.vaisseau.minesmorts.add(i)

class Boss():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 150
        self.vitesse = 8
        self.hp = 20
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()
        self.torpille = []
        self.torpillemorts = set()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.dimX)
        self.cibleY = random.randrange(round(self.parent.parent.dimY / 3))
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def trouvercibletorpille(self):
        self.torcibleX = random.torcibleY = self.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def creertorpille(self):
        self.random = random.randrange(100)  # randomise un numero de 0 a 100
        newx = random.randint(round(self.x) - round(self.taille / 2.5), round(self.x) + round(self.taille / 2.5))

        if self.random < 25:  # si 0 a 19 on tire une torpille
            self.torpille.append(Torpille(self, newx, self.y))

    def deplacer(self):
        self.creertorpille()  # 2% chance par appel de tirer une torpille
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)  # choisi un target random sur laxe x
        distancerestantemouvement = Helper.calcDistance(self.x, self.y, self.cibleX, self.cibleY)
        for i in self.parent.vaisseau.obus:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille / 2.5:
                self.hp -= 1
                print("Boss HP : " + str(self.hp))
                if self.hp <= 0:
                    self.parent.points += 25
                    print("Points : " + str(self.parent.points))
                    self.parent.ufosmorts.add(self)
                self.parent.vaisseau.obusmorts.add(i)
        for i in self.parent.vaisseau.mines:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille / 2 + 15:
                self.hp -= 3
                print("Boss HP : " + str(self.hp))
                if self.hp <= 0:
                    self.parent.ufosmorts.add(self)
                for j in self.parent.ufos:
                    if self != j:
                        distancerestante = Helper.calcDistance(self.x, self.y, j.x, j.y)
                        if distancerestante < 75:
                            self.hp -= 3
                            print("Boss HP : " + str(self.hp))
                            if self.hp <= 0:
                                self.parent.ufosmorts.add(self)

                self.parent.vaisseau.minesmorts.add(i)

        if distancerestantemouvement <= 20:
            self.trouvercible()

# ------------------- CONTROLEUR --------------------- #

class Controlleur():
    def __init__(self):
        self.modele = Modele(self)
        self.partie = None
        self.over = 0
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def demarrerpartie(self):
        self.over = 0
        self.modele.demarrerpartie()
        self.partie = self.modele.partie
        self.vue.initpartie()
        self.vue.afficherpartie(self.modele.partie)
        self.vue.root.after(50, self.jouercoup())       # appel apres 50 ms jouercoup()

    def coordvaisseau(self, x, y):
        self.modele.partie.coordvaisseau(x, y)

    def jouercoup(self):
        if self.over == 0:                              # si game pas terminee alors
            self.modele.partie.jouercoup()
            self.vue.afficherpartie(self.partie)
            self.vue.root.after(50, self.jouercoup)     # appel recursif a chaque 50 ms

    def creerobus(self):
        self.partie.creerobus()

    def creermines(self):
        self.partie.creermines()

    def gameover(self, points):
        self.over = 1
        self.vue.inputhighscores(points)

if __name__ == '__main__':
    c = Controlleur()