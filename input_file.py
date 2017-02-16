
temperature = 565
density = 10270

# CONTROL ARGUMENTS

radial_nodes = (3, 1, 1)

# this argument has to successfully divide the pellet into multiple nodes. This means that
# if the approach is to start from TH, from a single guessed temperature, density and composition
# it has to create a list of temperatures and densities where all parameters are the same

neutronics_solver = "wims11"  # or "monk" for continuous energy monte carlo

XS_library = "jeff3.12"
resonance = "full"  # or "partial", defaults to None

condense_energy_groups = 22  # only for non-continuous neutronics_solver

neutronics_method = "hybrid monte carlo"  # example of hybrid monte carlo

monk_neutron_sampling = 20000
monk_settling_stages = 10
monk_actual_stages = 1000
monk_stdv = 0.0001

# neutronics_method = "method of characteristics"
#
# c3d_n_azimuthal = 19
# c3d_sep_azimuthal = 0.005
# c3d_n_polar = 19

# Some neutronics_solver might have multiple methods available (WIMS has MONK and CACTUS for example)
# therefore the neutronics_method resolves to the right method.
# If a solver has multiple methods (such as WIMS) no default will be assumed and the method
# MUST be given, with its simulation parameters

th_solver = "cobraen"

# This is an example of sub-channel thermal-hydraulics solver
# In the future, CFD should also be available and in this case a CAD file (of whatever) has to be given

begins_with = "thermal-hydraulics"  # or "neutronics"

# The standard behaviour is for the sequence to begin with thermal-hydraulics assuming flat power profile,
# that meaning that for a channel of power X and Y equal length nodes, each node will have X/Y power.
# This flag can be used to override that and begin with neutronics (in which case, inlet temperatures
# and densities will be assumed everywhere.

