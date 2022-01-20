import numpy as np
import scipy.interpolate as spip

# Code fourni par les professeurs de l'UCL


def path_points(points, steps=None):
    """
    Calcule un chemin courbe à partir de points de passage.
    Les courbes sont des splines cubiques.

    Paramètres:
        points: array[3,N]
            N points de passage en 3 dimensions
        steps: int
            nombre de points à générer, par défaut 10 * N
    Retourne:
        XPath: array[3,steps]
            coordonnées des points sur le chemin en 3 dimensions
    """

    # paramètre: racine carrée de la corde accumulée:
    deltaTau = np.sqrt(np.sum(np.diff(points)**2, axis=0))
    tauPoints = np.hstack(((0), np.cumsum(deltaTau)))
    tauEnd = tauPoints[-1]

    # Interpoler avec des spline cubiques:
    spline = spip.splprep(points, u=tauPoints, s=0)[0]

    # Echantillonner à intervalles réguliers:
    if not steps:
        steps = 10*points.shape[1]
    tau = np.linspace(0, tauEnd, steps)
    XPath = np.array(spip.splev(tau, spline))

    return XPath


def path_vectors(XPath):
    """
    Calcule la distance curvilinéaire, le vecteur tangent et
    le vecteur de courbure le long du chemin.

    Paramètres:
        XPath: array[3,N]
            coordonnées de N points en 3 dimensions
    Retourne: (sPath, TPath, CPath)
        sPath: array[N]
            distance curvilinéaire des points
        TPath: array[3,N]
            vecteur tangent aux points (|T| = 1)
        CPath: array[3,N]
            vecteur de courbure aux points (|C| = courbure = 1/rayon)
    """
    ds = np.sqrt(np.sum(np.diff(XPath)**2, axis=0))
    s = np.hstack(((0), np.cumsum(ds)))

    dX_ds = np.gradient(XPath, s, axis=1, edge_order=2)
    d2X_ds = np.gradient(dX_ds, s, axis=1, edge_order=2)

    return s, dX_ds, d2X_ds


def path(points, steps=None):
    """
    Calcule les éléments d'un chemin courbe à partir de points de passage.

    Paramètres:
        points: array[3,N]
            N points de passage en 3 dimensions
        steps: int
            nombre de points à générer, par défaut 10 * N
    Retourne: (sPath, TPath, CPath)
        XPath: array[3,steps]
            coordonnées des points sur le chemin en 3 dimensions
        sPath: array[N]
            distance curvilinéaire des points
        TPath: array[3,N]
            vecteur tangent aux points (|T| = 1)
        CPath: array[3,N]
            vecteur de courbure aux points (|C| = courbure = 1/rayon)
    """
    XPath = path_points(points, steps)
    sPath, TPath, CPath = path_vectors(XPath)
    return sPath, XPath, TPath, CPath


def ainterp(x, xp, ap, **kwargs):
    """
    Interpolation en x sur plusieurs fonctions xp -> ap[k].

    Paramètres:
        x: float ou array[M]
            abscisses x_m où les fonctions sont évaluées
        xp: array[N]
            abscisses x_n des points des fonctions
        ap: array[K, N]
            ordonnées f_k(x_n) des points des fonctions

    Résultat:
        a: array[K] ou array[K, M]
            ordonnées évaluées f_k(x_m)
    """
    a = np.array([np.interp(x, xp, fp, **kwargs) for fp in ap])
    return a


def path_at(s, path, **kwargs):
    """
    Retourne les éléments en un point donné d'un chemin,
    par interpolation des données du chemin.

    Paramètres:
        s: float
            distance curviligne du point
        path: (sPath, XPath, TPath, CPath)
            éléments du chemin, tels que retournés par path().

    Retourne: X, T, C
        X: array[3]
            coordonnées du point
        T: array[3]
            vecteur tangent au point
        C: array[3]
            vecteur de courbure au point
    """
    sPath, XPath, TPath, CPath = path
    X = ainterp(s, sPath, XPath, **kwargs)
    T = ainterp(s, sPath, TPath, **kwargs)
    C = ainterp(s, sPath, CPath, **kwargs)
    return X, T, C


def tilt_vectors(T, beta=0.):
    """
    Retourne les vecteurs d'inclinaison le long d'un chemin.

    Paramètres:
        T: array[3]
            vecteur tangent au chemin
        beta: float, défaut=0.
            angle d'inclinaison par rapport à l'horizontale
            (> 0 = penche à droite dans le sens de T, en radians)

    Retourne: B, N
        B: array[3]
            vecteur unitaire normal parallèle à l'inclinaison
            (à gauche dans le sens de T)
        B: array[3]
            vecteur unitaire normal perpendiculaire à l'inclinaison
            (vers z > 0)
    """
    T /= np.sqrt(np.sum(T**2, axis=0))  # unit
    Z = np.array((0, 0, 1))

    D = np.cross(Z, T, axis=0)
    D /= np.sqrt(np.sum(D**2, axis=0))  # unit normale horizontale

    U = np.cross(T, D, axis=0)  # unit normale verticale

    B = D*np.cos(beta) + U*np.sin(beta)  # unit normale parallèle
    N = np.cross(T, B, axis=0)  # unit normale perpendiculaire
    return B, N
