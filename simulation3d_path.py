# Importation des librairies et fichiers nécessaires
import path3d as p3d
import numpy as np
import matplotlib.pyplot as plt
import physic_model_3d as phys
import shape

# Initialisation des variables temporels de la simulation
t = 0
tEnd = 20
dt = 0.0001
steps = int(tEnd//dt)
steps_graphic = 400  # Pour le lag de la représentation graphique si dt est trop petit

# Récupération des points de passages
xyzPoints = shape.xyz_from_file("xyz_circuit_real.txt")

# Utilisation de path3d pour obtenir les points et les vecteurs tangents et de courbure
sPath, xyzPath, TPath, CPath = p3d.path(xyzPoints, steps_graphic)

# Points jalons à afficher sur le graphique
length = sPath[-1]
sMarks = np.linspace(0, length, steps_graphic)
xyzMarks = np.empty((3, steps_graphic))    # Coordonnées
TMarks = np.empty((3, steps_graphic))  # Vecteur tangent
CMarks = np.empty((3, steps_graphic))      # Vecteur de courbure

# Interpolation du chemin avec l'aide du fichier fourni
for i in range(steps_graphic):
    xyz = p3d.ainterp(sMarks[i], sPath, xyzPath)
    T = p3d.ainterp(sMarks[i], sPath, TPath)
    C = p3d.ainterp(sMarks[i], sPath, CPath)

    xyzMarks[:, i] = xyz
    CMarks[:, i] = C
    TMarks[:, i] = T

# Affichage du circuit avec un graphique 3D
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_box_aspect(np.ptp(xyzPath, axis=1))
ax.plot(xyzPoints[0], xyzPoints[1], xyzPoints[2], 'bo', label='Points')
ax.plot(xyzPath[0], xyzPath[1], xyzPath[2], 'k-', lw=0.5, label='Chemin')
scale = 0.5*length/steps_graphic
ax.quiver(xyzMarks[0], xyzMarks[1], xyzMarks[2],
          scale*TMarks[0], scale*TMarks[1], scale*TMarks[2],
          color='r', linewidth=0.5, label='Vecteurs trajectoire')
show_c_vector = False  # Si on veut afficher les vecteurs de courbures ou pas
if show_c_vector:
    ax.quiver(xyzMarks[0], xyzMarks[1], xyzMarks[2],
              scale*CMarks[0], scale*CMarks[1], scale*CMarks[2],
              color='g', linewidth=0.5, label='Vecteurs courbure')
ax.legend()
plt.show()

# Simulation du mouvement de la bille

# Paramètre physique
e = 0.0007  # Coefficient de frottement
r = 0.008  # Rayon de la bille
m = 0.008  # Masse de la bille
b = 0.014  # Ecart des rails
g = 9.81  # Accélération du à la gravité
h = np.sqrt(r**2 - (b**2)/4)

# Données à remplir (tableaux numpy vides)
a_sim = np.zeros(steps+1)
vs_sim = np.zeros(steps+1)
t_sim = np.zeros(steps+1)
s_sim = np.zeros(steps+1)

# Tableaux des énergies
E_cin_sim = np.zeros(steps+1)
E_pot_sim = np.zeros(steps+1)

# Valeurs initiales
a_sim[0] = 0
vs_sim[0] = 0
t_sim[0] = 0
s_sim[0] = 0
E_cin_sim[0] = phys.cinetic_energy(m, vs_sim[0], phys.inertia(r, h))
E_pot_sim[0] = phys.potentiel_energy(m, xyzPoints[2][0], g)

# Boucle principale de la simulation
i = 0
while i < steps:
    # Interpolations des vecteurs
    T = p3d.ainterp(s_sim[i], sPath, TPath)
    C = p3d.ainterp(s_sim[i], sPath, CPath)

    # Calcul de l'accélération
    a = phys.acceleration(vs_sim[i], C, T, h, e, r, g)

    # Stockage des valeurs
    a_sim[i+1] = a
    vs_sim[i+1] = vs_sim[i] + a*dt
    t_sim[i+1] = t_sim[i] + dt
    s_sim[i+1] = s_sim[i] + vs_sim[i+1] * dt

    xyz = p3d.ainterp(s_sim[i+1], sPath, xyzPath)
    E_cin_sim[i+1] = phys.cinetic_energy(m, vs_sim[i+1], phys.inertia(r, h))
    E_pot_sim[i+1] = phys.potentiel_energy(m,
                                           xyz[2], g)

    # Arrêt de la simulation si on est plus loin que la piste
    if s_sim[i+1] > length:
        break
    i += 1

# Suppression des données superflues (si arrêt de la simulation)
if i != steps:
    a_sim = np.delete(a_sim, np.s_[i:])
    vs_sim = np.delete(vs_sim, np.s_[i:])
    t_sim = np.delete(t_sim, np.s_[i:])
    s_sim = np.delete(s_sim, np.s_[i:])
    E_cin_sim = np.delete(E_cin_sim, np.s_[i:])
    E_pot_sim = np.delete(E_pot_sim, np.s_[i:])

# Graphique de la vitesse, l'accélération tangentielle et la distance curviligne
plt.figure()
plt.subplot(311)
plt.plot(t_sim, vs_sim, label='vs')
plt.ylabel("Vitesse tangentielle [m/s]")
plt.xlabel("Temps [s]")
plt.subplot(312)
plt.plot(t_sim, a_sim, label='a')
plt.ylabel('Accélération tangentielle [m/s²]')
plt.xlabel('Temps [s]')
plt.subplot(313)
plt.plot(t_sim, s_sim, label='s')
plt.ylabel('Distance curviligne [m]')
plt.xlabel('Temps [s]')
plt.show()

# Graphiques des énergies
plt.figure()
plt.plot(t_sim, E_pot_sim, 'b-', label='Energie potentielle')
plt.plot(t_sim, E_cin_sim, 'r-', label='Energie cinétique')
plt.plot(t_sim, E_pot_sim+E_cin_sim, 'k-', label='Energie mécanique totale')
plt.legend()
plt.ylabel('Energie [J]')
plt.xlabel('Temps [s]')
plt.show()

# Affichage de la longueur du circuit
print("Longueur du circuit : ", length, " m")
print("Temps de parcours : ", t_sim[-1], " secondes")
