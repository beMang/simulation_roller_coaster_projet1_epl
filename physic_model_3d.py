import math


def norm_of_vector(vec):
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
    return -g*T[2]


def gn_vector(T, g):
    """Renvoie le vecteur gn

    Args:
        T (array): Le vecteur unitaire trajectoire
        g (float): la constante de gravité

    Returns:
        array: Le vecteur gn sous forme de tableau gn = g-gs
    """
    gs_norm = gs_normal(T, g)
    g_vector = [0, 0, -g]
    # Pour avoir gs comme vecteur, on multiplie sa norme par T (vecteur unitaire)
    gs_vector = [T[0]*gs_norm, T[1]*gs_norm, T[2]*gs_norm]
    # on soustrait chaque composante car gn = g - gs
    return [g_vector[0] - gs_vector[0], g_vector[1]-gs_vector[1], g_vector[2]-gs_vector[2]]


def norm_vector_rn(C, Vs, gn):
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
    return norm_of_vector(total_vector)


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
    return (gs_normal(T, g)-e*Vs*norm_vector_rn(C, Vs, gn_vector(T, g))/h)


def inertia(r, h):
    """Renvoie le coefficient d'intertie (le dénominateur de l'équation)

    Args:
        r (float): le rayon de la bille
        h (float): la hauteur entre le centre de la bille et les rails

    Returns:
        float: le coefficient
    """
    return 1 + 2/5*r**2/h**2


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
    return numerator_acceleration(Vs, C, T, h, e, g)/inertia(r, h)


def cinetic_energy(m, v, I):
    """Renvoie l'énergie cinétique spécifique d'une particule

    Args:
        m (float): masse de la particule (kg)
        v (float): vitesse (m/s)
        I (float): coefficient d'inertie

    Returns:
        float: énergie cinétique spécifique en joule de la particule (J)
    """
    return 0.5*m*I*v**2


def potentiel_energy(m, h, g):
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
        Imprime la valeur de l'accélération avec l'exercice donné dans le document donné par les professeurs
        pour vérifier l'exactitude de la simulation
    """
    T = [2/3, 2/3, 1/3]
    C = [2, -2, 0]
    h = math.sqrt(0.01**2 - (0.012**2)/4)
    print(acceleration(2, C, T, h, 0.0004, 0.01, 9))


if __name__ == "__main__":
    test()
