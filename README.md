# BootComp

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CLAHRCWessex/BootComp/master)

**Created by:**
* Christine Currie christine.currie@soton.ac.uk
* Thomas Monks thomas.monks@soton.ac.uk 

**Description:**

When a simulation study has a large number of competing system designs/alternatives/scenarios,
it quickly becomes difficult to conduct a meaningful statistical analysis.  

The BootComp package is a multiple comparison tool for simulation output using bootstrapping.
BootComp is a simple 2 stage procedure simple to use tools for multiple comparisons and ranking of scenarios.  The aim is to help analysts quickly identify the 'best' set of scenarios that can be investigated further or presented to clients.

**Installation:**

* Note: BootComp can be tested using Binder (just click on the badge above) without any installation of dependencies on a local machine.  Opening the tutorial notebook to see how it works.

BootComp is written in a mix of standard Python (3.x) and modern data science libraries.
It is recommended that users first install 'Anaconda' that bundles all of the 
data science libraries needed to run BootComp.  Anaconda also bundeles 'conda' (a package manager) and jupyter a (notebook based editing system for Python and other data centric languages).  

Anaconda: https://www.anaconda.com/download/ 

To get the correct libraries and versions it is recommended that the provided conda environment is used.  To create and activate a bootcomp environment:

1. Windows -> Open Anaconda prompt.  Mac/linux -> Open a terminal
2. Navigate to the BootComp/binder directory
3. Run the following command:
    conda env create -f environment.yml

This will fetch and install the libraries in a conda environment 'bootcomp'

4. To activate the bootcomp enviroment run the following command:
    conda activate bootcomp
    
More help on environments can be found here: https://conda.io/docs/user-guide/tasks/manage-environments.html
    
**Instructions for use:**

* BootComp includes a jupyter notebook tutorial: **BootComp_Tutorial.ipynb**

**Unit-testing**:

See unit_tests.py for all unit testing of BootComp.  All tests are designed to run with pytest https://docs.pytest.org/en/latest/

To run unit-tests open a terminal and enter:

* pytest unit_tests.py

**Question and Answers:**

*I am a simulation practitioner. Can I use BootComp?*

* Yes! BootComp is published under an MIT license.  It is free and open software that can be used in commerical and research applications.  

* Practitioners who would like to use BootComp are welcome to contact the authors directly.  We would be very happy to hear from you.

*What version of Python should I be using?*

* Python 3.x.  It is recommended that users run BootComp under the environment included.  However, it will run under a general install of Anaconda and by running 'conda install numba'