import os
import glob


model = glob.glob('*_alpha.txt')[0]

obs_file = glob.glob('119436*final.ms')[0]
obsID = obs_file[:10]

cmd0 = 'cp -r %s %s_removed.ms' %(obs_file, obsID)
os.system(cmd0)
print cmd0

print 'Will subtract model %s from %s' %(model, obsID)

cmd = 'peel -datacolumn CORRECTED_DATA -m %s %s_removed.ms' %(model, obsID)
os.system(cmd)
print cmd


