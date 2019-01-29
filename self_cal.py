#!/usr/bin/env python

import glob
import os
import sys


def change_cnt(obs, selfcal, ph_ra, ph_dec):

	cmd0 = 'chgcentre '+obs+'_sc'+selfcal+'.ms %s %s' %(ph_ra, ph_dec)
	cmd = 'chgcentre -minw -shiftback '+obs+'_sc'+selfcal+'.ms'
	os.system(cmd0)
	os.system(cmd)

def imaging(obs, selfcal, wght, imsize, cell, iters,):
	print 'Initial imaging observation: '+obs
	ms_name = obs+'_sc'+selfcal+'.ms'

	#image with wsclean
	cmd='wsclean -name '+ obs+'-iter'+selfcal+' -multiscale -mgain 0.85 -pol xx,yy,xy,yx -join-polarizations -channels-out 4 -join-channels -weight '+wght+' -size '+imsize+' '+imsize+'  -scale '+cell+' -niter '+iters+' -auto-threshold 5 -auto-mask 8 -data-column CORRECTED_DATA '+ms_name
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
	cmd = 'make_beam.py -f '+obs+'-iter'+selfcal+'-XX-image.fits -m '+obs+'.metafits --model 2016 --jones'		
	print cmd
	os.system(cmd)
	
	
	cmd0 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamXXi.fits '+obs+'-iter'+selfcal+'-XX-image_beam-xxi.fits'
	cmd1 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamXXr.fits '+obs+'-iter'+selfcal+'-XX-image_beam-xxr.fits'
	cmd2 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamXYi.fits '+obs+'-iter'+selfcal+'-XX-image_beam-xyi.fits'
	cmd3 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamXYr.fits '+obs+'-iter'+selfcal+'-XX-image_beam-xyr.fits'
	cmd4 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamYXi.fits '+obs+'-iter'+selfcal+'-XX-image_beam-yxi.fits'
	cmd5 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamYXr.fits '+obs+'-iter'+selfcal+'-XX-image_beam-yxr.fits'
	cmd6 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamYYi.fits '+obs+'-iter'+selfcal+'-XX-image_beam-yyi.fits'
	cmd7 = 'mv '+obs+'-iter'+selfcal+'-XX-image_beamYYr.fits '+obs+'-iter'+selfcal+'-XX-image_beam-yyr.fits'
	
	os.system(cmd0)
	os.system(cmd1)
	os.system(cmd2)
	os.system(cmd3)
	os.system(cmd4)
	os.system(cmd5)
	os.system(cmd6)
	os.system(cmd7)

	cmd='pbcorrect '+obs+'-iter'+selfcal+' image.fits '+obs+'-iter'+selfcal+'-XX-image_beam '+ obs
	print cmd
	os.system(cmd)
	'''
	cmd = 'mv %s*.fits SC2_IMAGES/' %(obs)
	os.system(cmd)

def cal_obs(obs, selfcal):
	
	cmd = 'calibrate -minuv 20 -i 500 '+obs+'_sc'+selfcal+'.ms solutions-'+obs+'-iter'+selfcal+'.bin'
	print cmd
	os.system(cmd)
	cmd = 'applysolutions '+obs+'_sc'+selfcal+'.ms solutions-'+obs+'-iter'+selfcal+'.bin'
	os.system(cmd)
	print cmd
	cmd = 'aocal_plot.py solutions-'+obs+'-iter'+selfcal+'.bin'
	os.system(cmd)
	print cmd
	cmd = 'aoflagger '+obs+'_sc'+selfcal+'.ms'
	os.system(cmd)
	print cmd

#Determine list of obsid
files = glob.glob('*cotter.ms')
findex = int(sys.argv[1])
files.sort()
obs_file = files[findex]
obsid = obs_file[:10]
print obsid

scal = '1'
ra = '04h00m00.0s'
dec = '-27d00m00.0s'
cmd_cp = 'cp -r %s_cotter.ms %s_sc%s.ms' %(obsid, obsid, scal)
os.system(cmd_cp)
print cmd_cp

#image parameters
isize = '6200'
cll = '0.0043'
itrs = '300000'
wt = 'uniform'

change_cnt(obsid, scal, ra, dec)
imaging(obsid, scal, wt, isize, cll, itrs,)
cal_obs(obsid,scal)
