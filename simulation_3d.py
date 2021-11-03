import numpy
import math

def angle_bewteen_vectors(a, b):
    """Renvoie l'angle entre 2 vecteurs (unitaires)

    Args:
        a ([array]): premier vecteur, il doit être unitaire
        b (array): deuxième vecteur unitaire

    Retruns:
        Valeur de l'angle en radian
    """
    scalar_product = a[0]*b[0] + a[1]*a[1] + a[2]*a[2]
    return math.acos(scalar_product)

def normal_of_vector(vec):
    sum = 0
    for comp in vec:
        sum+=comp**2
    return math.sqrt(sum)
    
def gs_normal(T, g):
    """Renvoie la norme du vecteur gs

    Args:
        T (array): Le vecteur unitaire trajectoire
        g (float): la constante de gravité

    Returns:
        flaot: la norme de g
    """
    angle = angle_bewteen_vectors([0,0,1], T)
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
    g_vector = [0,0, g]
    gs_vector = [T[0]*gs_norm, T[1]*gs_norm, T[2]*gs_norm]
    return [g_vector[0] - gs_vector[0], g_vector[1]-gs_vector[1], g_vector[2]-gs_vector[1]]

def denominator_acceleration(r, h):
    """Calcul le dénominateur de notre grosse équation

    Args:
        r (float): le rayon de la bille
        h (float): la hauteur entre le centre de la bille et jsp quoi

    Returns:
        float: le dénominateur
    """
    return (1 +(2*(r**2))/(5*(h**2)))

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
    total_vector = [speed_vector[0]-gn[0], speed_vector[1]-gn[1], speed_vector[2]-gn[2]]
    return normal_of_vector(total_vector)

def numerator_acceleration(Vs, C, T,h, e, g):
    return (gs_normal(C, g)-e*Vs*norm_vector_gn(C, Vs, gn_vector(T,g))/h)

def acceleration(Vs, C, T, h, e, r, g):
    return numerator_acceleration(Vs, C, T, h, e, g)/denominator_acceleration(r, h)
