import tomosaic
import glob, os
import numpy as np
import pickle
try:
    from mosaic_meta import *
except:
    reader = open(os.path.join('tomosaic_misc', 'meta'), 'rb')
    prefix, file_grid, x_shift, y_shift = pickle.load(reader)
    reader.close()
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()


# ==========================================
blend_options = {'depth': 5,
                 'blur': 0.4}
source_folder = 'data_raw_1x'
ds = 1
# ==========================================



try:
    shift_grid = tomosaic.util.file2grid("shifts.txt")
    shift_grid = tomosaic.absolute_shift_grid(shift_grid, file_grid)
except:
    print('Refined shift is not provided. Using pre-set shift values. ')
    shift_grid = tomosaic.start_shift_grid(file_grid, x_shift, y_shift)

shift_grid = shift_grid / ds
print(shift_grid)

t0 = time.time()
tomosaic.total_fusion(source_folder, 'fulldata_flatcorr_1x', 'fulldata_flatcorr_1x.h5', file_grid,
                           shift_grid, blend_method='pyramid',
                           color_correction=False, blend_options=blend_options, dtype='float16')
print('Rank {}: total time: {} s.'.format(rank, time.time() - t0))
