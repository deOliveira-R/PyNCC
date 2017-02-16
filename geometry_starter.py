"""
This module is responsible for a class that represents an initial, very simple geometry concept.

The objective is that this starter geometry is similar to how a person would reason about a PWR
geometry.

From this starter geometry, the program will create an expanded geometry that represents the reactor
in 3D "in its full glory". It is the expanded geometry that will be passed to the solvers!
"""

from layering import nodalize, equal_volume


class SimplifiedGeometry(object):

    def __init__(self):

        self.elements

    def expand_geometry(self):
        pass


outer_radii = [0.34, 0.4096, 0.4106]
inner_radius = 0.15
densities = [10270, 10230, 3000]   # has to be multiplied appropriately by number of nodes
temperatures = [1200, 900, 600]  # has to be multiplied appropriately by number of nodes
compositions = [{'UO2': 100}, {'Th': 100}, {'ZrB2': 100}]  # has to be multiplied appropriately by number of nodes
radial_nodes = (3, 1, 1)

# outer_radii = [(X   , Y, 0.34), (0.4096, ), (0.4106, )]
# inner_radii = [(0.15, X,    Y), (0.34  , ), (0.4096, )]
# densities = [(10270, 10270, 10270), (10230, ), (3000, )]
# temperatures = [(1200, 1200, 1200), (900, ), (600, )]
# compositions = [({'UO2': 100}, {'UO2': 100}, {'UO2': 100}), ({'Th': 100}, ), ({'ZrB2': 100}, )]
# radial_nodes = (3, 1, 1)

inner_radii = outer_radii[:-1]
inner_radii.insert(0, inner_radius)
inner_radii = inner_radii

fuel_inner_radii = []
fuel_outer_radii = []
fuel_densities = []
fuel_temperatures = []
fuel_compositions = []

for inner_radius, outer_radius, density, temperature, composition, nodes \
        in zip(inner_radii, outer_radii, densities, temperatures, compositions, radial_nodes):
    element_inner_radii, element_outer_radii = nodalize(outer_radius, nodes, equal_volume,
                                                        inner_radius=inner_radius)
    fuel_inner_radii.append(element_inner_radii)
    fuel_outer_radii.append(element_outer_radii)
    fuel_densities.append((density, ) * nodes)
    fuel_temperatures.append((temperature, ) * nodes)
    fuel_compositions.append((composition, ) * nodes)

print(fuel_inner_radii)
print(fuel_outer_radii)
print(fuel_densities)
print(fuel_temperatures)
print(fuel_compositions)
