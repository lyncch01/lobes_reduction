#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00
#SBATCH --partition=workq
#SBATCH --account=mwaeor
#SBATCH --export=NONE
#SBATCH --array=2-14
#SBATCH -J sc6_121

module load MWA_Tools/mwa-sci

python self_cal.py ${SLURM_ARRAY_TASK_ID}
    
