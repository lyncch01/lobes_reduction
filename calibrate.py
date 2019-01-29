from astropy.io import fits
import string
import os.path
import glob
import os
import sys

def calibrate_run(obsid):
	metafits_filename=obsid+'.metafits'
	
	# Construct sky model
	cmd = 'srclist_by_beam.py -x -m %s -s /home/clynch/catalog/srclist_pumav3_EoR0aegean_EoR1pietro+ForA.txt -n 200' %(metafits_filename)
	print cmd
	os.system(cmd)
	
	#cmd= 'cat srclist_pumav3_EoR0aegean_EoR1pietro+ForA_%s_peel200.txt | rts_to_skymodel.py > model.txt' %(obsid)
	cmd = 'python /home/clynch/bin/rts_to_skymodel.py -i srclist_pumav3_EoR0aegean_EoR1pietro+ForA_%s_peel200.txt -o model_%s.txt' %(obsid, obsid)
	print cmd
	os.system(cmd)

	cmd = 'calibrate -minuv 20 -m model_%s.txt -applybeam -j 20 -i 500 %s_cotter.ms solutions-%s.bin' %(obsid, obsid, obsid)
	print cmd
	os.system(cmd)

	cmd = 'applysolutions %s_cotter.ms solutions-%s.bin' %(obsid,obsid)
	print cmd
	os.system(cmd)
	
	cmd = 'aoflagger %s_cotter.ms' %(obsid)
	print cmd
	os.system(cmd)
	
	cmd = 'aocal_plot.py solutions-%s.bin' %(obsid)
	print cmd
	os.system(cmd)
	

file = glob.glob("lobes_6_???.txt")[0]
obs_ids = []
for line in open(file):
	obs_ids.append(line[:10])

obs_ids.sort()
indx = int(sys.argv[1])
obs = obs_ids[indx]

files = glob.glob('%s_cotter.ms' %(obs))
if len(files) > 0:
	calibrate_run(obs)
else:
	print 'No ms-file; did you run cotter?'
	pass
