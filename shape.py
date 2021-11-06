# Ce fichier contient plusieurs fonction pour faire différentes formes de chemin
import numpy as np


def looping_points(steps=21):
    """
    Calcule les points de passage pour un chemin simple avec
    un looping.  Le chemin a pour équations:

        x = t*(t-1)**2 + 0.5*t
        y = 0.5*t*(t-1)**2
        z = 2*t**2*(t-0.9)**2

    pour -1 ≤ t ≤ 1

    Paramètres:
        steps: int (défaut 21)
            le nombre de points
    Retourne: array[3, steps]
        coordonnées des point de passage
    """
    tPoints = np.linspace(-1, 1, steps)
    Xpoints = np.vstack((
        0.5*tPoints + tPoints*(tPoints-1)*(tPoints+1),
        0.5*tPoints*(tPoints-1)*(tPoints+1),
        2*tPoints*tPoints*(tPoints-0.9)*(tPoints+0.9)
    ))
    return Xpoints


def parabole_points(L, H, steps=12):
    """Renvoie les coordonés d'une parabole

    Args:
        L (float): longueur de la parabole
        H (float): hauteur de la parabole

    Returns:
        array: tableaux avec coordonés des points
    """
    A = 4*H/L**2  # parabole d'équation z = A * x**2
    # coordonnée horizontale: array[points] * [m]

    tPoints = np.linspace(-L/2, L/2, steps)
    Xpoints = np.vstack((
        tPoints,
        tPoints*0.2,
        A*tPoints**2
    ))
    return Xpoints


def droite(L, H, steps=12):
    """Renvoie une droite qui va tout droit

    Args:
        L (float): la longueur de la droite
        H (float): la hauteur de la droite
        steps (int, optional): le nombre de point. Defaults to 12.
    """
    tPoints = np.linspace(-L/2, L/2, steps)
    slope = H/L
    xpoints = np.vstack((
        tPoints,
        0*tPoints,
        -slope*tPoints
    ))
    return xpoints


def file_shape(filename):
    data = np.loadtxt(filename, int, unpack=True)
    return data
