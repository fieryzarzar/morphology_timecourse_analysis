# This file contains functions to calculate the different metrics!
import os,glob
import numpy as np
import math
import csv
import pandas as pd
import matplotlib.pyplot as plt
from utils import *

'''METRICS 
segments added
segments lost
filopodia to branch 
lifetimes: segments, filopodia, branches
- new lifetimes
- transient lifetimes
- new and persistent lifetimes

'''

def get_added_metric(data_arr):
	'''
	Returns added segments
	Args:
		data_arr - np matrix with segment lengths per timepoint
	Output:
		added - shape: len(data_arr)-1 
	'''
	pos_mask = (data_arr>0).astype(int)
	change_arr = np.diff(pos_mask, axis=0)
	add_arr = (change_arr>0).astype(int)
	added = np.sum(add_arr,axis=1)
	return added

def get_lost_metric(data_arr):
	'''
	Returns lost segments
	Args:
		data_arr - np matrix with segment lengths per timepoint
	Output:
		lost - shape: len(data_arr)-1 
	'''
	pos_mask = (data_arr>0).astype(int)
	change_arr = np.diff(pos_mask, axis=0)
	lost_arr = (change_arr<0).astype(int)
	lost = np.sum(lost_arr,axis=1)
	return lost

def get_fil_to_branch_metric(data_arr):
	'''
	Returns when filopodia became branches
	Args:
		data_arr - np matrix with segment lengths per timepoint
	Output:
		added - shape: len(data_arr)-1 
	'''
	fil_arr = get_filopodia(data_arr=data_arr)
	fil_exists = (fil_arr>0).astype(int)
	change_arr = np.diff(fil_exists, axis=0)
	fil_added_arr = (change_arr>0).astype(int)
	fil_added = np.nansum(fil_added_arr, axis=1)
	fil_lost_arr = (change_arr<0).astype(int)
	fil_lost = np.nansum(fil_lost_arr, axis=1)

	branch_arr = get_branches(data_arr=data_arr)
	branch_exists = (branch_arr>0).astype(int)
	change_arr = np.diff(branch_exists, axis=0)
	branch_added_arr = (change_arr>0).astype(int)
	branch_added = np.nansum(branch_added_arr, axis=1)
	branch_lost_arr = (change_arr<0).astype(int)
	branch_lost = np.nansum(branch_lost_arr, axis=1)

	fil_to_branch_arr = fil_lost_arr * branch_added_arr
	fil_to_branch = np.sum(fil_to_branch_arr, axis=1)
	
	return fil_added, fil_lost, branch_added, branch_lost, fil_to_branch

def get_lifetimes_metric(data_arr):
	'''
	Returns segment lifetimes
	Args:
		data_arr - np matrix with segment lengths per timepoint
		count_till - timepoint before which lifetime calculation is performed
	Output:
		segment, filopodia, branch + ...
		_lifetime_arr - np array with how long it was present
		_lifetimes - mean lifetime for that cell
	'''
	segment_lifetime_arr = np.nansum(data_arr>0, axis=0)
	segment_lifetime = np.nanmean(segment_lifetime_arr)

	fil_arr = get_filopodia(data_arr=data_arr)
	fil_lifetime_arr = np.nansum(fil_arr>0, axis=0)
	fil_lifetime = np.nanmean(fil_lifetime_arr)

	branch_arr = get_branches(data_arr=data_arr)
	branch_lifetime_arr = np.nansum(branch_arr>0, axis=0)
	branch_lifetime = np.nanmean(branch_lifetime_arr)

	return segment_lifetime_arr, segment_lifetime, fil_lifetime_arr, fil_lifetime, branch_lifetime_arr, branch_lifetime

def get_new_lifetimes_metric(data_arr):
	'''
	Returns lifetimes using get_lifetimes_metric fx but only for 
		new segments (get_new_segments fx in utils.py)
	'''
	new_segments_arr = get_new_segments(data_arr=data_arr)
	new_segment_lifetime_arr, new_segment_lifetime, new_fil_lifetime_arr, new_fil_lifetime, new_branch_lifetime_arr, new_branch_lifetime = get_lifetimes_metric(
		data_arr=new_segments_arr)
	return new_segment_lifetime_arr, new_segment_lifetime, new_fil_lifetime_arr, new_fil_lifetime, new_branch_lifetime_arr, new_branch_lifetime

def get_transient_lifetimes_metric(data_arr):
	'''
	Returns lifetimes using get_lifetimes_metric function but only for 
		transient segments (get_new_segments fx in utils.py)
	'''
	transient_segments_arr = get_transient_segments(data_arr=data_arr)
	res = get_lifetimes_metric(data_arr=transient_segments_arr)
	transient_segment_lifetime_arr = res[0]
	transient_segment_lifetime = res[1]
	transient_fil_lifetime_arr = res[2]
	transient_fil_lifetime = res[3]
	transient_branch_lifetime_arr = res[4]
	transient_branch_lifetime = res[5]		
	return transient_segment_lifetime_arr, transient_segment_lifetime, transient_fil_lifetime_arr, transient_fil_lifetime, transient_branch_lifetime_arr, transient_branch_lifetime

def get_new_pers_lifetimes_metric(data_arr):
	'''
	Returns lifetimes using get_lifetimes_metric function but only for segments 
		that appeared during the imaging period (i.e. after tp0) and lasted till
		the end of the imaging period (for at least last 4 tps)
	'''
	new_pers_segments_arr = get_new_pers_segments(data_arr=data_arr)
	res = get_lifetimes_metric(data_arr=new_pers_segments_arr)
	new_pers_segment_lifetime_arr = res[0]
	new_pers_segment_lifetime = res[1]
	new_pers_fil_lifetime_arr = res[2]
	new_pers_fil_lifetime = res[3]
	new_pers_branch_lifetime_arr = res[4]
	new_pers_branch_lifetime = res[5]		
	return new_pers_segment_lifetime_arr, new_pers_segment_lifetime, new_pers_fil_lifetime_arr, new_pers_fil_lifetime, new_pers_branch_lifetime_arr, new_pers_branch_lifetime

def get_density_per_tp_metrics(data_arr):
	'''
	Returns number density of segments, filopodia, and branches
		for every timepoint
	Args:
		data_arr - np matrix with segment lengths per timepoint
	Output:
		arbor_lengths_pertp
		segment_num_pertp
		fil_num_pertp
		branch_num_pertp
		segment_density_pertp
		fil_density_pertp
		branch_density_pertp
	'''
	arbor_lengths_pertp = np.nansum(data_arr, axis=1)

	segment_num_pertp = np.nansum(data_arr>0, axis=1)

	fil_arr = get_filopodia(data_arr=data_arr)
	fil_num_pertp = np.nansum(fil_arr>0, axis=1)

	branch_arr = get_branches(data_arr=data_arr)
	branch_num_pertp = np.nansum(branch_arr>0, axis=1)

	segment_density_pertp = segment_num_pertp / arbor_lengths_pertp
	fil_density_pertp = fil_num_pertp / arbor_lengths_pertp
	branch_density_pertp = branch_num_pertp / arbor_lengths_pertp

	return arbor_lengths_pertp, segment_num_pertp, fil_num_pertp, branch_num_pertp, segment_density_pertp, fil_density_pertp, branch_density_pertp

def get_perc_filtered_metrics(data_arr):
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
	new_segments_arr = get_new_segments(data_arr)
	new_perc_filtered_segments, new_perc_filtered_fil, new_perc_filtered_branch = get_perc_filtered_function(
		filtered_data_arr=new_segments_arr, original_data_arr=data_arr)

	transient_segments_arr = get_transient_segments(data_arr)
	transient_perc_filtered_segments, transient_perc_filtered_fil, transient_perc_filtered_branch = get_perc_filtered_function(
		filtered_data_arr=transient_segments_arr, original_data_arr=data_arr)

	new_pers_segments_arr = get_new_pers_segments(data_arr)
	new_pers_perc_filtered_segments, new_pers_perc_filtered_fil, new_pers_perc_filtered_branch = get_perc_filtered_function(
		filtered_data_arr=new_pers_segments_arr, original_data_arr=data_arr)

	return (new_perc_filtered_segments, new_perc_filtered_fil, new_perc_filtered_branch,
		transient_perc_filtered_segments, transient_perc_filtered_fil, transient_perc_filtered_branch,
		new_pers_perc_filtered_segments, new_pers_perc_filtered_fil, new_pers_perc_filtered_branch)

def get_motility_metrics(data_arr):
	'''
	Returns motility 
	Args:
		data_arr - np matrix with segment lengths per timepoint
	Output:
		elongations - elongations between subsequent timepoints
		retractions - retractions between subsequent timepoints
		motility - sum of abs elongations and retractions
	'''
	arbor_lengths = np.nansum(data_arr, axis=1)
	nonan_data_arr = np.nan_to_num(data_arr)
	change_arr = np.diff(nonan_data_arr, axis=0)
	elongations = np.nansum(change_arr*(change_arr>0), axis=1)
	retractions = np.abs(np.nansum(change_arr*(change_arr<0), axis=1))
	motility = elongations + retractions
	
	return arbor_lengths, elongations, retractions, motility

if __name__=='__main__':
	A1 = np.array([[20, 11, 5, np.nan, np.nan], [22, 13, 7, 8, np.nan], [25, 12, 7, 10, 1], [27, np.nan, np.nan, 10, 2]])
	breakpoint()
	tmp = get_motility_metrics(A1)