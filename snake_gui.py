import pygame
import time
import random

pygame.init()

# paramètres de l'écran de jeu
largeur = 800
hauteur = 600
taille_case = 20

# définition des couleurs
vert_tete = (80, 160, 40)
vert_corps = (120, 220, 80)
blanc_fond = (255, 255, 255)
rouge_fruit = (255, 0, 0)

# initialisation des paramètres du serpent
x_tete = largeur/2  # position de la tête du serpent (abscisse)
y_tete = hauteur/2  # position de la tête du serpent (ordonnée)
delta_x_tete = 0  # direction du serpent - abscisse (gauche / droite)
delta_y_tete = 0  # direction du serpent - ordonnée (haut / bas)

corps_serpent = [[x_tete, y_tete + taille_case],
                 [x_tete, y_tete + 2*taille_case]]

# initilisation des paramètres de la nourriture (position aléatoire
x_fruit = round(random.randrange(0, largeur - taille_case) / float(taille_case)) * float(taille_case)
y_fruit = round(random.randrange(0, hauteur - taille_case) / float(taille_case)) * float(taille_case)

# initialisation de l'écran et des paramètres de jeu
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Snake")

game_over = False
en_mouvement = False
horloge = pygame.time.Clock()
vitesse_jeu = 15

while not game_over:
    print(corps_serpent)
    for event in pygame.event.get():
        # l'utilisateur souhaite quitter le jeu
        if event.type == pygame.QUIT:
            game_over = True
        # l'utilisateur appuie sur une touche directionnelle
        if event.type == pygame.KEYDOWN:
            en_mouvement = True
            if event.key == pygame.K_LEFT:
                delta_x_tete = -taille_case
                delta_y_tete = 0
            elif event.key == pygame.K_RIGHT:
                delta_x_tete = taille_case
                delta_y_tete = 0
            elif event.key == pygame.K_UP:
                delta_x_tete = 0
                delta_y_tete = -taille_case
            elif event.key == pygame.K_DOWN:
                delta_x_tete = 0
                delta_y_tete = taille_case

    # Vérification de collision - bordures de l'écran
    if x_tete >= largeur or x_tete < 0 or y_tete >= hauteur or y_tete < 0:
        game_over = True
    # Vérification de collision - corps du serpent
    if [x_tete, y_tete] in corps_serpent:
        game_over = True

    # Si le serpent n'a pas rencontré d'obstacle, on met à jour les positions / on agrandit le serpent si nécessaire
    if not game_over:
        # Vérification de collision - fruit
        if x_tete == x_fruit and y_tete == y_fruit :
            # ajout d'un nouveau tronçon au corps du serpent (à la place de la tête, au lieu de déplacer tout le corps)
            corps_serpent.insert(0, [x_tete, y_tete])
            # changement de place du fruit
            x_fruit = round(random.randrange(0, largeur - taille_case) / float(taille_case)) * float(taille_case)
            y_fruit = round(random.randrange(0, hauteur - taille_case) / float(taille_case)) * float(taille_case)

        # On s'assure que le jeu a commencé avant de modifier les positions
        elif en_mouvement:
            # Déplacement de l'intégralité du corps
            for i in range(len(corps_serpent)-1, 0, -1):
                corps_serpent[i][0] = corps_serpent[i-1][0]
                corps_serpent[i][1] = corps_serpent[i-1][1]
            corps_serpent[0] = [x_tete, y_tete]
        # déplacement de la tête
        x_tete += delta_x_tete
        y_tete += delta_y_tete

        # modification de l'écran
        ecran.fill(blanc_fond)

        for element in corps_serpent:
            pygame.draw.rect(ecran, vert_corps, [element[0], element[1], taille_case, taille_case])
        pygame.draw.rect(ecran, rouge_fruit, [x_fruit, y_fruit, taille_case, taille_case])
        pygame.draw.rect(ecran, vert_tete, [x_tete, y_tete, taille_case, taille_case])
        # mise à jour de l'état du jeu
        pygame.display.update()

        # avancement de l'horloge
        horloge.tick(vitesse_jeu)

# fin du jeu (le joueur a perdu)
mesg = pygame.font.SysFont("comicsansms", 30).render("Perdu !", True, rouge_fruit)
ecran.blit(mesg, [largeur/2, hauteur/2])  # Affichage d'un message de défaite
pygame.display.update()

time.sleep(2)  # On laisse le programme ouvert deux secondes pour que le joueur ait le temps de voir le message

# On quitte le jeu
pygame.quit()
quit()