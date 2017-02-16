"""
1 object for geometry and materials of the reactor at the current iteration
1 object for geometry and materials of the reactor at the next iteration
and eventually becomes the new "current"

Send both, one to be executed and one to store data for next iteration

The sub-channel module also needs its own class of geometry, which has more requirements since it
has to calculate centroid and so on.

Proposal 1:

Create a list of objects to store iterations, retaining each at the memory.

Proposal 2:

Dump the last iteration into an HDF5 file to release memory and always store 2 objects at a time:
1 for now and 1 for the next.

"""

from math import pi

tau = 2*pi


class RadialNode(object):

    """
        This class defines the smallest element of an annular element (probably of fuel).

    Attributes:
        - Inner radius in m
        - Outer radius in m
        - Density in kg/m3
        - Temperature in K
        - Power generation in W
        - Elemental composition
    """

    def __init__(self, inner_radius, outer_radius, density, temperature, composition):

        """
            Initializes the RadialNode object.

        :param inner_radius: float
        :param outer_radius: float
        :param density: float
        :param temperature: float
        :param composition: dictionary
        """

        self.power = 0.0

        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.density = density
        self.temperature = temperature
        self.composition = composition

    def atombarn_composition(self):

        """
            This method converts the mass % composition to atom barn

        :return: a float of the composition in atom-barn
        """

        return 'atombarn'


class RadialElement(object):

    """
        This class defines the RadialElement object, which is the minimum element of a fresh
    assembly that has the same composition.

        A traditional UO2 fuel pellet has only 1 Fuel Element. A pellet with gadolinia in it,
    also know as Gadolinia Integral Burnable Absorber, has a single Fuel Element as well.
    A fuel pellet with a thin coating of neutron absorber (typically Zirconium DiBoride),
    also known as Integral Fuel Burnable Absorber, has 2 Fuel Elements, 1 for the fuel and
    1 for the absorber coating. A Duplex fuel pellet, which is a pellet that has 2 distinct
    radial compositions (e.g. UO2 inside and Thoria outside) also has 2 Fuel Elements.
    A UO2-Thoria duplex pellet with additional absorber coating would have 3 Fuel Elements,
    1 for UO2, 1 for Thoria and 1 for the absorber.

        The defining characteristic is that for a fresh assembly, elements have only 1 composition.
    Elements can be further divided in Nodes. Nodes of a fresh assembly also have the same composition
    and only properties such as temperature and radius (naturally) change from node to node.
    With burnup, nodes from a RadialElement will have different composition between themselves.

    Attributes:
        - nodes: a list of RadialNode. Every RadialElement contains at least 1 node
        - power: a float of total power in the RadialElement (sum of power in its nodes)
    """

    def __init__(self, element_inner_radii, element_outer_radii,
                 element_densities, element_temperatures, element_compositions):

        """
            Initializes the RadialElement object.

        :param element_inner_radii: tuple
        :param element_outer_radii: tuple
        :param element_densities: tuple
        :param element_temperatures: tuple
        :param element_compositions: tuple
        """

        self.power = 0.0
        self.nodes = []

        for node_inner_radius, node_outer_radius, node_density, node_temperature, node_composition \
                in zip(element_inner_radii, element_outer_radii,
                       element_densities, element_temperatures, element_compositions):
            self.nodes.append(RadialNode(node_inner_radius, node_outer_radius,
                                         node_density, node_temperature, node_composition))

    def power_update(self):

        """This method updates the element power by summing all the power values in the nodes"""

        self.power = sum(node.power for node in self.nodes)


class Fuel(object):

    """
        The Fuel class defines a concrete object, unlike RadialElement and RadialNode
    classes, which defines increasingly abstract ideas.

    Attributes:
        - elements: a list of RadialElements. Every Fuel contains at least 1 element
        - power: a float of total power in the Fuel (sum of power in its elements)
    """

    def __init__(self, fuel_inner_radii, fuel_outer_radii,
                 fuel_densities, fuel_temperatures, fuel_compositions):

        """
            This method initializes the Fuel object.

        :param fuel_inner_radii: tuple
        :param fuel_outer_radii: tuple
        :param fuel_densities: tuple
        :param fuel_temperatures: tuple
        :param fuel_compositions: tuple
        """

        self.power = 0.0
        self.elements = []

        self.clad_inner_temperature = 0.0
        self.clad_outer_temperature = 0.0

        for element_inner_radii, element_outer_radii, element_densities, element_temperatures, element_compositions \
                in zip(fuel_inner_radii, fuel_outer_radii, fuel_densities, fuel_temperatures, fuel_compositions):
            self.elements.append(RadialElement(element_inner_radii, element_outer_radii,
                                               element_densities, element_temperatures, element_compositions))

    def power_update(self):

        """This method updates the insert power by summing all the power values in the elements"""

        [element.power_update() for element in self.elements]

        self.power = sum(element.power for element in self.elements)

    @staticmethod
    def insert_type():

        return 'fuel'


class HollowRod(object):

    """
        This class models hollow rods in the reactor. Examples of hollow rods include fuel
    rod cladding, guide tubes and instrumentation tubes.
    """

    def __init__(self,
                 clad_inner_radius, clad_outer_radius,
                 clad_density, clad_temperature, clad_composition):

        self.power = 0.0
        self.clad_inner_temperature = 0.0
        self.clad_outer_temperature = 0.0

        self.clad_outer_radius = clad_outer_radius
        self.clad_inner_radius = clad_inner_radius
        self.clad_density = clad_density
        self.clad_temperature = clad_temperature
        self.clad_composition = clad_composition

    def thickness(self):
        """This method returns the thickness of the cladding of the rod"""
        return self.clad_outer_radius - self.clad_inner_radius

    def area(self):
        """This method returns the area of the rod"""
        return (1 / 2) * tau * (self.clad_outer_radius ** 2)

    def perimeter(self):
        """This method returns the perimeter of the rod"""
        return tau * self.clad_outer_radius

# class FuelRod(HollowRod, FuelPellet):
#
#
#     def __init__(self,
#                  pellet_outer_radius, pellet_inner_radius, pellet_density,
#                  clad_outer_radius, clad_inner_radius, clad_density):
#
#         HollowRod.__init__(self, clad_outer_radius, clad_inner_radius, clad_density)
#         FuelPellet.__init__(self, pellet_outer_radius, pellet_inner_radius, pellet_density)


