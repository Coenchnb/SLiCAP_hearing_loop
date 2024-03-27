#usr/bin/env python3
# -*- coding: utf-8 -*-

from SLiCAP import *
# Always run SLiCAP from the project directory, this will define the correct path settings.
t1=time()

prj = initProject('Hearing Loop Project') # Sets all the paths and creates the HTML main index page.

fileName = 'SLiCAPReceiver'

makeNetlist(fileName + '.asc', 'Hearing Loop Project')
i1 = instruction()                       # Creates an instance of an instruction object
i1.setCircuit(fileName + '.cir')                  # Checks and defines the local circuit object and
                                         # sets the index page to the circuit index page

all_param_names = list(i1.circuit.parDefs.keys()) + i1.circuit.params
print(all_param_names)

# How to estimate all parameter definitions?
all_par_defs = i1.circuit.parDefs
print(all_par_defs)

# Here the parameters can be assigned via expressions or numeric values

# i1.defPars({'R': 'tau/C', 'C': '10n', 'tau': '1u'})
# i1.setSimType('numeric')
# print(i1.getParValue(['R', 'C']))

# We will generate a HTML report (not from within Jupyter). Let us first create an empty HTML page:
htmlPage('Circuit data')
# Put a header on this page and display the circuit diagram on it.
head2html('Circuit diagram')
img2html('SLiCAPReceiver.svg', 250, caption = 'Circuit diagram of the receiver network.', label = 'fig_receiver_network')
netlist2html(fileName + '.cir', label = 'netlist') # This displays the netlist
elementData2html(i1.circuit, label = 'elementData') # This shows the data of the expanded netlist
params2html(i1.circuit, label = 'params') # This displays the circuit parameters

i1.setSimType('symbolic')
i1.setGainType('vi')
i1.setDataType('matrix')
# We execute the instruction and assign the result to a variable 'MNA'
MNA = i1.execute();

# We will put the instruction on a new HTML page and display it in this notebook
htmlPage('Matrix equations')
# Let us put some explaining text in the report:
text2html('The MNA matrix equation for the RC network is:')
matrices2html(MNA, label = 'MNA', labelText = 'MNA equation of the network')
# The variables in this equation are available in the variable that holds 
# the result of the execution:
#
# 1. The vector 'Iv' with independent variables:
text2html('The vector with independent variables is:')
eqn2html('I_v', MNA.Iv, label = 'Iv', labelText = 'Vector with independent variables')
# 2. The matrix 'M':
text2html('The MNA matrix is:')
eqn2html('M', MNA.M, label = 'M', labelText = 'MNA matrix')
# 3. The vercor wit dependent variables 'Dv':
text2html('The vector with dependent variables is:')
eqn2html('D_v', MNA.Dv, label = 'Dv', labelText = 'Vector with dependent variables')

# Print a list with independent sources in the circuit
print(i1.indepVars())
# print a list with possible detectors in the circuit
print(i1.depVars())          
# Let us now evaluate the transfer function of this network.
# To this end we need to define a signal source and a detector.
# Both the source and the detector are attributes of the instruction object:
i1.setSource('V1')   # 'V1' is the identifier of the independent source that we assign as signal source
i1.setDetector('V_out') # 'V_out' is the voltage at node 'out' with respect to ground (node '0')
# The transfer from source to load is called 'gain'. Later we will discuss more transfer types.
i1.setGainType('gain')
# The data that we would like to obtain is the Laplace transfer of the gain. SLiCAP has many different 
# data types. The data type for an instruction is also an attribute of the instruction object:
i1.setDataType('laplace')
# SLiCAP performs symbolic calculations, even when the data is numeric. In those case SLiCAP calculates
# with rationals. Only in a limited number of cases SLiCAP calculates with floats.
# Numeric values or combined numeric/symbolic expressions can be assigned to circuit parameters. In cases
# in which the simulation type is set to 'numeric' such definitions are substituted recursively.
#
# Let us display the transfer symbolically. In this case we have no parameters defined, so 'numeric' will
# give the same answer as 'symbolic'.
i1.setSimType('symbolic')
# Let us execute the (modified) instruction 'i1' and assign the result to the variable gain:
gain = i1.execute()
# The laplace transform can now be found in the attribute 'laplace' of 'gain'.
eqn2html('V_out/V_1', gain.laplace, label = 'gainLaplace', labelText = 'Laplace transfer function')

# The parameters 'R' and 'C' stem from the circuit, while 's' is defined as the Laplace variable:
print(ini.Laplace)
