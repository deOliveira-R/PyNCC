"""
    This module is responsible for the many divisions necessary during operations in cylinders.
For example, for neutronics it is very common to divide the pellet into equal-volume regions
in order to investigate the power density variation with radius. In thermal hydraulics codes
it is very common to use equal-thickness finite element to discretize components.

    Therefore, this module is a support module to help in these operations and others related
to discretization, sometimes with the simple objective of unloading such operation from some
other code in order to increase readability and understanding.
"""

from math import sqrt


def equal_volume(outer_radius, radial_layers, *, inner_radius=0.0):

    """
        YIELDS A GENERATOR! Items are yielded in crescent order of inner radii.

        This function divides a cylinder into multiple equal-volume concentric cylinders.
    It receives the outer radius and the inner radius optionally (defaults to 0) of the
    unified cylinder. It uses the interval_constant between each rind and adds the square
    of the current inner radius to calculate the next inner radius the rings in sequence.

    Example case:

    A cylinder of outer radius r_o and inner radius r_i is to be divided into 5 concentric
    equal-thickness cylinders.

    Each of the 5 regions will have an inner radius. r_i1 for region 1, r_i2 for region 2, until
    r_i5 for region 5. The function then yields in order:

    r_i1, r_i2, r_i3, r_i4 and r_i5, where r_i1 is equal to r_i.

    :type outer_radius: float
    :type radial_layers: int
    :type inner_radius: float
    :return: float
    """

    interval_constant = ((outer_radius**2) - (inner_radius**2)) / radial_layers

    for i in range(radial_layers):
        yield inner_radius
        inner_radius = sqrt(interval_constant + inner_radius**2)


def equal_thickness(outer_radius, radial_layers, *, inner_radius=0.0):

    """
        YIELDS A GENERATOR! Items are yielded in crescent order of inner radii.

        This function divides a cylinder into multiple equal-thickness concentric cylinders.
    It receives the outer radius and optionally the inner radius of the unified cylinder
    (defaults to 0). It then calculates the interval_constant between each rind and calculates
    the rings in sequence.

    Example case:

    A cylinder of outer radius r_o and inner radius r_i is to be divided into 5 concentric
    equal-thickness cylinders.

    Each of the 5 regions will have an inner radius. r_i1 for region 1, r_i2 for region 2, until
    r_i5 for region 5. The function then yields in order:

    r_i1, r_i2, r_i3, r_i4 and r_i5, where r_i1 is equal to r_i.

    :type outer_radius: float
    :type radial_layers: int
    :type inner_radius: float
    :return: float
    """

    interval_constant = (outer_radius - inner_radius) / radial_layers

    for i in range(0, radial_layers):
        yield inner_radius
        inner_radius += interval_constant


def nodalize(outer_radius, radial_nodes, discretizer, *, inner_radius=0.0):

    """
        This function divides an arbitrary cylinder into concentric cylindrical radial_nodes
    according to a discretizer (equal-volume cylinders using the equal-volume function for
    example). It then returns 2 tuples: one of inner radii and another of outer radii. Each
    item of same index in the lists corresponds to the inner and outer radii of the node
    with same index (for example, node 0 has inner_radii[0] inner radius and outer_radii[0]
    outer radius).

        Rationale: Parts of the code that need nodalization becomes clean and easy to
        understand. That is how codes MUST be!

    Example case:

    A cylinder of outer radius r_o and inner radius r_i is to be divided into 5 concentric
    equal-volume cylindrical nodes. Therefore this function is caller with the equal-volume
    function as a discretizer.

    The equal-volume functions divides the cylinders and returns a GENERATOR containing that
    giver the inner radius of each node in order:

    r_i1, r_i2, r_i3, r_i4, r_i5

    This function then generates a list of the inner radii of each node. In order to generate
    the outer radii list it slices the inner radii list without the first term as a starting
    point, because the outer radius of node i is the same as the inner radius of node i+1
    (the outer radius of node 2 is the inner radius of node 3, for example). It then appends
    the outer radius of the original cylinder as the last item in the outer radii list (since
    that is the outer radius of the last node). Finally it converts both lists to tuples and
    returns the tuples.

    :param outer_radius: float
    :param radial_nodes: int
    :param discretizer: function
    :param inner_radius: float
    :return: tuple, tuple
    """

    inner_radii = list(discretizer(outer_radius, radial_nodes, inner_radius=inner_radius))

    outer_radii = inner_radii[1:]
    outer_radii.append(outer_radius)

    return tuple(inner_radii), tuple(outer_radii)


def volume_averaged(outer_radius, inner_radius):
    """
        This function receives the outer radius and inner radius of a cylindrical region.
    It then returns the volume-averaged radius of this region.

    :type outer_radius: float
    :type inner_radius: float
    :return: float
    """

    return (2 / 3) * ((outer_radius ** 2 + outer_radius * inner_radius + inner_radius ** 2)
                      / (outer_radius + inner_radius))
