#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AuTomo with Tomosaic.
"""

import tomosaic
import time
import os
import sys
import argparse
import pickle
try:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    name = MPI.Get_processor_name()
except:
    from tomosaic.util.pseudo import pseudo_comm
    comm = pseudo_comm()
    rank = 0
    size = 1


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("--ds", help="downsample levels, separated by comma",default='1')
    args = parser.parse_args()
    ds = args.ds
    ds = [int(i) for i in ds.split(',')]

    f_pattern = 1
    prefix = ''
    src_folder = '.'
    file_list = tomosaic.get_files(src_folder, prefix, type='h5')

    t0 = time.time()
    tomosaic.reorganize_dir(file_list, raw_ds=ds)

    print('Total time: {}s'.format(time.time() - t0))


if __name__ == "__main__":
    main(sys.argv[1:])
