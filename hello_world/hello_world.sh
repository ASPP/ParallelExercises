#!/bin/bash
#$ -V -N hello_world.py -cwd -o output.$JOB_NAME.$JOB_ID

# Run with: qsub -pe mpislots N hello_world.sh

module load apps/anaconda3/2.5.0/bin
module load mpi/openmpi/1.8.5/gcc-4.8.5

mpirun python hello_world.py
