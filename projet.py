####### Projet IN603 - Attaque contre le chiffrement à flot CSS #######
##### LE CORRE Camille - LEFEVRE Laura - LDD BI #####


### QUESTION 1 ###

### Programmer le premier LFSR de 17 bits où l'état sera représenté par une seule variable.
### Ce LFSR possède deux coefficients de rétroaction non-nuls : 0 et 14.

def XOR(x,y):
    ''' Retourne x XOR y, où x et y appartiennent à {0,1} '''

    if (x not in ('0','1')) or (y not in ('0','1')):
        raise Exception("x et y doivent appartenir à {0,1}")
    
    return abs(int(x)-int(y))     # si x = y alors x - y = 0 => x XOR y = 0
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

    return y


## Pour tester ce LFSR :

s1_test = '10110010100011000'    # remplacez par ce que vous voulez
taille_sortie_s1 = 8   # remplacez par la taille souhaitée
#print(LFSR_17(s1_test, taille_sortie_s1))


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

    return y


## Pour tester ce LFSR :

s2_test = '0100110001110000111100000'    # remplacez par ce que vous voulez
taille_sortie_s2 = 8   # remplacez par la taille souhaitée
#print(LFSR_25(s2_test, taille_sortie_s2))