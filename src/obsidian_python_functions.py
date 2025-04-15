import numpy as np
from helper_functions import *

expected_fields__sim_res_signal_file = ['quality:: ', 'notes:: ']
default_fields__sim_res_signal_file = ['#sig_qual/', '']


def get_fields_from_Obsidian_note(path_embedded_reference, look_for_fields):
	
	fields = ['' for _ in look_for_fields]
	
	with open(path_embedded_reference, 'r', encoding='utf8') as file:
		lines = file.readlines()

	for i, field in enumerate(look_for_fields):
		for line in lines:
			if line.startswith(field):
				fields[i] = line.replace(field, '').replace('\n', '').strip()
				break
				
	return fields


def replace_fields_in_Obsidian_note(path_embedded_reference, look_for_fields, new_values):
	"""
	Replace the values of specified fields in an Obsidian note with new values.

	:param path_embedded_reference: Path to the Obsidian note file.
	:param look_for_fields: A list of field names to search for.
	:param new_values: A list of new values to replace the field values with.
	"""
	
	# Ensure we have the same number of fields and values to replace
	if len(look_for_fields) != len(new_values):
		raise ValueError("The number of fields and new values must be the same.")
	
	# Read the content of the file
	with open(path_embedded_reference, 'r', encoding='utf8') as file:
		lines = file.readlines()

	# Modify the lines where the fields are found
	for i, field in enumerate(look_for_fields):
		for j, line in enumerate(lines):
			if line.startswith(field):
				# Replace the field value with the new one
				lines[j] = f"{field} {new_values[i]}\n"
				break

	# Write the updated content back to the file
	with open(path_embedded_reference, 'w', encoding='utf8') as file:
		file.writelines(lines)

def write_Obsidian_table(table, return_lines = True):
	'''
	# Example
	table = {
		0: {1: 'col_1_title',
			2: 'col_2_title',
			3: 'col_3_title',
			4: 'col_4_title'
		},
		1: {1: 'r1c1',
			2: 'r1c2',
			3: 'r1c3'
		},
		2: {1: 'r2c1',
			2: 'r2c2',
			3: 'r3c2',
			4: 'r4c2'}
	}
	write_Obsidian_table(table)
	'''
	
	if not isinstance(table, dict):
		raise Exception('`table` input must be a dict!')
	
	cols = np.max([len(list(table[i].keys())) for i in list(table.keys())])
	rows = len(table.keys())
	lines = []
	keys = list(table.keys())
	if 0 in keys:
		# has column titles
		lines.append('| '+' | '.join([f'**{table[0][key]}**' for key in table[0].keys()]) + ' |')
	else:
		lines.append(''.join('| '*cols) + '|')

	lines.append(''.join('| --- '*cols) + '|')
	
	for i in keys:
		if i!=0:
			lines.append('| '+' | '.join([table[i][key] for key in table[i].keys()]) + ' |')
			lines[-1] += ' |'*(cols-len(table[i].keys()))
	
	if return_lines: 
		return [l + '\n' for l in lines]
	return '\n'.join(lines)

def write_obsidian_sim_parameter_file(PARS_PRINT, PATHS, sim_name):
	flat_dict = flatten_dict(PARS_PRINT)
	lines = [f'{f_key}:: {flat_dict[f_key]}' for f_key in flat_dict.keys()]
	with open(f'{PATHS['path_Obsidian_vault']}{PATHS['path_results_print_objects']}{sim_name}__pars_print.md', 'w', encoding='utf8') as file:
		file.writelines('\n'.join(lines)) 



# filenameSave1 = path_project_plots + signal_name
# figure_file_no_ext = f'{path_project_plots_vault}{signal_name}'
# figure_file = f'{figure_file_no_ext}.jpg'
# obsidian_figure_note = f'{path_figure_blocks}figure__block_{signal_name}.md'
def plot_in_Obsidian(plt, filenameSave1, figure_file_no_ext, obsidian_figure_note, PATHS, signal_name = 'signal_'):
	extensions = ['.pdf', '.jpg', '.png']
	has_extension = np.any([filenameSave1.endswith(ext) for ext in extensions])
	plt.savefig(filenameSave1 + '.jpg'*(not has_extension))
	plt.close()
	
	# create figure note file
	with open(PATHS['path_figure_block_template'], 'r') as file:
		lines = file.readlines()
		
  
	figure_file = f'{figure_file_no_ext}.jpg'
	lines.append('\n'+f"![[{figure_file}]]".replace('\\', '/')+'\n')
 
	with open(obsidian_figure_note, 'w') as file:
		file.writelines(lines)
	
	figBlockFileName = f'figure__block_{signal_name}'
	figureFileSim = f'{PATHS['path_figure_blocks']}{figBlockFileName}.md'
	fields_1 = default_fields__sim_res_signal_file
	if os.path.exists(filenameSave1+'.md'):
		fields_1 = get_fields_from_Obsidian_note(filenameSave1+'.md', expected_fields__sim_res_signal_file)

	dum1 = '#sig_qual/'
	with open(filenameSave1+'.md', 'w', encoding='utf8') as file:
		write1 = [
			'%%',
			f'{expected_fields__sim_res_signal_file[0]}{dum1}{fields_1[0].replace(dum1, "")}',
			f'{expected_fields__sim_res_signal_file[1]}{fields_1[1]}',
			'%%',
			'# %% fig %%',
			'`=replace(this.quality, "#sig_qual/", "")`'
			]
		write1.append(f'![[{figBlockFileName}#fig]]'+'\n')
		file.write("\n".join(write1))  # Write filenames in the specified format

	return figureFileSim