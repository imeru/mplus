import sys
import os
import shutil
import csv


def get_lhs_set(lhs_file_path):
    with open(lhs_10_path, "r") as f:
        csv_contents = csv.reader(f)
        lhs_set = [value for value in csv_contents]
    return lhs_set


def write_idf(template_path, output_path, lhs_value):
    MARK_WINDOWS = "@@WINDOWS@@"
    origin = open(template_path, 'r')
    new = open(output_path, 'w')
    for line in origin:
         line = line.replace(MARK_WINDOWS, lhs_value)
         new.write(line)
    origin.close()
    new.close()

lhs_10_path = "sample_data/lhs_10.csv"
template_idf_path = "sample_data/template.idf"
output_folder = sys.argv[1]
lhs_set = get_lhs_set(lhs_10_path)

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

for index, lhs_value in enumerate(lhs_set[0]):
    path_to_write = output_folder + "/" + str(index)
    output_path = path_to_write + "/" + "lhs_" + str(index) + ".idf"
    os.makedirs(path_to_write)
    write_idf(template_idf_path, output_path, lhs_value)
