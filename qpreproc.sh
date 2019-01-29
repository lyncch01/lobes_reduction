#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=1:00:00
#SBATCH --partition=gpuq
#SBATCH --account=mwaeor
#SBATCH --export=NONE
#SBATCH --mem=30000
#SBATCH --gres=gpu:1
#SBATCH --array=0-18
#SBATCH -J prp6_121

python meta_cotter.py ${SLURM_ARRAY_TASK_ID}
