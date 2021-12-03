# Ce fichier contient plusieurs fonctions pour faire différentes formes de chemin ainsi que une fonction pour générer les points d'un looping
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
        2*tPoints*tPoints*(tPoints-0.9)*(tPoints+0.9) + .5
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


def xyz_from_file(filename):
    """Renvoie les coordonnés depuis un fichier (en cm)
    Format du ficher : x y z

    Args:
        filename (str): nom du fichier

    Returns:
        array_numpy: tableau numpy
    """
    data = np.loadtxt(filename, int, unpack=True)
    return data/100  # Pour avoir les données en mètre


def generate_looping(origin, rayon, ecart):
    """Méthode pour générer des points pour un looping

    Args:
        origin (tuple): point de départ
        rayon (float): rayon du looping
        ecart (float): écart du looping

    Returns:
        str: Chaine des caractères avec les coordonés
    """
    points = [origin]
    points.append((origin[0]+rayon/2, origin[1], origin[2]))
    points.append((origin[0]+rayon, origin[1], origin[2]+rayon/2))
    points.append((origin[0]+rayon/2, origin[1]+ecart/2, origin[2]+rayon))
    points.append((origin[0], origin[1]+ecart, origin[2]+rayon/2))
    points.append((origin[0]+rayon/2, origin[1]+ecart, origin[2]))
    points.append((origin[0]+rayon, origin[1]+ecart, origin[2]))

    s = ""
    for x, y, z in points:
        s += "{x} {y} {z}\n".format(x=x, y=y, z=z)
    return s


# Enregistrement des points générés par la fonction generate_looping
if __name__ == "__main__":
    f = open("xyz_generated.txt", "w")
    f.write(generate_looping((60, 45, 26), 6, 4))
    f.close()
