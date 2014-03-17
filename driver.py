import sys
import os
import shutil
import csv
from mplus import run_eplus_multi
from make_idf import generate_markup_value_pairs, write_idf, copy_files
from make_idf import prepare_job_folders

# initial values
template_idf_path = "sample_data/template1.idf"
eplus_basic_folder = "sample_data/eplus_basic_files"
output_folder = sys.argv[1]
markup_range_pairs = {"@@WALL@@": [0.09667, 0.02],
                      "@@WINDOWS@@": [3.2, 0.2],
                      "@@EPD@@": [40, 5]}
count = 10
eplusout_file_name = "eplusout.csv"
result_folder_name = "result"

# check output path
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

# prepares jobs
markup_value_pairs = generate_markup_value_pairs(markup_range_pairs, count)
pathes = prepare_job_folders(output_folder, template_idf_path,
                             eplus_basic_folder, markup_value_pairs)

# run jobs
run_eplus_multi(pathes)

# post-processing: gathering eplusout.csv files
eplus_out_csv_pathes = []
for root, dirs, files in os.walk(output_folder):
    for file in files:
        if file.endswith(eplusout_file_name):
            eplus_out_csv_pathes.append(os.path.join(root, file))
eplus_out_csv_pathes = sorted(eplus_out_csv_pathes)
result_path = os.path.join(output_folder, result_folder_name)
os.makedirs(result_path)
dest_pathes = []
for path in eplus_out_csv_pathes:
    path = path.replace(output_folder + "/", '')
    path = path.replace("/", "_")
    path = os.path.join(result_path, path)
    dest_pathes.append(path)
for orig, dest in zip(eplus_out_csv_pathes, dest_pathes):
    shutil.copyfile(orig, dest)

# gathering csv files into a csv file
csv_sum = []
with open(dest_pathes[0]) as csv_file:
    rows = csv.reader(csv_file, delimiter='|')
    contents = [row for row in rows]
    csv_sum.extend(contents[0])

for file in dest_pathes:
    print "***", file
    with open(file) as csv_file:
        rows = csv.reader(csv_file, delimiter='|')
        contents = [row for row in rows]
        print "***", type(contents), contents
        csv_sum.extend(contents[1])

csv_sum_file_name = "csv_sum.csv"
csv_sum_file_path = os.path.join(result_path, csv_sum_file_name)
with open(csv_sum_file_path, "wb") as file:
    for row in csv_sum:
        file.write("%s\n" % row)

# generating csv file for markup value_pairs
input_param_val_name = "input_parameters_values.csv"
input_param_val_path = os.path.join(result_path, input_param_val_name)
with open(input_param_val_path, "wb") as file:
    out = csv.writer(file, delimiter='|', quoting=csv.QUOTE_NONE)
    header = ["JOB_ID"]
    header.extend(markup_value_pairs[0].keys())
    out.writerow(header)
    for index, item in enumerate(markup_value_pairs):
        row = [index]
        row.extend(item.values())
        out.writerow(row)
