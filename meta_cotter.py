from astropy.io import fits
import string
import os.path
import glob
import os
import sys
 
def meta_run(obsid, meta, pth): 	
	
	#check if metafits file exists, if not, download it
	if not os.path.isfile(pth+'/'+obsid+'/'+meta):
		cmd="make_metafits.py -o %s -g %s" % (meta,obsid)
		print 'Make Metafits'
		os.system(cmd)
	else:
		pass

def flag_run(obsid, meta):
	fls = glob.glob('*.mwaf')
	print len(fls)
	if len(fls) == 0:
		flagfiles = glob.glob('*.zip')
		if len(flagfiles) > 0:
			cmd = 'unzip %s_flags.zip' %(obsid)
			os.system(cmd)
			print 'Flag unzip'
		else:
			cmd = 'cotter -allowmissing -m %s -o %s_%s.mwaf *gpubox*.fits' % (meta,obsid,"%%")
			os.system(cmd)
			print 'Run cotter for flags'
	else:
		print 'already flagged'
		pass

def cotter_run(obsid, meta, fres, tres):
	msfls = glob.glob('*cotter.ms')
	if len(msfls) == 0:
		base_name=obsid+'_cotter'
		ms_name=base_name+'.ms'
		flagfiles_string=" %s_%s.mwaf " % (obsid,"%%")
	
		cmd = 'cotter -flagfiles %s -norfi -m %s -o %s  -timeres %s -freqres %s *gpubox*.fits' %(flagfiles_string, meta, ms_name, tres, fres)
		os.system(cmd)
		print 'Run cotter to create MS file'
	else:
		print 'ms file already created'
		pass

obs_ids = []
file = glob.glob("lobes_6_121.txt")[0]
obs_ids = []
for line in open(file):
	if len(line) < 1:
		continue
	if line[0] == "#":
		continue
	obs_ids.append(line[0:10])
obs_ids.sort()	
findex = int(sys.argv[1])
obs = obs_ids[findex]
wd_path = os.getcwd()
path = '/astro/mwaeor/MWA/data'

print 'Processing observation: '+obs
metafits_filename=obs+'.metafits'
 	
#create metafits file if does not exist
#meta_run(obs, metafits_filename, path)
	
#move to obsid directory to do rest of cottering
#cmd0 = 'mv %s.metafits %s/%s/' %(obs, path, obs)
#print cmd0
#os.system(cmd0) 
	
new_dir = '%s/%s' %(path, obs)
print 'change to '+new_dir
os.chdir(new_dir)
	
#create flag files using cotter
flag_run(obs, metafits_filename)
	
#cotter to create .ms file with specified averaging
tt = '8'
ff = '80'
cotter_run(obs, metafits_filename, ff, tt)	

cmd1 = 'mv %s.metafits %s' %(obs, wd_path)
os.system(cmd1)
print cmd1

cmd2 = 'mv %s_cotter.ms %s' %(obs, wd_path)
os.system(cmd2)
print cmd2

cmd3 = 'cp -r %s_cotter.ms %s_orig.ms' %(obs, obs)
os.system(cmd3)
print cmd3
