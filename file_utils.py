import os
from glob import glob
import numpy as np 
import xlsxwriter
import pandas as pd

def get_xls_fname(save_dir=os.getcwd(),fname_str=None):
	assert fname_str is not None, "Pass a fname"
	if len(fname_str.split('.'))>1:
		name = ".".join(fname_str.split('.')[:-1])
		extension = fname_str.split('.')[-1]
		curr_files = glob(os.path.join(
					save_dir,'*{}*.{}'.format(name,extension)))
		num_files = len(curr_files)
		fname_new = "{}_{}.{}".format(".".join(fname_str.split('.')[:-1]),num_files+1,fname_str.split('.')[-1])
	else:
		curr_files = glob(os.path.join(
					save_dir,'*{}*'.format(fname_str)))
		num_files = len(curr_files)
		fname_new = "{}_{}".format(fname_str,num_files+1)
	return fname_new

def convert_np_to_pd(metric_arr,col_names=None,row_names=None):
	if col_names is None:
		col_names = list(range(metric_arr.shape[1]))
	if row_names is None:
		row_names = list(range(metric_arr.shape[0]))
	metric_df = pd.DataFrame(data=metric_arr, index=row_names, columns=col_names)
	return metric_df

def write_df_to_sheet(metric_df,save_dir=os.getcwd(),writer=None,fname_str='dendritic_dynamics_metrics.xlsx',sheet_name=None):
	if writer is None:
		fname = get_xls_fname(save_dir=save_dir,fname_str=fname_str)
		writer = pd.ExcelWriter(os.path.join(save_dir,fname),mode='w',
				engine='xlsxwriter')#,if_sheet_exists='new')
	if sheet_name is None:
		sheet_name = 'Sheet1'
	metric_df.to_excel(writer,sheet_name=sheet_name)
	writer.save()
	return writer

def get_df_per_tp(cell_over_time_arr,row_names,fname_str):
	col_names = list(range(len(cell_over_time_arr[0])))
	cell_over_time_df = convert_np_to_pd(cell_over_time_arr,col_names=col_names,row_names=row_names)
	cell_over_time_sheet = write_df_to_sheet(cell_over_time_df,fname_str=fname_str)
	return cell_over_time_sheet

def get_df_per_cell(percell_metric_arrs, row_names, col_names, metrics_df, fname_str):
	for metric_idx in range(len(percell_metric_arrs)):
		metric = percell_metric_arrs[metric_idx]
		col_name = col_names[metric_idx]
		metrics_df.insert(metric_idx, col_name, metric, True)
	metrics_per_cell_sheet = write_df_to_sheet(metrics_df, fname_str=fname_str)
	return metrics_per_cell_sheet

if __name__=='__main__':
	A1 = np.array([[1,2,3],[2,3,4]])
	A2 = np.array([[10,2,30],[20,30,4]])
	# tmp_fname = 'temp'
	breakpoint()
	A1_df = convert_np_to_pd(A1,col_names=['A','B','C'],row_names=['hehe','hihi'])
	A2_df = convert_np_to_pd(A2,col_names=['A','B','C'],row_names=['hehe','hihi'])
	writer = write_df_to_sheet(A1_df,fname_str='file1.xlsx')
	writer = write_df_to_sheet(A2_df,fname_str='file2.xlsx')

	# np.hstack or np.vstack or np.stack