import math


def angle_bewteen_vectors(a, b):
    """Renvoie l'angle entre 2 vecteurs (unitaires)

    Args:
        a (array): premier vecteur, il doit être unitaire
        b (array): deuxième vecteur unitaire

    Retruns:
        Valeur de l'angle en radian
    """
    scalar_product = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    return math.acos(scalar_product/(normal_of_vector(a)*normal_of_vector(b)))


def normal_of_vector(vec):
    """Calcul la norme d'un vecteur à n dimension

    Args:
        vec (array): le vecteur (avec len(vec) dimension)

    Returns:
        float: la norme du vecteur
    """
    sum = 0
    for comp in vec:  # Je fais une boucle pour mettre au carré chaque composante
        sum += comp**2
    return math.sqrt(sum)


def gs_normal(T, g):
    """Renvoie la norme du vecteur gs

    Args:
        T (array): Le vecteur unitaire trajectoire
        g (float): la constante de gravité

    Returns:
        flaot: la norme de g
    """
    angle = angle_bewteen_vectors([0, 0, -1], T)
    return math.cos(angle)*g


def gn_vector(T, g):
    """Renvoie le vecteur gn

    Args:
        T (array): Le vecteur unitaire trajectoire
        g (float): la constante de gravité

    Returns:
        array: Le vecteur gn sous forme de tableau gn = g-gs
    """
    gs_norm = gs_normal(T, g)
    g_vector = [0, 0, g]
    # Pour avoir gs comme vecteur, on multiplie sa norme par T (vecteur unitaire)
    gs_vector = [T[0]*gs_norm, T[1]*gs_norm, T[2]*gs_norm]
    # on soustrait chaque composante car gn = g - gs
    return [g_vector[0] - gs_vector[0], g_vector[1]-gs_vector[1], g_vector[2]-gs_vector[1]]


def denominator_acceleration(r, h):
    """Calcul le dénominateur de notre grosse équation

    Args:
        r (float): le rayon de la bille
        h (float): la hauteur entre le centre de la bille et jsp quoi

    Returns:
        float: le dénominateur
    """
    return (1 + (2*(r**2))/(5*(h**2)))  # Dénominateur


def norm_vector_gn(C, Vs, gn):
    """Renvoie la norme du "gros" vecteur qui est au numérateur

    Args:
        C (array): le vecteur de courbure
        Vs (float): la vitesse actuelle
        gn (array): le vecteur gn

    Returns:
        float: la norme du gros_vecteur
    """
    sq_spd = Vs**2
    speed_vector = [C[0]*sq_spd, C[1]*sq_spd, C[2]*sq_spd]
    # On soustrait les 2 vecteurs (composante par composante)
    total_vector = [speed_vector[0]-gn[0],
                    speed_vector[1]-gn[1], speed_vector[2]-gn[2]]
    return normal_of_vector(total_vector)


def numerator_acceleration(Vs, C, T, h, e, g):
    """Renvoie le numérateur de notre grosse équation

    Args:
        Vs (float): vitesse actuelle
        C (array): vecteur normal/courbure
        T (array): vecteur tangeant à la trajectoire
        h (float): hauteur avec la bille et le rail
        e (float): frottemnt
        g (float): constante de gravité

    Returns:
        float: le numérateur de l'équation
    """
    return (gs_normal(T, g)-e*Vs*norm_vector_gn(C, Vs, gn_vector(T, g))/h)


def acceleration(Vs, C, T, h, e, r, g):
    """Renvoie la valeur de l'accélération en fonction des différents paramètres

    Args:
        Vs (float): vitesse actuelle
        C (array): vecteur normal/courubre
        T (array): vecteur tangeant à la trajectoire
        h (float): hauteur avec la bille et le rail
        e (float): frottement
        r (float): rayon de la bille
        g (float): constante de gravité

    Returns:
        float: résultats de l'équation en fonction de tous les paramètres
    """
    return numerator_acceleration(Vs, C, T, h, e, g)/denominator_acceleration(r, h)

def cinetic_energy(m, v):
    """Renvoie l'énergie cinétique d'une particule

    Args:
        m (float): masse de la particule (kg)
        v (float): vitesse (m/s)

    Returns:
        float: énergie cinétique en joule de la particule (J)
    """
    return 0.5*m*v**2

def potentiel_energy(m, h,g):
    """Renvoie l'énergie potentielle d'une particule

    Args:
        m (float): masse (kg)
        h (float): hauteur
        g (float): cst de gravité

    Returns:
        float: énergie potentielle en J
    """
    return m*g*h


def test():
    """Teste de l'exercice
        Imprime la valeur de l'accélération avec l'exercice donné dans le document
    """
    T = [2/3, 2/3, 1/3]
    C = [2, -2, 0]
    h = math.sqrt(0.01**2 - (0.012**2)/4)
    print(h)
    print(acceleration(2, C, T, h, 0.0004, 0.01, 9))

test()
