#!/usr/bin/env python

import glob
import os
import sys


files = glob.glob('*sc1.ms')

obs_ids = []
for f in files:
	obs_ids.append(f[:10])


#set working directory to be one above that of individual obsid directories
path = os.getcwd()

#set index of obs_ids from sbatch script
findex = int(sys.argv[1])

#image parameters
imsize = '6154'
cell = '0.0052'
iters = '300000'
wght = 'uniform'


#for the obs image the calibrated ms file using wsclean and beam correct using pbcorrect
obs_ids.sort()
obs = obs_ids[findex]

	
#check to see if this obs has already been imaged
if not os.path.isfile(path+'/IMAGES/'+obs+'-I.fits'):
	print 'Imaging observation: '+obs
	cmd = 'cp -r %s_sc1.ms %s_final.ms' %(obs, obs)
	os.system(cmd)
	print cmd 
	ms_name = obs+'_final.ms'
	
	cmd0 = 'chgcentre %s %s %s' %(ms_name, '04h00m00.0s', '-27d00m00.0s')
	os.system(cmd0)
	print cmd0

	cmd0b = 'chgcentre -minw -shiftback %s' %(ms_name)
	os.system(cmd0b)
	print cmd0b

	#image with wsclean
	cmd='wsclean -name '+ obs+' -multiscale -mgain 0.85 -pol i -channels-out 4 -join-channels -weight '+wght+' -size '+imsize+' '+imsize+ ' -scale '+cell+' -niter '+iters+' -apply-primary-beam -auto-threshold 1.5 -auto-mask 3 -data-column CORRECTED_DATA '+ms_name
	os.system(cmd)

	#delete all the unwanted files
	cmd='rm -f '+obs+'*-residual.fits'
	os.system(cmd)
	cmd='rm -f '+obs+'*-dirty.fits'
	os.system(cmd)
	cmd='rm -f '+obs+'*-model.fits'
	os.system(cmd)
	cmd='rm -f '+obs+'*-psf.fits'
	os.system(cmd)
	'''
	#only generate beam if any one of the beam files doesn't already exist and you are not mosaicking later
	if not os.path.exists(obs+'_beam-xxi.fits') or not os.path.exists(obs+'_beam-xxr.fits') or not os.path.exists(obs+'_beam-xyi.fits') or not os.path.exists(obs+'_beam-xyr.fits') or not os.path.exists(obs+'_beam-yxi.fits')  or not os.path.exists(obs+'_beam-yxr.fits')  or not os.path.exists(obs+'_beam-yyi.fits') or not os.path.exists(obs+'_beam-yyr.fits'):
		cmd = 'make_beam.py -f '+obs+'-multiscale-XX-image.fits -m '+obs+'.metafits --model 2016 --jones'		
		print cmd
		os.system(cmd)
	
		
		cmd0 = 'mv '+obs+'-multiscale-XX-image_beamXXi.fits '+obs+'-XX-image_beam-xxi.fits'
		cmd1 = 'mv '+obs+'-multiscale-XX-image_beamXXr.fits '+obs+'-XX-image_beam-xxr.fits'
		cmd2 = 'mv '+obs+'-multiscale-XX-image_beamXYi.fits '+obs+'-XX-image_beam-xyi.fits'
		cmd3 = 'mv '+obs+'-multiscale-XX-image_beamXYr.fits '+obs+'-XX-image_beam-xyr.fits'
		cmd4 = 'mv '+obs+'-multiscale-XX-image_beamYXi.fits '+obs+'-XX-image_beam-yxi.fits'
		cmd5 = 'mv '+obs+'-multiscale-XX-image_beamYXr.fits '+obs+'-XX-image_beam-yxr.fits'
		cmd6 = 'mv '+obs+'-multiscale-XX-image_beamYYi.fits '+obs+'-XX-image_beam-yyi.fits'
		cmd7 = 'mv '+obs+'-multiscale-XX-image_beamYYr.fits '+obs+'-XX-image_beam-yyr.fits'
	
		os.system(cmd0)
		os.system(cmd1)
		os.system(cmd2)
		os.system(cmd3)
		os.system(cmd4)
		os.system(cmd5)
		os.system(cmd6)
		os.system(cmd7)
		
		cmd='pbcorrect '+obs+'-multiscale image.fits '+obs+'-XX-image_beam '+ obs
		print cmd
		os.system(cmd)
	'''
	cmd = 'mv %s*.fits IMAGES/' %(obs)
	os.system(cmd)
