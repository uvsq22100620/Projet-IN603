####### Projet IN603 - Attaque contre le chiffrement à flot CSS #######
##### LE CORRE Camille - LEFEVRE Laura - LDD BI #####


### QUESTION 1 ###

### Programmer le premier LFSR de 17 bits où l'état sera représenté par une seule variable.
### Ce LFSR possède deux coefficients de rétroaction non-nuls : 0 et 14.

def XOR(x,y):
    ''' Retourne x XOR y, où x et y appartiennent à {0,1} '''
    # Cette fonction sera utilisée tout au long du projet

    if (x not in ('0','1')) or (y not in ('0','1')):
        raise Exception("x et y doivent appartenir à {0,1}")
    
    return abs(int(x)-int(y))   # si x = y alors x - y = 0 => x XOR y = 0
                                # si x != y alors x - y = 1 si x = 1 et y = 0
                                #                 x - y = -1 si x = 0 et y = 1
                                # => abs(x - y) = 1


def DecaleRegistre(s):
    ''' Décale tous les bits du registre d'un indice plus faible.
    La chaine de caractères renvoyée et donc d'une taille plus petite (de 1) que celle de l'entrée '''

    return s[1:]


def LFSR_17(s, l):
    ''' Le LFSR prend en entrée un état s = (s0, s1, ..., s16) qui est une chaîne de caractères de taille 17,
    où chaque caractère correspond à un bit de l'état initial. l est la taille du résultat que l'on veut en sortie'''

    # Vérification que s est bien de taille 17
    if len(s) != 17:
        raise Exception("L'entrée s doit être de taille 17")
    
    # Vérification que s ne contient pas que des 0
    if '1' not in s:
        raise Exception("L'entrée s ne doit pas être composée uniquement de 0")

    y = ''  # initialisation de la suite binaire y

    for tour in range(l):   # à chaque coup d'horloge
        y += s[0]   # ajout de s0 à y
        b = str(XOR(s[14], s[0]))   # calcul du bit b = s0 XOR s14
        s = DecaleRegistre(s) + b      # décalage du registre et ajout de b en position n-1

    return (y,s)       # on retourne le résultat ainsi que l'état du LFSR à la fin
         # (nécessaire pour garder l'historique et relancer ensuite le LFSR avec ce dernier état, cf question 3)


## Pour tester ce LFSR :

s1_test = '00000000000000001'    # remplacez par ce que vous voulez
taille_sortie_s1 = 48   # remplacez par la taille souhaitée
#print(LFSR_17(s1_test, taille_sortie_s1)[0])


### Implementer une fonction de test qui vérifie que l'état prend bien les 2^17 - 1 valeurs différentes
### pour une initialisation quelconque non-nulle du registre s1 = {0,1}^17

# Il y 2^17 suites différentes de 17 bits. Cependant, nous ne voulons pas de la suite s composée uniquement de 0.
# Donc il existe 2^17 - 1 = 131 071 suites non-nulles de taille 17.

def test_LFSR17():
    ''' En énumérant les nombres binaires de 1 à 131 071, on va tester tous les cas possibles d'entrée pour ce LFSR.
        La fonction renvoie un message si toutes les entrées ont été testées et acceptées. Si une d'entre elles ne
        l'est pas, alors une exception définie dans la fonction LFSR17 sera levée et le programme s'arrêtera.'''

    for n in range(1, 131072):      # pour tous les entiers de 1 à 131 071
        n_binaire = bin(n)[2:].zfill(17)    # bin(n) transforme n en base 10 en n en binaire
                                            # [2:] permet de se débarasser des 2 premiers caractères, qui sont '0b'
                                            # zfill(17) rajoute autant de 0 que nécessaire à gauche du nombre pour
                                            # que la taille atteigne 17 bits
        LFSR_17(n_binaire, 1)   # on teste que cette entrée est valide
                                # si elle ne l'est pas, alors une exception sera levée et le programme s'arrêtera

    return 'Toutes les entrées sont valides'     # si toutes les entrées ont été acceptées, on retourne ce message


## Pour tester que la fonction LFSR17 prend bien les 2^17 - 1 entrées possibles :
#print(test_LFSR17())


### QUESTION 2 ###

### Programmer le second LFSR de 25 bits.
### Ce LFSR possède quatre coefficients de rétroaction non-nuls : 12, 4, 3 et 0.

def LFSR_25(s, l):
    ''' Le LFSR prend en entrée un état s = (s0, s1, ..., s24) qui est une chaîne de caractères de taille 25,
    où chaque caractère correspond à un bit de l'état initial. l est la taille du résultat que l'on veut en sortie'''

    # Vérification que s est bien de taille 25
    if len(s) != 25:
        raise Exception("L'entrée s doit être de taille 17")
    
    # Vérification que s ne contient pas que des 0
    if '1' not in s:
        raise Exception("L'entrée s ne doit pas être composée uniquement de 0")

    y = ''  # initialisation de la suite binaire y

    for tour in range(l):   # à chaque coup d'horloge
        y += s[0]   # ajout de s0 à y
        b = str(XOR ( str(XOR(s[12], s[4])) , str(XOR(s[3], s[0])) ))   # calcul du bit b = (s12 XOR s4) XOR (s3 XOR s0)
        s = DecaleRegistre(s) + b      # décalage du registre et ajout de b en position n-1

    return (y,s)


## Pour tester ce LFSR :

s2_test = '0000000000000000000000001'    # remplacez par ce que vous voulez
taille_sortie_s2 = 48   # remplacez par la taille souhaitée
#print(LFSR_25(s2_test, taille_sortie_s2)[0])


### QUESTION 3 ###

### Programmer l'opération de chiffrement et de déchiffrement d'un texte avec CSS.

def Grand_XOR(x, y):
    ''' Retourne le XOR entre deux nombres binaires (de taille supérieure à 1)'''

    # Dans notre cas, x et y auront la même taille donc il n'est pas nécessaire
    # de vérifier cette condition. Sinon, il aurait fallut rajouter autant de 0
    # à gauche du plus petit nombre pour qu'il ait la même taille que le plus grand

    res = ''

    for b in range(len(x)-1, -1, -1):      # effectue l'opération de droite à gauche
        res = str(XOR(x[b], y[b])) + res
    
    return res

#print(Grand_XOR('01011011', '10110110'))
#print(Grand_XOR('1111', '1111'))


def Genere_s(taille_m, k):
    ''' Permet de générer la suite s'''

    s = ''      # initialisation de la suite s qui sera ensuite XORée avec le message clair m
    c = 0       # initialisation de c
    s1 = k[:16] + '1'       # initialisation de s1
    s2 = k[16:] + '1'       # et s2 (à partir de la clé)

    while len(s) < taille_m:        # pour que la taille de s soit supérieure ou égale à la taille de m

        # On fait tourner les 2 LFSR avec s1 en entrée pour celui de 17 bits et s2 pour celui de 25 bits
        # On veut récupérer un octet par LFSR
        res1 = LFSR_17(s1, 8)
        res2 = LFSR_25(s2, 8)

        # Stockage de ces octets dans x (pour LFSR_17) et y (pour LFSR_25) et conversion en décimal
        x = int(res1[0][::-1], 2)           # il faut inverser le résultat du LFSR car le premier bit
        y = int(res2[0][::-1], 2)           # sorti de chaque LFSR est le bit de poids faible de x et y

        # On récupère aussi l'état des LFSR après avoir sorti l'octet x ou y ;
        # ce sera la configuration utilisée pour relancer le LFSR pour produire le prochain octet
        s1 = res1[1]
        s2 = res2[1]

        # Calcul de z
        z = (x + y + c) % 256

        # Ajout de l'octet z à s
        s += bin(z)[2:].zfill(8)        # il faut d'abord le convertir en binaire et ajouter à gauche
                                        # autant de 0 que nécessaire pour avoir 8 bits

        # Calcul de c
        if (x + y) > 255:
            c = 1
        else:
            c = 0

    return s[:taille_m]    # on retire les bits de gauche en trop de s pour que s et m aient la même taille


def chiffrement_CSS(m, k):
    ''' Simule le chiffrement d'un message clair m avec la clé k grâce au chiffrement à flot CSS'''

    # Vérification que k est bien de taille 40
    if len(k) != 40:
        raise Exception("k doit être de taille 40")
    
    ### Génération de la suite s ###
    s = Genere_s(len(m), k)
    
    ### Chiffrement de m en faisant un XOR avec s ###
    chiffre = Grand_XOR(m, s)       # Production de c = m XOR s

    return chiffre      # on retourne le chiffré


## Pour tester le chiffrement avec CSS :

def affiche_resultat_chiffrement():
    ''' Permet l'affichage des résultats '''

    m_test = '1111111111111111111111111111111111111111'     # message à chiffrer : m = 0xffffffffff
    k_test = '0000000000000000000000000000000000000000'     # clé de 40 bits
    resultat_attendu = '1111111111111111101101100110110000111001'      # c = 0xffffb66c39
    resultat_obtenu = chiffrement_CSS(m_test, k_test)

    if resultat_obtenu == resultat_attendu:
        print("Le chiffrement CSS a permis d'obtenir le bon résultat.")
        print("message : ", m_test)
        print("clé : ", k_test)
        print("chiffré obtenu par le chiffrement CSS : ", resultat_obtenu)
        print("en hexadécimal : ", hex(int(resultat_obtenu,2)))
    else:
        print("Le résultat obtenu n'est pas celui attendu.")


#print(affiche_resultat_chiffrement())


### Vérifier que le déchiffrement se passe correctement.

# On sait que ci = si XOR mi <=> mi = si XOR ci
# Pour retrouver le message clair m, il faudra donc le chiffré mais il faudra aussi reproduire s.
# Pour reproduire s, il suffit de réaliser exactement les mêmes étapes que lors de la production
# de s pour le chiffrement. On utilise les mêmes LFSR initialisés de la même façon, avec la même
# clé et les mêmes coefficients de rétroactions associés aux LFSR.


## Voici la fonction de déchiffrement :

def dechiffrement_CSS(c, k):
    ''' Simule le déchiffrement d'un chiffré c avec la clé k'''

    # Vérification que k est bien de taille 40
    if len(k) != 40:
        raise Exception("k doit être de taille 40")
    
    ### Génération de la suite s ###
    s = Genere_s(len(c), k)
    
    ### Déchiffrement de c en faisant un XOR avec s ###
    clair = Grand_XOR(c, s)       # Production de m = c XOR s

    return clair      # on retourne le clair


## Pour tester le déchiffrement avec CSS (même exemple) :

def affiche_resultat_dechiffrement():
    ''' Permet l'affichage des résultats '''

    c_test = '1111111111111111101101100110110000111001'     # obtenu grâce à chiffrement_CSS(m_test, k_test)
    k_test = '0000000000000000000000000000000000000000'     # clé de 40 bits (la même que pour le chiffrement)
    resultat_obtenu = dechiffrement_CSS(c_test, k_test)
    resultat_attendu = '1111111111111111111111111111111111111111'   # c'est m_test

    if resultat_obtenu == resultat_attendu:
        print("Le déchiffrement CSS a permis d'obtenir le bon résultat.")
        print("chiffré : ", c_test)
        print("clé : ", k_test)
        print("clair obtenu par le déchiffrement : ", resultat_obtenu)
        print("en hexadécimal : ", hex(int(resultat_obtenu,2)))
    else:
        print("Le résultat obtenu n'est pas celui attendu.")


#print(affiche_resultat_dechiffrement())


### QUESTION 6 ###

### Programmer l'attaque contre ce générateur. Pour cela, initialiser le générateur avec une
### valeur aléatoire s appartenant à {0,1}^40 et générer par la suite 6 octets z1, z2, ..., z6.
### Vérifier que votre attaque permet de bien retrouver l'état initial.


def test_s1_s2(s2, x1_a_x6, liste_z1_a_z6, c):
    ''' Retourne True si z4, z5 et z6 calculés à partir de x1, x2, ... x6 et y1, y2, ..., y6
        correspondent bien à ceux attendus, retourne False sinon '''    

    y1_a_y6 = LFSR_25(s2, 48)[0]

    for i in range(3):          # Génération de z4, z5 et z6

        x = int(x1_a_x6[8*(3+i):8*(4+i)][::-1], 2)
        y = int(y1_a_y6[8*(3+i):8*(4+i)][::-1], 2)
        z_calcule = bin((x + y + c) % 256)[2:].zfill(8)

        # Test pour savoir si le z calculé est égal à celui attendu
        if z_calcule != liste_z1_a_z6[i+3]:
            return False
        
        # Calcul de c
        if (x + y) > 255:
            c = 1
        else:
            c = 0
    
    return True


def attaque_CSS(liste_z1_a_z6):
    ''' Réalise l'attaque contre CSS '''

    ## Tester toutes les suites s1 de 16 bits possibles
    for s1 in range(65536) :
        s1 = bin(s1)[2:].zfill(16) + '1'
        if len(s1) != 17:
            print('Il y a un problème car s1 = ', s1)
        x1_a_x6 = LFSR_17(s1, 48)[0]   # on fait tourner le premier LFSR pour obtenir les 6 octets x1 à x6

        ## Calcul de s2
        c = 0       # initialisation de c
        s2 = ''     # initialisation de s2

        for i in range(3):      # pour calculer y1, y2 et y3

            z = int(liste_z1_a_z6[i], 2)
            x = int(x1_a_x6[8*i:8*(i+1)][::-1], 2)
            y = (z - x - c) % 256

            # Ajout de y à s2
            s2 += bin(y)[2:].zfill(8)

            # Calcul de c
            if (x + y) > 255:
                c = 1
            else:
                c = 0

        s2 += '1'

        ## Test du couple (s1, s2)
        if test_s1_s2(s2, x1_a_x6, liste_z1_a_z6, c) :
            return (s1, s2)
        # si la condition n'est pas vérifiée alors un autre s1 sera testé

    return " Aucune clé trouvée"

#suite_z_test = ['00000000', '00000000', '01001001', '10010011', '11000110', '11001001']
#print(attaque_CSS(suite_z_test2))
#print(test_s1_s2('0000000000000000000000001', '000000000000000010010010010010010110010110010110', suite_z_test, 0))

from random import randint

def test_attaque_CSS():
    ''' Teste l'attaque '''

    # Génération de la clé
    k = ''
    for i in range(40):
        k = k + str(randint(0, 1))
    print('k : ', k)

    # Génération des six octets z1, z2, ..., z6
    s = Genere_s(48, k)     # production de s avec la clé k
    liste_z1_a_z6 = []
    for i in range(6):
        liste_z1_a_z6.append(s[i*8:(i+1)*8])
    print('z : ', liste_z1_a_z6)
    
    # Test
    print(attaque_CSS(liste_z1_a_z6))


test_attaque_CSS()