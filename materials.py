from collections import namedtuple


class ElementaryParticle(object):

    def __init__(self, mass, charge):

        self.mass = mass
        self.charge = charge

proton = ElementaryParticle(1.672621898E-27, 1)
neutron = ElementaryParticle(1.674927471E-27, 0)


class Atom(object):

    def __init__(self, mass, protons, neutrons):

        self.mass = mass
        self.protons = protons
        self.neutrons = neutrons

    def binding_energy_per_nucleon(self):

        pass


mass = namedtuple('mass', ['value', 'uncertainty'])

Uranium_233 = Atom(mass(233.0396355, 0.0000029), 92, 141)
Uranium_234 = Atom(mass(234.0409523, 0.0000019), 92, 142)
Uranium_235 = Atom(mass(235.0439301, 0.0000019), 92, 143)
Uranium_236 = Atom(mass(236.0455682, 0.0000019), 92, 144)
Uranium_238 = Atom(mass(238.0507884, 0.0000020), 82, 146)
