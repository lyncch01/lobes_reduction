# lobes_reduction
Scripts associated with Pawsey reduction of LOBES (2017) data

(1) meta_cotter.py ==  Run cotter on the files to either create flag files or unzip those downloaded from the archive. Then runs cotter to do the averaging and creates a measurement set. This can also get the metafits from the archive if not downloaded. Submitted to Pawsey supercomputers using qpreproc.sh

(2) calibrate.py == uses Offringa's calibrate function (mitchcal) to calibrate the measurement set. Submitted to queue using qcalibrate.sh

(3) self_cal.py == After initial calibration a single round of self-cal is run on each measurement set. This script re-centres the measurement set on the observation pointing centre and then the location of min-w (using chgcentre from wsclean). Then does a round of imaging where the model is saved to the measurement set. Then finally a second round of calibration (using the saved model in the MODEL column of the measurement set) -- again uses Offringa's calibrate function. Submitted to queue using qsc_image.sh

(4) imaging_wsclean.py == Does final imaging using wsclean; submitted using qimage_wsclean.sh
