import os
from glob import glob
import xlsxwriter

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 

from utils import *
from file_utils import *
from metrics import *

data_folder = os.getcwd()
data_folder = os.path.join('C:',os.sep,'Users','zchor','D-serine dynamics analysis 2')
save_dir = os.getcwd()
files = glob.glob(os.path.join(data_folder,'*.csv'))
fnames = [os.path.basename(f) for f in files]

segment_num_pertp_arr = []
fil_num_pertp_arr = []
branch_num_pertp_arr = []

added_arr = []
lost_arr = []
fil_added_arr = []
fil_lost_arr = []
branch_added_arr = []
branch_lost_arr = []
fil_to_branch_arr = []
segment_density_pertp_arr = []
fil_density_pertp_arr = []
branch_density_pertp_arr = []

arbor_lengths_arr = []
elongations_arr = []
retractions_arr = []
motility_arr = []

fil_arbor_lengths_arr = []
fil_elongations_arr = []
fil_retractions_arr = []
fil_motility_arr = []

branch_arbor_lengths_arr = []
branch_elongations_arr = []
branch_retractions_arr = []
branch_motility_arr = []

added_dens_arr = []
lost_dens_arr = []
fil_added_dens_arr = []
fil_lost_dens_arr = []
branch_added_dens_arr = []
branch_lost_dens_arr = []
fil_to_branch_dens_arr = []
elongations_norm_to_len_arr = []
retractions_norm_to_len_arr = []
motility_norm_to_len_arr = []
fil_elongations_norm_to_len_arr = []
fil_retractions_norm_to_len_arr = []
fil_motility_norm_to_len_arr = []
branch_elongations_norm_to_len_arr = []
branch_retractions_norm_to_len_arr = []
branch_motility_norm_to_len_arr = []

percell_segment_lifetime_arr = []
percell_new_segment_lifetime_arr = []
percell_transient_segment_lifetime_arr = []
percell_new_pers_segment_lifetime_arr = []
percell_new_perc_filtered_segments_arr = []
percell_transient_perc_filtered_segments_arr = []
percell_new_pers_perc_filtered_segments_arr = []

percell_fil_lifetime_arr = []
percell_new_fil_lifetime_arr = []
percell_transient_fil_lifetime_arr = []
percell_new_pers_fil_lifetime_arr = []
percell_new_perc_filtered_fil_arr = []
percell_transient_perc_filtered_fil_arr = []
percell_new_pers_perc_filtered_fil_arr = []

percell_branch_lifetime_arr = []
percell_new_branch_lifetime_arr = []
percell_transient_branch_lifetime_arr = []
percell_new_pers_branch_lifetime_arr = []
percell_new_perc_filtered_branch_arr = []
percell_transient_perc_filtered_branch_arr = []
percell_new_pers_perc_filtered_branch_arr = []

for cell in files:
	print(cell)
	
	data_arr_from_csv = np.genfromtxt(cell, delimiter=',')	
	notnan_idx = np.unique(np.where(np.isnan(data_arr_from_csv[:]).astype(int)==0)[1])
	data_arr = data_arr_from_csv[:, notnan_idx]

	arbor_lengths, elongations, retractions, motility = get_motility_metrics(data_arr)
	arbor_lengths_arr.append(arbor_lengths)
	elongations_arr.append(elongations)
	elongations_norm_to_len = elongations / arbor_lengths[0]
	elongations_norm_to_len_arr.append(elongations_norm_to_len)
	retractions_arr.append(retractions)
	retractions_norm_to_len = retractions / arbor_lengths[0]
	retractions_norm_to_len_arr.append(retractions_norm_to_len)
	motility_arr.append(motility)
	motility_norm_to_len = motility / arbor_lengths[0]
	motility_norm_to_len_arr.append(motility_norm_to_len)

	added = get_added_metric(data_arr)
	added_arr.append(added)
	added_dens = added / arbor_lengths[0]
	added_dens_arr.append(added_dens)

	lost = get_lost_metric(data_arr)
	lost_arr.append(lost)
	lost_dens = lost / arbor_lengths[0]
	lost_dens_arr.append(lost_dens)

	fil_added, fil_lost, branch_added, branch_lost, fil_to_branch = get_fil_to_branch_metric(data_arr)
	fil_added_arr.append(fil_added)
	fil_lost_arr.append(fil_lost)
	branch_added_arr.append(branch_added)
	branch_lost_arr.append(branch_lost)
	fil_to_branch_arr.append(fil_to_branch)

	fil_added_dens = fil_added / arbor_lengths[0]
	fil_added_dens_arr.append(fil_added_dens)
	fil_lost_dens = fil_lost / arbor_lengths[0]
	fil_lost_dens_arr.append(fil_lost_dens)
	branch_added_dens = branch_added / arbor_lengths[0]
	branch_added_dens_arr.append(branch_added_dens)
	branch_lost_dens = branch_lost / arbor_lengths[0]
	branch_lost_dens_arr.append(branch_lost_dens)
	fil_to_branch_dens = fil_to_branch / arbor_lengths[0]
	fil_to_branch_dens_arr.append(fil_to_branch_dens)

	fil_arr = get_filopodia(data_arr)
	fil_arbor_lengths, fil_elongations, fil_retractions, fil_motility = get_motility_metrics(data_arr=fil_arr)
	fil_arbor_lengths_arr.append(fil_arbor_lengths)
	fil_elongations_arr.append(fil_elongations)
	fil_retractions_arr.append(fil_retractions)
	fil_motility_arr.append(fil_motility)

	fil_elongations_arr.append(fil_elongations)
	fil_elongations_norm_to_len = fil_elongations / arbor_lengths[0]
	fil_elongations_norm_to_len_arr.append(fil_elongations_norm_to_len)
	fil_retractions_arr.append(fil_retractions)
	fil_retractions_norm_to_len = fil_retractions / arbor_lengths[0]
	fil_retractions_norm_to_len_arr.append(fil_retractions_norm_to_len)
	fil_motility_arr.append(fil_motility)
	fil_motility_norm_to_len = fil_motility / arbor_lengths[0]
	fil_motility_norm_to_len_arr.append(fil_motility_norm_to_len)

	branch_arr = get_branches(data_arr)
	branch_arbor_lengths, branch_elongations, branch_retractions, branch_motility = get_motility_metrics(data_arr=branch_arr)
	branch_arbor_lengths_arr.append(branch_arbor_lengths)
	branch_elongations_arr.append(branch_elongations)
	branch_retractions_arr.append(branch_retractions)
	branch_motility_arr.append(branch_motility)

	branch_elongations_arr.append(branch_elongations)
	branch_elongations_norm_to_len = branch_elongations / arbor_lengths[0]
	branch_elongations_norm_to_len_arr.append(branch_elongations_norm_to_len)
	branch_retractions_arr.append(branch_retractions)
	branch_retractions_norm_to_len = branch_retractions / arbor_lengths[0]
	branch_retractions_norm_to_len_arr.append(branch_retractions_norm_to_len)
	branch_motility_arr.append(branch_motility)
	branch_motility_norm_to_len = branch_motility / arbor_lengths[0]
	branch_motility_norm_to_len_arr.append(branch_motility_norm_to_len)

	segment_lifetime_arr, segment_lifetime, fil_lifetime_arr, fil_lifetime, branch_lifetime_arr, branch_lifetime = get_lifetimes_metric(data_arr)
	new_segment_lifetime_arr, new_segment_lifetime, new_fil_lifetime_arr, new_fil_lifetime, new_branch_lifetime_arr, new_branch_lifetime = get_new_lifetimes_metric(data_arr)
	transient_segment_lifetime_arr, transient_segment_lifetime, transient_fil_lifetime_arr, transient_fil_lifetime, transient_branch_lifetime_arr, transient_branch_lifetime = get_transient_lifetimes_metric(data_arr)
	new_pers_segment_lifetime_arr, new_pers_segment_lifetime, new_pers_fil_lifetime_arr, new_pers_fil_lifetime, new_pers_branch_lifetime_arr, new_pers_branch_lifetime = get_new_pers_lifetimes_metric(data_arr)
	
	percell_segment_lifetime_arr.append(segment_lifetime)
	percell_new_segment_lifetime_arr.append(segment_lifetime)
	percell_transient_segment_lifetime_arr.append(transient_segment_lifetime)
	percell_new_pers_segment_lifetime_arr.append(new_pers_segment_lifetime)

	percell_fil_lifetime_arr.append(fil_lifetime)
	percell_new_fil_lifetime_arr.append(fil_lifetime)
	percell_transient_fil_lifetime_arr.append(transient_fil_lifetime)
	percell_new_pers_fil_lifetime_arr.append(new_pers_fil_lifetime)

	percell_branch_lifetime_arr.append(branch_lifetime)
	percell_new_branch_lifetime_arr.append(branch_lifetime)
	percell_transient_branch_lifetime_arr.append(transient_branch_lifetime)
	percell_new_pers_branch_lifetime_arr.append(new_pers_branch_lifetime)

	arbor_lengths_pertp, segment_num_pertp, fil_num_pertp, branch_num_pertp, segment_density_pertp, fil_density_pertp, branch_density_pertp = get_density_per_tp_metrics(data_arr)
	segment_num_pertp_arr.append(segment_num_pertp)
	fil_num_pertp_arr.append(fil_num_pertp)
	branch_num_pertp_arr.append(branch_num_pertp)
	segment_density_pertp_arr.append(segment_density_pertp)
	fil_density_pertp_arr.append(fil_density_pertp)
	branch_density_pertp_arr.append(branch_density_pertp)

	new_perc_filtered_segments, new_perc_filtered_fil, new_perc_filtered_branch, transient_perc_filtered_segments, transient_perc_filtered_fil, transient_perc_filtered_branch, new_pers_perc_filtered_segments, new_pers_perc_filtered_fil, new_pers_perc_filtered_branch = get_perc_filtered_metrics(data_arr)
	percell_new_perc_filtered_segments_arr.append(new_perc_filtered_segments)
	percell_transient_perc_filtered_segments_arr.append(transient_perc_filtered_segments)
	percell_new_pers_perc_filtered_segments_arr.append(new_pers_perc_filtered_segments)
	percell_new_perc_filtered_fil_arr.append(new_perc_filtered_fil)
	percell_transient_perc_filtered_fil_arr.append(transient_perc_filtered_fil)
	percell_new_pers_perc_filtered_fil_arr.append(new_pers_perc_filtered_fil)
	percell_new_perc_filtered_branch_arr.append(new_perc_filtered_branch)
	percell_transient_perc_filtered_branch_arr.append(transient_perc_filtered_branch)
	percell_new_pers_perc_filtered_branch_arr.append(new_pers_perc_filtered_branch)

'''PER TIMEPOINT 
Results will be a data matrix with rows=timepoint, columns=unique segments'''

segment_num_pertp_sheet = get_df_per_tp(cell_over_time_arr=segment_num_pertp_arr, row_names = fnames, fname_str='segment_num_pertp_per_tp.xlsx')
fil_num_pertp_sheet = get_df_per_tp(cell_over_time_arr=fil_num_pertp_arr, row_names = fnames, fname_str='fil_num_pertp_per_tp.xlsx')
branch_num_pertp_sheet = get_df_per_tp(cell_over_time_arr=branch_num_pertp_arr, row_names = fnames, fname_str='branch_num_pertp_per_tp.xlsx')

added_sheet = get_df_per_tp(cell_over_time_arr=added_arr, row_names=fnames, fname_str='added_per_tp.xlsx')
lost_sheet = get_df_per_tp(cell_over_time_arr=lost_arr, row_names=fnames, fname_str='lost_per_tp.xlsx')
fil_added_sheet = get_df_per_tp(cell_over_time_arr=fil_added_arr, row_names=fnames, fname_str='fil_added_per_tp.xlsx')
fil_lost_sheet = get_df_per_tp(cell_over_time_arr=fil_lost_arr, row_names=fnames, fname_str='fil_lost_per_tp.xlsx')
branch_added_sheet = get_df_per_tp(cell_over_time_arr=branch_added_arr, row_names=fnames, fname_str='branch_added_per_tp.xlsx')
branch_lost_sheet = get_df_per_tp(cell_over_time_arr=branch_lost_arr, row_names=fnames, fname_str='branch_lost_per_tp.xlsx')
fil_to_branch_sheet = get_df_per_tp(cell_over_time_arr=fil_to_branch_arr, row_names=fnames, fname_str='fil_to_branch_per_tp.xlsx')

segment_density_pertp_sheet = get_df_per_tp(cell_over_time_arr=segment_density_pertp_arr, row_names = fnames, fname_str='segment_density_pertp_per_tp.xlsx')
fil_density_pertp_sheet = get_df_per_tp(cell_over_time_arr=fil_density_pertp_arr, row_names = fnames, fname_str='fil_density_pertp_per_tp.xlsx')
branch_density_pertp_sheet = get_df_per_tp(cell_over_time_arr=branch_density_pertp_arr, row_names = fnames, fname_str='branch_density_pertp_per_tp.xlsx')

arbor_lengths_sheet = get_df_per_tp(cell_over_time_arr=arbor_lengths_arr, row_names = fnames, fname_str='arbor_lengths_per_tp.xlsx')
elongations_sheet = get_df_per_tp(cell_over_time_arr=elongations_arr, row_names = fnames, fname_str='elongations_per_tp.xlsx')
retractions_sheet = get_df_per_tp(cell_over_time_arr=retractions_arr, row_names = fnames, fname_str='retractions_per_tp.xlsx')
motility_sheet = get_df_per_tp(cell_over_time_arr=motility_arr, row_names = fnames, fname_str='motility_per_tp.xlsx')

fil_arbor_lengths_sheet = get_df_per_tp(cell_over_time_arr=fil_arbor_lengths_arr, row_names = fnames, fname_str='fil_arbor_lengths_per_tp.xlsx')
fil_elongations_sheet = get_df_per_tp(cell_over_time_arr=fil_elongations_arr, row_names = fnames, fname_str='fil_elongations_per_tp.xlsx')
fil_retractions_sheet = get_df_per_tp(cell_over_time_arr=fil_retractions_arr, row_names = fnames, fname_str='fil_retractions_per_tp.xlsx')
fil_motility_sheet = get_df_per_tp(cell_over_time_arr=fil_motility_arr, row_names = fnames, fname_str='fil_motility_per_tp.xlsx')

branch_arbor_lengths_sheet = get_df_per_tp(cell_over_time_arr=branch_arbor_lengths_arr, row_names = fnames, fname_str='branch_arbor_lengths_per_tp.xlsx')
branch_elongations_sheet = get_df_per_tp(cell_over_time_arr=branch_elongations_arr, row_names = fnames, fname_str='branch_elongations_per_tp.xlsx')
branch_retractions_sheet = get_df_per_tp(cell_over_time_arr=branch_retractions_arr, row_names = fnames, fname_str='branch_retractions_per_tp.xlsx')
branch_motility_sheet = get_df_per_tp(cell_over_time_arr=branch_motility_arr, row_names = fnames, fname_str='branch_motility_per_tp.xlsx')

'''PER TIMEPOINT as DENSITY MEASURES'''

added_dens_sheet = get_df_per_tp(cell_over_time_arr=added_dens_arr, row_names=fnames, fname_str='added_dens_per_tp.xlsx')
lost_dens_sheet = get_df_per_tp(cell_over_time_arr=lost_dens_arr, row_names=fnames, fname_str='lost_dens_per_tp.xlsx')
fil_added_dens_dens_sheet = get_df_per_tp(cell_over_time_arr=fil_added_dens_arr, row_names=fnames, fname_str='fil_added_dens_per_tp.xlsx')
fil_lost_dens_sheet = get_df_per_tp(cell_over_time_arr=fil_lost_dens_arr, row_names=fnames, fname_str='fil_lost_dens_per_tp.xlsx')
branch_added_dens_sheet = get_df_per_tp(cell_over_time_arr=branch_added_dens_arr, row_names=fnames, fname_str='branch_added_dens_per_tp.xlsx')
branch_lost_dens_sheet = get_df_per_tp(cell_over_time_arr=branch_lost_dens_arr, row_names=fnames, fname_str='branch_lost_dens_per_tp.xlsx')
fil_to_branch_dens_sheet = get_df_per_tp(cell_over_time_arr=fil_to_branch_dens_arr, row_names=fnames, fname_str='fil_to_branch_dens_per_tp.xlsx')

elongations_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=elongations_norm_to_len_arr, row_names = fnames, fname_str='elongations_norm_to_len_per_tp.xlsx')
retractions_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=retractions_norm_to_len_arr, row_names = fnames, fname_str='retractions_norm_to_len_per_tp.xlsx')
motility_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=motility_norm_to_len_arr, row_names = fnames, fname_str='motility_norm_to_len_per_tp.xlsx')
fil_elongations_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=fil_elongations_norm_to_len_arr, row_names = fnames, fname_str='fil_elongations_norm_to_len_per_tp.xlsx')
fil_retractions_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=fil_retractions_norm_to_len_arr, row_names = fnames, fname_str='fil_retractions_norm_to_len_per_tp.xlsx')
fil_motility_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=fil_motility_norm_to_len_arr, row_names = fnames, fname_str='fil_motility_norm_to_len_per_tp.xlsx')
branch_elongations_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=branch_elongations_norm_to_len_arr, row_names = fnames, fname_str='branch_elongations_norm_to_len_per_tp.xlsx')
branch_retractions_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=branch_retractions_norm_to_len_arr, row_names = fnames, fname_str='branch_retractions_norm_to_len_per_tp.xlsx')
branch_motility_norm_to_len_sheet = get_df_per_tp(cell_over_time_arr=branch_motility_norm_to_len_arr, row_names = fnames, fname_str='branch_motility_norm_to_len_per_tp.xlsx')

'''PER CELL
Results will be a single measure per cell'''
row_names = fnames

'All Segments'
all_segments_metrics_per_cell_df = pd.DataFrame(data=percell_segment_lifetime_arr, index=fnames, columns=['segment_lifetime'])
percell_segments_metric_arrs = [percell_new_segment_lifetime_arr, percell_transient_segment_lifetime_arr, percell_new_pers_segment_lifetime_arr, percell_new_perc_filtered_segments_arr, percell_transient_perc_filtered_segments_arr, percell_new_pers_perc_filtered_segments_arr]
segments_col_names = ['new_segment_lifetime', 'transient_segment_lifetime', 'new_pers_segment_lifetime', 'new_perc_filtered_segments', 'transient_perc_filtered_segments', 'new_pers_perc_filtered_segments']
all_segments_metrics_per_cell_sheet = get_df_per_cell(percell_metric_arrs=percell_segments_metric_arrs, row_names=fnames, col_names=segments_col_names, metrics_df=all_segments_metrics_per_cell_df, fname_str='percell_segments_metrics.xlsx')

'Filopodia'
fil_metrics_per_cell_df = pd.DataFrame(data=percell_fil_lifetime_arr, index=fnames, columns=['fil_lifetime'])
percell_fil_metric_arrs = [percell_new_fil_lifetime_arr, percell_transient_fil_lifetime_arr, percell_new_pers_fil_lifetime_arr, percell_new_perc_filtered_fil_arr, percell_transient_perc_filtered_fil_arr, percell_new_pers_perc_filtered_fil_arr]
fil_col_names = ['new_fil_lifetime', 'transient_fil_lifetime', 'new_pers_fil_lifetime', 'new_perc_filtered_fil', 'transient_perc_filtered_fil', 'new_pers_perc_filtered_fil']
fil_metrics_per_cell_sheet = get_df_per_cell(percell_metric_arrs=percell_fil_metric_arrs, row_names=fnames, col_names=fil_col_names, metrics_df=fil_metrics_per_cell_df, fname_str='percell_filopodia_metrics.xlsx')

'Branches'
branch_metrics_per_cell_df = pd.DataFrame(data=percell_branch_lifetime_arr, index=fnames, columns=['branch_lifetime'])
percell_branch_metric_arrs = [percell_new_branch_lifetime_arr, percell_transient_branch_lifetime_arr, percell_new_pers_branch_lifetime_arr, percell_new_perc_filtered_branch_arr, percell_transient_perc_filtered_branch_arr, percell_new_pers_perc_filtered_branch_arr]
branch_col_names = ['new_branch_lifetime', 'transient_branch_lifetime', 'new_pers_branch_lifetime', 'new_perc_filtered_branch', 'transient_perc_filtered_branch', 'new_pers_perc_filtered_branch']
branch_metrics_per_cell_sheet = get_df_per_cell(percell_metric_arrs=percell_branch_metric_arrs, row_names=fnames, col_names=branch_col_names, metrics_df=branch_metrics_per_cell_df, fname_str='percell_branch_metrics.xlsx')

