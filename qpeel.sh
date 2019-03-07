#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=05:00:00
#SBATCH --partition=workq
#SBATCH --account=mwaeor
#SBATCH --export=NONE
#SBATCH --mail-type END,FAIL,TIME_LIMIT
#SBATCH --mail-user christene.lynch@curtin.edu.au
#SBATCH -J peel_picA

module load MWA_Tools/mwa-sci
python peel_picA.py
    
