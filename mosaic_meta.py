import tomosaic
import pickle
import os
from mpi4py import MPI
import pickle

prefix = 'Ming_Charcoal_25kev_lens10x_dfocus12cm_180'
file_list = tomosaic.get_files('data_raw_1x', prefix, type='h5')
file_grid = tomosaic.start_file_grid(file_list, pattern=1)
data_format = 'aps_32id'
x_shift = 1560
y_shift = 996

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

try:
    os.mkdir('tomosaic_misc')
except:
    pass
writer = open(os.path.join('tomosaic_misc', 'meta'), 'wb')
pickle.dump([prefix, file_grid, x_shift, y_shift], writer)
writer.close()
