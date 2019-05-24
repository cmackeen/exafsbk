Cameron Mackeen

#Program use
This is written for python2.7 and uses the following packages: scipy, pandas, matplotlib, argparse 

This is set up to run the python script as an executabe, and use TkAGG matplotlib (check in header) for graphics delivered via bash execution.

The -h will show you brief help, and in general the only needed argument is the -es.

The -es flag must be followed by the edge energy of your simulated interefering edge (in eV). That is, the lower energy edge. 


Symbolic linking works for universal use on a unix system.

#Pre_edge bleed: EXAFS bg from conflicting absoprtion edges

If you do not know why/what this is, it is used to remove a special type of background where EXAFS oscillations extend into the atomic edge you are trying to analyze. These small deviations may not be filtered by generic polynomial spline fitting, and thus we seek to manually simulate the EXAFS from the interfering low-energy edge out to hi k (~20 inv. ang.). Clear indicator you need this EXAFS background removal is if the pre edge itself has oscillations of ~5%. 

credits to: Jason Gruzdas, Ryan Dudschus, and lifted argparse stuff form omgenomics
