import numpy as np
import matplotlib.pyplot as plt


# Paramètres physiques:
g = 9.81  # accélération de gravitation [m/s**2]
b = 0.012  # écart des rails [m]
r = 0.008  # diamètre de la bille [m]
h = np.sqrt(r**2 - b**2/4)  # hauteur du centre de la bille sur les rails [m]

e1 = 0.0004  # coefficient de frottement linéaire [m/(m/s)]
e2 = 0.0002

# Dimensions de la piste (parabole)
#             |-----------L-----------|
#             +                       +---
#              ++                   ++  |
#                +++             +++    H
#                   ++++     ++++       |
#                       +++++          ---
L = 0.681*2  # longueur horizontale [m]
H = 0.412  # hauteur verticale [m]
A = 4*H/L**2  # parabole d'équation z = A * x**2

# Calcul de la piste:
points = 101  # nombre de points générés
dx = L / points
# coordonnée horizontale: array[points] * [m]
xPath = np.linspace(-L/2, L/2, points)
# coordonnée verticale: array[points] * [m]
zPath = A*xPath**2
# distance curviligne: array[points] * [m]
dsHalf = np.sqrt(np.diff(xPath)**2 + np.diff(zPath)**2)
sPath = np.hstack(((0), np.cumsum(dsHalf)))

# plot de la piste:
plt.figure()
plt.axis('equal')
plt.plot(xPath, zPath, 'x')
plt.plot((0., 0.), (0., H), ':k')
plt.annotate('H', (0., H/2))
plt.plot((-L/2, L/2), (H, H), ':k')
plt.annotate('L', (0, H))
plt.show()


# paramètres pour la simulation:
tEnd = 8.4  # durée de la simulation [s]
dt = 0.001  # pas de la simulation [s]

steps = int(tEnd / dt)  # nombre de pas de la simulatio
tSim = np.zeros(steps+1)  # temps: array[steps+1] * [s]
sSim = np.zeros(steps+1)  # distance curviligne: array[steps+1] * [m]
VsSim = np.zeros(steps+1)  # vitesse tangentielle: array[steps+1] * [m/s]

M = 1 + 2/5*r**2/h**2  # coefficient d'inertie [1]

# valeurs initiales:
tSim[0] = 0
sSim[0] = 0
VsSim[0] = 0
i = 0

# boucle de simulation:
while i < steps:
    x = np.interp(sSim[i], sPath, xPath)
    p = 2*A*x  # pente dz/dx
    cos_beta = 1 / np.sqrt(1+p*p)
    sin_beta = p / np.sqrt(1+p*p)
    c = 2*A / (1 + p*p)**1.5  # courbure

    As = (-g*sin_beta - e1*VsSim[i]/h * (g*cos_beta + c*VsSim[i]**2)) / M

    VsSim[i+1] = VsSim[i] + As * dt
    sSim[i+1] = sSim[i] + VsSim[i+1] * dt
    tSim[i+1] = tSim[i] + dt
    i = i+1


tSim2 = np.zeros(steps+1)  # temps: array[steps+1] * [s]
sSim2 = np.zeros(steps+1)  # distance curviligne: array[steps+1] * [m]
VsSim2 = np.zeros(steps+1)  # vitesse tangentielle: array[steps+1] * [m/s]

M = 1 + 2/5*r**2/h**2  # coefficient d'inertie [1]

# valeurs initiales:
tSim2[0] = 0
sSim2[0] = 0
VsSim2[0] = 0
i = 0

# boucle de simulation:
while i < steps:
    x = np.interp(sSim2[i], sPath, xPath)
    p = 2*A*x  # pente dz/dx
    cos_beta = 1 / np.sqrt(1+p*p)
    sin_beta = p / np.sqrt(1+p*p)
    c = 2*A / (1 + p*p)**1.5  # courbure

    As = (-g*sin_beta - e2*VsSim[i]/h * (g*cos_beta + c*VsSim[i]**2)) / M

    VsSim2[i+1] = VsSim2[i] + As * dt
    sSim2[i+1] = sSim2[i] + VsSim2[i+1] * dt
    tSim2[i+1] = tSim2[i] + dt
    i = i+1

zSim = np.interp(sSim, sPath, zPath)

# plot distance et vitesse et hauteur
plt.figure()
plt.subplot(311)
plt.plot(tSim, sSim, 'b-', label='Distance avec e=0.0004')
plt.plot(tSim2, sSim2, 'r-', label='Distance avec e=0.0002')
plt.ylabel('s [m]')
plt.xlabel('t [s]')
plt.subplot(312)
plt.plot(tSim, VsSim, "b-", label='Vitesse avec e=0.0004')
plt.plot(tSim2, VsSim2, "r-", label='Vitesse avec e=0.0002')
plt.ylabel('Vs [m/s]')
plt.xlabel('t [s]')
plt.legend()
plt.subplot(313)
plt.plot(tSim, zSim, label='z')
plt.ylabel('z [m]')
plt.xlabel('t [s]')
plt.legend()
plt.show()

EpSim = g*zSim  # énergie potentielle spécifique [m**2/s**2]
EkSim = 0.5*M*VsSim**2  # énergie cinétique spécifique [m**2/s**2]

# plot énergies
plt.figure()
plt.plot(tSim, EpSim, 'b-', label='Ep/m')
plt.plot(tSim, EkSim, 'r-', label='Ek/m')
plt.plot(tSim, EkSim+EpSim, 'k-', label='E/m')
plt.legend()
plt.ylabel('Energy/mass [J/kg]')
plt.xlabel('t [s]')
plt.show()

# sauver les données de simulation
np.savetxt('simulation_data.txt',
           np.column_stack((tSim, sSim, VsSim)), fmt='%10.5f')

# charger les données expérimentales
tExp, sExp, VsExp, AsExp = \
    np.loadtxt('tracker_data.txt', unpack=True, skiprows=2)

# plot données expérimentales
plt.figure()
plt.subplot(211)
plt.plot(tExp, sExp, 'r:', label='exp')
plt.plot(tSim, sSim, 'b-', label='sim')
plt.legend()
plt.ylabel('s [m]')
plt.xlabel('t [s]')

plt.subplot(212)
plt.plot(tExp, VsExp, 'r:', label='exp')
plt.plot(tSim, abs(VsSim), 'b-', label='sim')
plt.legend()
plt.ylabel('Vs [m/s]')
plt.xlabel('t [s]')

plt.show()
