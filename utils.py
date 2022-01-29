# This file contains functions to calculate types of segments!
import os,glob
import numpy as np
import math
import csv
import pandas as pd
import matplotlib.pyplot as plt

'''GLOBAL VARIABLES'''
_FIL_THRESHOLD_CONST = 10
_PERSISTENT_THRESHOLD_CONST = 4

'''SEGMENT CATEGORIES
segments (all)
filopodia
branches
new segments
transient segments
new and persistent segments
'''

def get_filopodia(data_arr, fil_threshold=_FIL_THRESHOLD_CONST):
	'''
	Returns masked array indicating filopodia
	Args:
		data_arr - np matrix with segment lengths per timepoint
		fil_threshold - segment length threshold for branch vs filopodia
	Output:
		fil_id - filopodia identity; fil = length, branch = 0, nan = nan
	'''
	fil_mask = data_arr > fil_threshold
	fil_id = data_arr.copy()
	fil_id[fil_mask] = 0
	return fil_id

def get_branches(data_arr, fil_threshold=_FIL_THRESHOLD_CONST):
	'''
	Returns masked array indicating branches
	Args:
		data_arr - np matrix with segment lengths per timepoint
		fil_threshold - segment length threshold for branch vs filopodia
	Output:
		branch_id - branch identity; fil = 0, branch = lengths, nan = nan
	'''
	branch_mask = data_arr<=fil_threshold
	branch_id = data_arr.copy()
	branch_id[branch_mask] = 0
	return branch_id

def get_new_segments(data_arr):
	'''
	Returns array with new segments
	Args:
		data_arr - np matrix with segment lengths per timepoint
	Output:
		new_segments_arr - np matrix with newly appearing segments only
	'''
	all_cols = list(range(data_arr.shape[1])) #all columns
	del_cols = np.where(data_arr[0]>0)[0] #tp0 columns with non-0 vals
	new_segments_idx = [i for i in all_cols if i not in del_cols]
	new_segments_arr = data_arr[:, new_segments_idx]
	return new_segments_arr

def get_transient_segments(data_arr):
	'''
	Returns array with transient segments
		(i.e. segments that appear and disappear during imaging)
	Args:
		data_arr - np matrix with segment lengths per timepoint
	Output:
		transient_segments_arr - np matrix with transient segments only 
			
	'''
	new_segments_arr = get_new_segments(data_arr=data_arr)
	new_cols = list(range(new_segments_arr.shape[1])) #all new segments
	del_cols = np.where(new_segments_arr[-1]>0)[0]
	transient_segments_idx = [i for i in new_cols if i not in del_cols]
	transient_segments_arr = new_segments_arr[:, transient_segments_idx]
	return transient_segments_arr

def get_new_pers_segments(data_arr, persistent_thresh=_PERSISTENT_THRESHOLD_CONST):
	'''
	Returns array with new and persistent segments
	(i.e. segments appear and lasting during imaging for at least last 4 timepoints)
	Args:
		data_arr - np matrix with segment lengths per timepoint
		persistent_thresh - end time window as persistent criteria
	Output:
		new_pers_segments_arr - np matrix with persistent segments only 
	'''
	new_segments_arr = get_new_segments(data_arr=data_arr)
	pers_segments_idx = np.where(np.isnan(new_segments_arr[-persistent_thresh:]).astype(int)==0)[1]
	pers_segments_idx = np.unique(pers_segments_idx)
	new_pers_segments_arr = new_segments_arr[:, pers_segments_idx]
	return new_pers_segments_arr

def get_perc_filtered_function(filtered_data_arr,original_data_arr=None):
	'''
	Returns percentile of filtered number of segments (or fil or branch) over total numer
	Args:
		filtered_data_arr - np matrix with filtered segments;
			filters are new, transient, new and persistent
	Output:
		perc_filtered_segments - # of new segments / all segments * 100percent
		perc_filtered_filopodia - 
		perc_filtered_branches -
	'''
	if original_data_arr is None:
		original_data_arr = filtered_data_arr.copy()

	OG_segment_num = len(original_data_arr[1])
	perc_filtered_segments = filtered_data_arr.shape[1] / OG_segment_num * 100

	OG_fil_arr = get_filopodia(data_arr=original_data_arr)
	OG_fil_num = len(np.unique(np.where(OG_fil_arr>0)[1]))
	filtered_fil_arr = get_filopodia(data_arr=filtered_data_arr)
	filtered_fil_num = len(np.unique(np.where(filtered_fil_arr>0)[1]))
	perc_filtered_fil = filtered_fil_num / OG_fil_num * 100

	OG_branch_arr = get_branches(data_arr=original_data_arr)
	OG_branch_num = len(np.unique(np.where(OG_branch_arr>0)[1]))
	filtered_branch_arr = get_branches(data_arr=filtered_data_arr)
	filtered_branch_num = len(np.unique(np.where(filtered_branch_arr>0)[1]))
	perc_filtered_branch = filtered_branch_num / OG_branch_num * 100

	return perc_filtered_segments, perc_filtered_fil, perc_filtered_branch 

if __name__=='__main__':
	A1 = np.array([[20, 11, 5, np.nan, np.nan], [22, 13, 7, 8, np.nan], [25, 12, 7, 10, 1], [27, np.nan, np.nan, 10, 2]])
	breakpoint()
	tmp = get_filopodia(A1)
