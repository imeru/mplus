import sys
import os
import shutil
import csv
from mplus import run_eplus_multi
from sampling import lhs

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
         line = line.replace(MARK_WINDOWS, str(lhs_value))
         new.write(line)
    origin.close()
    new.close()

def copy_files(orig, dest):
    files = os.listdir(orig)
    for file_name in files:
        file_path = os.path.join(orig, file_name)
        shutil.copy(file_path, dest)

if __name__ == '__main__':
    template_idf_path = "sample_data/template.idf"
    eplus_basic_folder = "sample_data/eplus_basic_files"
    output_folder = sys.argv[1]
    lhs_set = lhs(3.2, 0.2, 10)

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    pathes = []
    for index, lhs_value in enumerate(lhs_set):
        path_to_write = output_folder + "/" + str(index)
        pathes.append(path_to_write)
        output_path = path_to_write + "/" + "in.idf"
        os.makedirs(path_to_write)
        copy_files(eplus_basic_folder, path_to_write)
        write_idf(template_idf_path, output_path, lhs_value)
    run_eplus_multi(pathes)
