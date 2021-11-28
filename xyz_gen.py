def s_looping(origin, rayon, ecart):
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


f = open("xyz_generated.txt", "w")
f.write(s_looping((60, 45, 26), 6, 4))
f.close()
