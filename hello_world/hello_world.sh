#!/bin/bash
#SBATCH --time=0:0:20 --mem=1G
#SBATCH --ntasks=40

# Run with: sbatch hello_world.sh

mpirun python3 hello_world.py
