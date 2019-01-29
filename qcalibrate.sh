#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=01:10:00
#SBATCH --partition=workq
#SBATCH --account=mwaeor
#SBATCH --export=NONE
#SBATCH --array=0-14
#SBATCH -J cal6_121

module load MWA_Tools/mwa-sci
python calibrate.py ${SLURM_ARRAY_TASK_ID}
