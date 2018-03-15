# BootComp
Created by:
Christine Currie christine.currie@soton.ac.uk
& Thomas Monks thomas.monks@soton.ac.uk 

Description:

When a simulation study has a large number of competing system designs/alternatives/scenarios,
it quickly becomes difficult to conduct a meaningful statistical analysis.  
The BootComp package is a multiple comparison tool for simulation output using bootstrapping.
BootComp provides simple to use tools for multiple comparisons and ranking
of scenarios.  The aim is to help analysts quickly identify the 'best' set
of scenarios that can be investigated further or presented to clients.

Installation:

BootComp is written in a mix of standard Python (3.x) and modern data science libraries.
It is recommended that users first install 'Anaconda' that bundles all of the 
data science libraries needed to run BootComp.  Anaconda also bundeles 'conda'
- a package manager - and jupyter a notebook based editing system for Python 
(and other data centric languages).

Anaconda: https://www.anaconda.com/download/ 

(Note: After installing Anaconda is is likely that BootComp will run fine.
Following the instructions below will install the exact libraries used 
to develop BootComp)

To get the correct libraries and versions in place.


1. Windows -> Open Anaconda prompt.  Mac/linux -> Open a terminal
2. Navigate to the BootComp directory
3. Run the following command:
    conda env create -f environment.yaml


This will fetch and install the libraries in a conda environment 'bootstrap'

4. To activate the bootstrap enviroment run the following command:
    activate bootstrap
    

Intructions for use:

BootComp includes a jupyter notebook tutorial: BootCompTutorial.ipynb


Alternatively if your prefer a text editor see BootComp.py

Launching