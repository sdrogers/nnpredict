import os

from subprocess import CalledProcessError, TimeoutExpired, STDOUT, check_call

datapath = "G://Dev//Data"
batch_file_dir = batch_file_dir = datapath + os.sep + "ALL_GNPS_20181012_mini_batches"
sirius_exe_path = "sirius-console-64" # sirius .exe file, need to change this path to where sirius is downloaded to (full path)
output_file_dir = datapath + os.sep + "sirius_output_minibatches"
processed_files = [file + ".mgf" for file in os.listdir(output_file_dir)]
combined_processed_files = []

# This is there to continue from breakpoint as some will get stuck
# After cancelling (due to being stuck etc.), follow these steps
# New output folder, include what is processed, and if more, use combined_processed_files
# After all batches have been processed by CSI, combine all together in one single output_file_dir
# say yes to replace 

#output_file_dir = "sirius_output_minibatches3"
#processed_files2 = [file + ".mgf" for file in os.listdir("sirius_output_minibatches2")]
#combined_processed_files = processed_files + processed_files2

for file in os.listdir(batch_file_dir):
	if file not in combined_processed_files:
		filepath = os.path.join(batch_file_dir, file)
		output_filepath = os.path.join(output_file_dir, file[:-4])
		cmd = "{} -o {} -F {}".format(sirius_exe_path, output_filepath, filepath)
		seconds = 360
		
		try:
			output = check_call(cmd, stderr=STDOUT, timeout=seconds, shell=True)
		except CalledProcessError as e:
			print(e)
		except TimeoutExpired:
			pass
			
print("Done")