# config file for jedimaster.py and associated programs
# a1.jedicolor    a2.jedicatalog
# b1.jedicolor    b2.jeditransform b3.jedidistort b4.jedipaste
# b5.jediconvolve b6.jedipaste     b7.jedirescale
# c1.jediaverage  c2.jedinoise     c3.jedinoise_10
#------------------------------ jedicolor --------------------------------------
# jedicolor will create simdatabase/bulge_disk_f8/bulge_disk_f8_0.fits
# using input text file physics_settings/color.txt.
# i.e. it scales bulge_f814w and disk_f818w galaxies into bulge_disk_f8 files.
# jedicatalog will read MAG,MAG0,PIXSCALE, and RADIUS from these files and
# will create three catalogs: 
# jedisim_out/out1/catalog.txt,convolved.txt,distortedlist.txt
# Therefore the files in bulge_f8 and disk_f8 should have these headers.
# The file f606w_gal284.fits has magnitude problem.
# The file f814w_gal202.fits has tabbed headers problem.
# All the original stamps have byteordr problem.
# None of the two component fitting files have four headers
# MAG, MAG0, RADIUS, PIXSCALE.
# So first we have to fix these problems and create bulge_f8 and disk_f8.
color_infile="physics_settings/color.txt"
color_outfolder="simdatabase/bulge_disk_f8"
jedicolor_args_infile="physics_settings/jedicolor_args.txt"
# jedicatalog will read these physics settings.
#----------------------------- physics settings --------------------------------
nx=12288            # x pixels            (arg for jedidistort)
ny=12288            # y pixels            (arg for jedidistort)
pix_scale=0.06      # arseconds per pixel (arg for jedidistort)
lens_z=0.3          # lens redshift       (arg for jedidistort)
single_redshift=1   # 0 = not-fixed, 1=fixed
fixed_redshift=1.5  # the single source galaxy redshift to use
final_pix_scale=0.2 # LSST pixscale (arcsecords per pixel)
exp_time=6000       # exposure time in seconds
noise_mean=10       # mean for poisson noise
x_border=301        # must be large enough so that no image can overflow_
y_border=301        # must be large enough so that no image can overflow
x_trim=480          # larger than x_border to ensure no edge effects
y_trim=480          # larger than y_border to ensure no edge effects
num_galaxies=12420  # number of galaxies to simulate 138,000 default
min_mag=22          # minimum magnitude galaxy to simulate (inclusive)
max_mag=28          # maximum magnitude galaxy to simulate (inclusive)
power=0.33          # power for the power law galaxy distribution
# For the f814 filter for our 201 galaxy images
#minmag   =  19.4715 # f814w_gal_19.fits
#maxmag   =  25.9455 # f814w_gal_214.fits
# For the HST galaxies cut outs we have magnitude range from 19-26.
# Note that we do not have the file radius database 19.txt
# inside simdatabase/radius_db/ so jedicatalog will fail if we take min_mag 19.
# However, we are not interested in HST galaxies cutouts.
# We are interested in fainter LSST galaxies with range 22-28 right now.
#---------------------------- psf and lenses -----------------------------------
# lens.txt has a single line with 5 parameters
# 6144 6144 1 1000.000000 4.000000
#  x    y  type p1       p2
#  x - x center of lens (in pixels)
#  y - y center of lens (in pixels)
#  type - type of mass profile
#         1. Singular isothermal sphere
#         2. Navarro-Frenk-White profile
#	       3. NFW constant distortion profile for grid simulations
#  p1 - first profile parameter
#         1. sigma_v [km/s]
#         2. M200 parameter [10^14 solar masses]
#		  3. Distance to center in px. M200 fixed at 20 default,
#            which can be modified in case 3
#  p2 - second profile parameter
#         1. not applicable, can take any numerical
#         2. c parameter [unitless]
#         3. c parameter [unitless]
lenses_file="physics_settings/lens.txt"	  # arg for jedidistort
#----------------------- output settings ---------------------------------------
# Note: we are taking prefix as trial1_ for all the output catalogs from jedicatalog.
# We will prefix output_folder to HST and LSST images in jedimaster.
# Fun fact: For some reasons if I don't use prefix the file name will be
# something like `s%DCtcatalog.txt either I use empty string or
# I don't use the  prefix row at all.
# So, for now just take trial1_ as the prefix to our catalogs.
output_folder="jedisim_out/out0/"  # jedicatalog etc.
HST_image="HST.fits"
HST_convolved_image="HST_convolved.fits"
LSST_averaged_image="LSST_averaged.fits"
LSST_averaged_noised_image="LSST_averaged_noised.fits"
rescaled_outfolder="jedisim_out/rescaled_lsst"
rescaled_lsst_outfile="physics_settings/rescaled_lsst_outfile.txt" # jediavg
monochromatic_infits="jedisim_out/rescaled_lsst/rescaled_lsst_10.fits"
monochromatic_outfits="jedisim_out/rescaled_lsst/rescaled_noised_lsst_10.fits"
#----------------------- 90 degree rotated case---------------------------------
90_output_folder="jedisim_out/out90/"  # jedicatalog etc.
prefix="trial1_" # used by jedicatalog etc.
rescaled_outfolder90="jedisim_out/rescaled_lsst90"
rescaled_lsst_outfile90="physics_settings/rescaled_lsst_outfile90.txt" # jediavg
monochromatic_infits90="jedisim_out/rescaled_lsst90/rescaled_lsst90_10.fits"
monochromatic_outfits90="jedisim_out/rescaled_lsst90/rescaled_noised_lsst90_10.fits"
#----------------------- database folders --------------------------------------
# There are 10 radius database files 20.dat to 29.dat.
# which contains min and max radius to be used by jedicatalog.
# e.g. the file simdatabase/radius_db/20.dat has two lines: 36.72 3.51
# This must contain files "n.txt" for n= min_mag to max_mag
radius_db_folder="simdatabase/radius_db/"
# There are 15+2 redshift database files 19.dat to 33.dat with +- 99.dat.
# which contains min and max redshift to be used by jedicatalog.
# e.g. the file simdatabase/red_db/19.dat has two lines: 0.301000 0.138000
# For f814 filter images:
# minmag   =  19.4715 # f814w_gal_19.fits
# maxmag   =  25.9455 # f814w_gal_214.fits
# minrad   =  1.31    # f814w_gal_43.fits     
# maxrad   =  21.895  # f814w_gal_9.fits
# For f606 filter images:
# minmag =  19.3882 # f606w_gal120.fits 
# maxmag =  25.5268 # f606w_gal215.fits  
# minrad =  1.157   # f606w_gal93.fits 
# maxrad =  22.055  # f606w_gal110.fits 
red_db_folder="simdatabase/red_db/"
#------------------- catalog files for jedicatalog -----------------------------
# jedicatalog will write:
# name,x,y,angle,redshift,pixscale,old_mag,old_rad,new_mag,new_rad,stamp_name,dis_name
# in the jedisim_out/out1/catalog.txt
# jedicatalog also creates jedisim_out/out1/convolvedlist.txt
# which has 6 lines like: jedisim_out/out1/convolved/convolved_band_0.fits
# jedicatalog also creates jedisim_out/out1/trial0_distortedlist.txt
# it has 0-12 folders and 1000 fitsfiles (total: 12420 files)
# line     1: jedisim_out/out1/distorted_0/distorted_0.fits
# line 12420: jedisim_out/out1/distorted_12/distorted_12419.fits
catalog_file="catalog.txt"
convolvedlist_file="convolvedlist.txt"
distortedlist_file="distortedlist.txt"
#----------------- catalog files for jedidistort -------------------------------
# jeditransform creates jedisim_out/out1/dislist.txt along with 12420 .gz stamps
# jedidistort will use these files.
# Input galaxy parameter file for jedidistort: x y nx ny zs file
#           x - x coord. of lower left pixel where galaxy should be embedded
#           y - y coord. of lower left pixel where galaxy should be embedded
#           nx - width of the galaxy in pixels
#           ny - height of the galaxy in pixels
#           zs - redshift of this galaxy
#           infile - filepath to the FITS file for this galaxy, 1024 chars max
#           outfile - filepath for the output FITS file for this galaxy, 1024 chars max
#
#  e.g. jedisim_out/out1/dislist.txt looks like this: (was created by jeditransform)
# 6813 888 10 23 1.500000 jedisim_out/out1/stamp_0/stamp_.fits.gz out1/distorted_0/distorted_0.fits
# x    y   nx ny zs       infile                      outfile
dislist_file="dislist.txt"  # arg for jedidistort
convlist_file="toconvolvelist.txt"
#----- source images for jedicatalog which are created from jedicolor ----------
num_source_images=201
# jedicolor scales bulge_f814w and disk_f814w galaxies and writes these files.
# jedicatalog will read MAG, MAG0, PIXSCALE, RADIUS from these files.
# jedicatalog will write these names in jedisim_out/out1/catalog.txt
# Required headers:
# MAG      : magnitude of the postage stamp image
# MAG0     : magnitude zeropoint of the postage stamp image
# PIXSCALE : pixel scale of the postage stamp image
# RADIUS   : R50 radius of the image, in pixels
image="simdatabase/bulge_disk_f8/bdf8_0.fits"
image="simdatabase/bulge_disk_f8/bdf8_1.fits"
image="simdatabase/bulge_disk_f8/bdf8_2.fits"
image="simdatabase/bulge_disk_f8/bdf8_3.fits"
image="simdatabase/bulge_disk_f8/bdf8_4.fits"
image="simdatabase/bulge_disk_f8/bdf8_5.fits"
image="simdatabase/bulge_disk_f8/bdf8_6.fits"
image="simdatabase/bulge_disk_f8/bdf8_7.fits"
image="simdatabase/bulge_disk_f8/bdf8_8.fits"
image="simdatabase/bulge_disk_f8/bdf8_9.fits"
image="simdatabase/bulge_disk_f8/bdf8_10.fits"
image="simdatabase/bulge_disk_f8/bdf8_11.fits"
image="simdatabase/bulge_disk_f8/bdf8_12.fits"
image="simdatabase/bulge_disk_f8/bdf8_13.fits"
image="simdatabase/bulge_disk_f8/bdf8_14.fits"
image="simdatabase/bulge_disk_f8/bdf8_15.fits"
image="simdatabase/bulge_disk_f8/bdf8_16.fits"
image="simdatabase/bulge_disk_f8/bdf8_17.fits"
image="simdatabase/bulge_disk_f8/bdf8_18.fits"
image="simdatabase/bulge_disk_f8/bdf8_19.fits"
image="simdatabase/bulge_disk_f8/bdf8_20.fits"
image="simdatabase/bulge_disk_f8/bdf8_21.fits"
image="simdatabase/bulge_disk_f8/bdf8_22.fits"
image="simdatabase/bulge_disk_f8/bdf8_23.fits"
image="simdatabase/bulge_disk_f8/bdf8_24.fits"
image="simdatabase/bulge_disk_f8/bdf8_25.fits"
image="simdatabase/bulge_disk_f8/bdf8_26.fits"
image="simdatabase/bulge_disk_f8/bdf8_27.fits"
image="simdatabase/bulge_disk_f8/bdf8_28.fits"
image="simdatabase/bulge_disk_f8/bdf8_29.fits"
image="simdatabase/bulge_disk_f8/bdf8_30.fits"
image="simdatabase/bulge_disk_f8/bdf8_31.fits"
image="simdatabase/bulge_disk_f8/bdf8_32.fits"
image="simdatabase/bulge_disk_f8/bdf8_33.fits"
image="simdatabase/bulge_disk_f8/bdf8_34.fits"
image="simdatabase/bulge_disk_f8/bdf8_35.fits"
image="simdatabase/bulge_disk_f8/bdf8_36.fits"
image="simdatabase/bulge_disk_f8/bdf8_37.fits"
image="simdatabase/bulge_disk_f8/bdf8_38.fits"
image="simdatabase/bulge_disk_f8/bdf8_39.fits"
image="simdatabase/bulge_disk_f8/bdf8_40.fits"
image="simdatabase/bulge_disk_f8/bdf8_41.fits"
image="simdatabase/bulge_disk_f8/bdf8_42.fits"
image="simdatabase/bulge_disk_f8/bdf8_43.fits"
image="simdatabase/bulge_disk_f8/bdf8_44.fits"
image="simdatabase/bulge_disk_f8/bdf8_45.fits"
image="simdatabase/bulge_disk_f8/bdf8_46.fits"
image="simdatabase/bulge_disk_f8/bdf8_47.fits"
image="simdatabase/bulge_disk_f8/bdf8_48.fits"
image="simdatabase/bulge_disk_f8/bdf8_49.fits"
image="simdatabase/bulge_disk_f8/bdf8_50.fits"
image="simdatabase/bulge_disk_f8/bdf8_51.fits"
image="simdatabase/bulge_disk_f8/bdf8_52.fits"
image="simdatabase/bulge_disk_f8/bdf8_53.fits"
image="simdatabase/bulge_disk_f8/bdf8_54.fits"
image="simdatabase/bulge_disk_f8/bdf8_55.fits"
image="simdatabase/bulge_disk_f8/bdf8_56.fits"
image="simdatabase/bulge_disk_f8/bdf8_57.fits"
image="simdatabase/bulge_disk_f8/bdf8_58.fits"
image="simdatabase/bulge_disk_f8/bdf8_59.fits"
image="simdatabase/bulge_disk_f8/bdf8_60.fits"
image="simdatabase/bulge_disk_f8/bdf8_61.fits"
image="simdatabase/bulge_disk_f8/bdf8_62.fits"
image="simdatabase/bulge_disk_f8/bdf8_63.fits"
image="simdatabase/bulge_disk_f8/bdf8_64.fits"
image="simdatabase/bulge_disk_f8/bdf8_65.fits"
image="simdatabase/bulge_disk_f8/bdf8_66.fits"
image="simdatabase/bulge_disk_f8/bdf8_67.fits"
image="simdatabase/bulge_disk_f8/bdf8_68.fits"
image="simdatabase/bulge_disk_f8/bdf8_69.fits"
image="simdatabase/bulge_disk_f8/bdf8_70.fits"
image="simdatabase/bulge_disk_f8/bdf8_71.fits"
image="simdatabase/bulge_disk_f8/bdf8_72.fits"
image="simdatabase/bulge_disk_f8/bdf8_73.fits"
image="simdatabase/bulge_disk_f8/bdf8_74.fits"
image="simdatabase/bulge_disk_f8/bdf8_75.fits"
image="simdatabase/bulge_disk_f8/bdf8_76.fits"
image="simdatabase/bulge_disk_f8/bdf8_77.fits"
image="simdatabase/bulge_disk_f8/bdf8_78.fits"
image="simdatabase/bulge_disk_f8/bdf8_79.fits"
image="simdatabase/bulge_disk_f8/bdf8_80.fits"
image="simdatabase/bulge_disk_f8/bdf8_81.fits"
image="simdatabase/bulge_disk_f8/bdf8_82.fits"
image="simdatabase/bulge_disk_f8/bdf8_83.fits"
image="simdatabase/bulge_disk_f8/bdf8_84.fits"
image="simdatabase/bulge_disk_f8/bdf8_85.fits"
image="simdatabase/bulge_disk_f8/bdf8_86.fits"
image="simdatabase/bulge_disk_f8/bdf8_87.fits"
image="simdatabase/bulge_disk_f8/bdf8_88.fits"
image="simdatabase/bulge_disk_f8/bdf8_89.fits"
image="simdatabase/bulge_disk_f8/bdf8_90.fits"
image="simdatabase/bulge_disk_f8/bdf8_91.fits"
image="simdatabase/bulge_disk_f8/bdf8_92.fits"
image="simdatabase/bulge_disk_f8/bdf8_93.fits"
image="simdatabase/bulge_disk_f8/bdf8_94.fits"
image="simdatabase/bulge_disk_f8/bdf8_95.fits"
image="simdatabase/bulge_disk_f8/bdf8_96.fits"
image="simdatabase/bulge_disk_f8/bdf8_97.fits"
image="simdatabase/bulge_disk_f8/bdf8_98.fits"
image="simdatabase/bulge_disk_f8/bdf8_99.fits"
image="simdatabase/bulge_disk_f8/bdf8_100.fits"
image="simdatabase/bulge_disk_f8/bdf8_101.fits"
image="simdatabase/bulge_disk_f8/bdf8_102.fits"
image="simdatabase/bulge_disk_f8/bdf8_103.fits"
image="simdatabase/bulge_disk_f8/bdf8_104.fits"
image="simdatabase/bulge_disk_f8/bdf8_105.fits"
image="simdatabase/bulge_disk_f8/bdf8_106.fits"
image="simdatabase/bulge_disk_f8/bdf8_107.fits"
image="simdatabase/bulge_disk_f8/bdf8_108.fits"
image="simdatabase/bulge_disk_f8/bdf8_109.fits"
image="simdatabase/bulge_disk_f8/bdf8_110.fits"
image="simdatabase/bulge_disk_f8/bdf8_111.fits"
image="simdatabase/bulge_disk_f8/bdf8_112.fits"
image="simdatabase/bulge_disk_f8/bdf8_113.fits"
image="simdatabase/bulge_disk_f8/bdf8_114.fits"
image="simdatabase/bulge_disk_f8/bdf8_115.fits"
image="simdatabase/bulge_disk_f8/bdf8_116.fits"
image="simdatabase/bulge_disk_f8/bdf8_117.fits"
image="simdatabase/bulge_disk_f8/bdf8_118.fits"
image="simdatabase/bulge_disk_f8/bdf8_119.fits"
image="simdatabase/bulge_disk_f8/bdf8_120.fits"
image="simdatabase/bulge_disk_f8/bdf8_121.fits"
image="simdatabase/bulge_disk_f8/bdf8_122.fits"
image="simdatabase/bulge_disk_f8/bdf8_123.fits"
image="simdatabase/bulge_disk_f8/bdf8_124.fits"
image="simdatabase/bulge_disk_f8/bdf8_125.fits"
image="simdatabase/bulge_disk_f8/bdf8_126.fits"
image="simdatabase/bulge_disk_f8/bdf8_127.fits"
image="simdatabase/bulge_disk_f8/bdf8_128.fits"
image="simdatabase/bulge_disk_f8/bdf8_129.fits"
image="simdatabase/bulge_disk_f8/bdf8_130.fits"
image="simdatabase/bulge_disk_f8/bdf8_131.fits"
image="simdatabase/bulge_disk_f8/bdf8_132.fits"
image="simdatabase/bulge_disk_f8/bdf8_133.fits"
image="simdatabase/bulge_disk_f8/bdf8_134.fits"
image="simdatabase/bulge_disk_f8/bdf8_135.fits"
image="simdatabase/bulge_disk_f8/bdf8_136.fits"
image="simdatabase/bulge_disk_f8/bdf8_137.fits"
image="simdatabase/bulge_disk_f8/bdf8_138.fits"
image="simdatabase/bulge_disk_f8/bdf8_139.fits"
image="simdatabase/bulge_disk_f8/bdf8_140.fits"
image="simdatabase/bulge_disk_f8/bdf8_141.fits"
image="simdatabase/bulge_disk_f8/bdf8_142.fits"
image="simdatabase/bulge_disk_f8/bdf8_143.fits"
image="simdatabase/bulge_disk_f8/bdf8_144.fits"
image="simdatabase/bulge_disk_f8/bdf8_145.fits"
image="simdatabase/bulge_disk_f8/bdf8_146.fits"
image="simdatabase/bulge_disk_f8/bdf8_147.fits"
image="simdatabase/bulge_disk_f8/bdf8_148.fits"
image="simdatabase/bulge_disk_f8/bdf8_149.fits"
image="simdatabase/bulge_disk_f8/bdf8_150.fits"
image="simdatabase/bulge_disk_f8/bdf8_151.fits"
image="simdatabase/bulge_disk_f8/bdf8_152.fits"
image="simdatabase/bulge_disk_f8/bdf8_153.fits"
image="simdatabase/bulge_disk_f8/bdf8_154.fits"
image="simdatabase/bulge_disk_f8/bdf8_155.fits"
image="simdatabase/bulge_disk_f8/bdf8_156.fits"
image="simdatabase/bulge_disk_f8/bdf8_157.fits"
image="simdatabase/bulge_disk_f8/bdf8_158.fits"
image="simdatabase/bulge_disk_f8/bdf8_159.fits"
image="simdatabase/bulge_disk_f8/bdf8_160.fits"
image="simdatabase/bulge_disk_f8/bdf8_161.fits"
image="simdatabase/bulge_disk_f8/bdf8_162.fits"
image="simdatabase/bulge_disk_f8/bdf8_163.fits"
image="simdatabase/bulge_disk_f8/bdf8_164.fits"
image="simdatabase/bulge_disk_f8/bdf8_165.fits"
image="simdatabase/bulge_disk_f8/bdf8_166.fits"
image="simdatabase/bulge_disk_f8/bdf8_167.fits"
image="simdatabase/bulge_disk_f8/bdf8_168.fits"
image="simdatabase/bulge_disk_f8/bdf8_169.fits"
image="simdatabase/bulge_disk_f8/bdf8_170.fits"
image="simdatabase/bulge_disk_f8/bdf8_171.fits"
image="simdatabase/bulge_disk_f8/bdf8_172.fits"
image="simdatabase/bulge_disk_f8/bdf8_173.fits"
image="simdatabase/bulge_disk_f8/bdf8_174.fits"
image="simdatabase/bulge_disk_f8/bdf8_175.fits"
image="simdatabase/bulge_disk_f8/bdf8_176.fits"
image="simdatabase/bulge_disk_f8/bdf8_177.fits"
image="simdatabase/bulge_disk_f8/bdf8_178.fits"
image="simdatabase/bulge_disk_f8/bdf8_179.fits"
image="simdatabase/bulge_disk_f8/bdf8_180.fits"
image="simdatabase/bulge_disk_f8/bdf8_181.fits"
image="simdatabase/bulge_disk_f8/bdf8_182.fits"
image="simdatabase/bulge_disk_f8/bdf8_183.fits"
image="simdatabase/bulge_disk_f8/bdf8_184.fits"
image="simdatabase/bulge_disk_f8/bdf8_185.fits"
image="simdatabase/bulge_disk_f8/bdf8_186.fits"
image="simdatabase/bulge_disk_f8/bdf8_187.fits"
image="simdatabase/bulge_disk_f8/bdf8_188.fits"
image="simdatabase/bulge_disk_f8/bdf8_189.fits"
image="simdatabase/bulge_disk_f8/bdf8_190.fits"
image="simdatabase/bulge_disk_f8/bdf8_191.fits"
image="simdatabase/bulge_disk_f8/bdf8_192.fits"
image="simdatabase/bulge_disk_f8/bdf8_193.fits"
image="simdatabase/bulge_disk_f8/bdf8_194.fits"
image="simdatabase/bulge_disk_f8/bdf8_195.fits"
image="simdatabase/bulge_disk_f8/bdf8_196.fits"
image="simdatabase/bulge_disk_f8/bdf8_197.fits"
image="simdatabase/bulge_disk_f8/bdf8_198.fits"
image="simdatabase/bulge_disk_f8/bdf8_199.fits"
image="simdatabase/bulge_disk_f8/bdf8_200.fits"
