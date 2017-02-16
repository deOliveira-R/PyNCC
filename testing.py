from geometry_rod_centered import Fuel
from layering import nodalize, equal_volume
from copy import deepcopy

elements_outer_radii = (0.4096, )
inner_radius = 0.15
densities = (10270, )
temperatures = (1200, )
compositions = ({'UO2': 100}, )
elements_nodes = (1, )

# elements_outer_radii = (0.34, 0.4096, 0.4106)
# inner_radius = 0.15
# densities = (10270, 10100, 3000)
# temperatures = (1200, 900, 600)
# compositions = ({'UO2': 102}, {'Th': 100}, {'ZrB2': 100})
# elements_nodes = (3, 1, 1)

elements_inner_radii = list(elements_outer_radii).copy()
elements_inner_radii.insert(0, inner_radius)
elements_inner_radii = tuple(elements_inner_radii[:len(elements_outer_radii)])

print(elements_inner_radii, elements_outer_radii)

for inner_radius, outer_radius, nodes in zip(elements_inner_radii, elements_outer_radii, elements_nodes):
    nodes_inner_radii, nodes_outer_radii = nodalize(outer_radius, nodes, equal_volume, inner_radius=inner_radius)
    print(nodes_inner_radii, nodes_outer_radii)


# Pellet = Fuel(outer_radii, densities, temperatures, compositions, inner_radius=inner_radius, radial_nodes=radial_nodes)
#
# for element in Pellet.elements:
#     for node in element.nodes:
#         print(node.inner_radius, node.outer_radius, node.density, node.temperature, node.composition)
#
# # THE CLASSES WORK UNTIL NOW
#
# Pellet2 = deepcopy(Pellet)
#
# for element in Pellet2.elements:
#     for node in element.nodes:
#         print(node.inner_radius, node.outer_radius, node.composition)
#
# # DEEPCOPY WORKS WITH OBJECTS
#
# print(Pellet.insert_type())
#
# if Pellet.insert_type() is "fuel":
#     print("Comparação funciona!")
# else:
#     print("Nada funciona nessa merda!")

