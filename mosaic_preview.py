#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AuTomo with Tomosaic.
"""

import tomosaic
from tomosaic import *
from tomosaic.misc.misc import read_data_adaptive
import glob, os
import numpy as np
import dxchange
import tomopy
import sys
import argparse
from mosaic_meta import x_shift, y_shift

def preprocess(dat, blur=None):

    dat[np.abs(dat) < 2e-3] = 2e-3
    dat[dat > 1] = 1
    dat = -np.log(dat)
    dat[np.where(np.isnan(dat) == True)] = 0
    if blur is not None:
        dat = gaussian_filter(dat, blur)

    return dat

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("--src_folder", help="folder where the H5 files are located",default='data_raw_1x')
    parser.add_argument("--frame", help="frame to preview",default=None)   
    parser.add_argument("--pano", help="Preview Panorama",default=None)
    args = parser.parse_args()
    
    src_folder = args.src_folder

    method = 'pyramid'
    margin = 50
    pyramid_options = {'depth': 5,
                 'blur': 0.4}

    f_pattern = 1
    prefix = ''
    file_list = tomosaic.get_files(src_folder, prefix, type='h5')
    print(file_list)
    file_grid = tomosaic.start_file_grid(file_list, pattern=f_pattern)
    file_grid = np.fliplr(file_grid)
    print(file_grid)
    data_format = 'aps_32id'

    try:
        shift_grid = tomosaic.util.file2grid("shifts.txt")
        shift_grid = tomosaic.absolute_shift_grid(shift_grid, file_grid)
    except:
        print('Refined shift is not provided. Using pre-set shift values. ')
        shift_grid = tomosaic.start_shift_grid(file_grid, x_shift, y_shift)

    if(args.frame!=None):
        frame = int(args.frame)
        for f in file_list:
            dat, flt, drk, _ = read_data_adaptive(os.path.join(src_folder, f), proj=(frame, frame+1), data_format=data_format)
            #dat = tomopy.normalize(dat, flt, drk)
            #dat = tomopy.minus_log(dat)
            f = os.path.splitext(os.path.basename(f))[0]
            dxchange.write_tiff(flt.mean(0), os.path.join('preview_flats', f), dtype='float32', overwrite=True)
            dxchange.write_tiff(drk.mean(0), os.path.join('preview_darks', f), dtype='float32', overwrite=True)
            dxchange.write_tiff(dat, os.path.join('preview_frames', f), dtype='float32', overwrite=True)


    if(args.pano!=None):
        pano = int(args.pano)
        buff = build_panorama('data_raw_1x',file_grid,shift_grid.astype(int),frame=pano,data_format=data_format,
                              method=method, 
                              blend_options=pyramid_options)
        dxchange.write_tiff(buff, 'preview_panos/{}_norm'.format(pano), dtype='float32', overwrite=True)




if __name__ == "__main__":
    main(sys.argv[1:])
