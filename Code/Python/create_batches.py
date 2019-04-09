import os

datapath = "G://Dev//Data"
all_gnps_processed_path = datapath + os.sep + "ALL_GNPS_20181012_processed.mgf"
batch_file_dir = datapath + os.sep + "ALL_GNPS_20181012_mini_batches"

with open(all_gnps_processed_path, 'r') as f:
	content = f.readlines()

print(len(content))

mol_list = []

for index, line in enumerate(content):
	if line.startswith("BEGIN IONS"):
		start = index
		cursor = index
		while not content[cursor].startswith("END IONS"):
			cursor += 1
		end = cursor + 1
		pair = (start, end)
		mol_list.append(content[start:end])
		
for index, mol in enumerate(mol_list):
	filename = "batch" + str(index+1) + ".mgf"
	filepath = os.path.join(batch_file_dir, filename)
	with open(filepath, 'w') as f:
		for item in mol:
			f.write(item)