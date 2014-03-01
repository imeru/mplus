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

def replace_markup(line, markup_value_pairs):
    for markup in markup_value_pairs.keys():
        line = line.replace(markup, str(markup_value_pairs[markup]))
    return line

def generate_markup_values(markup_range_pairs, count):
    markup_values_pairs = {}
    for key in markup_range_pairs:
        markup = key
        ranges = markup_range_pairs[key]
        lhs_values = lhs(ranges[0], ranges[1], count)
        markup_values_pairs[markup] = lhs_values
    return markup_values_pairs

def generate_markup_value_pairs(markup_range_pairs, count):
    markup_values_pairs = generate_markup_values(markup_range_pairs, count)
    markup_value_pairs = []
    for index in range(count):
        markup_value_pair = {}
        for key in markup_range_pairs:
            markup_value_pair[key] = markup_values_pairs[key].pop()
        markup_value_pairs.append(markup_value_pair)
    return markup_value_pairs

def write_idf(template_path, output_path, markup_value_pairs):
    origin = open(template_path, 'r')
    new = open(output_path, 'w')
    for line in origin:
        replaced_line = replace_markup(line, markup_value_pairs)
        new.write(replaced_line)
    origin.close()
    new.close()

def copy_files(orig, dest):
    files = os.listdir(orig)
    for file_name in files:
        file_path = os.path.join(orig, file_name)
        shutil.copy(file_path, dest)

if __name__ == '__main__':
    template_idf_path = "sample_data/template1.idf"
    eplus_basic_folder = "sample_data/eplus_basic_files"
    output_folder = sys.argv[1]
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    markup_range_pairs = {"@@WALL@@": [0.09667, 0.02],
                          "@@WINDOWS@@": [3.2, 0.2],
                          "@@EPD@@": [40, 5]}
    count = 10
    markup_value_pairs = generate_markup_value_pairs(markup_range_pairs, count)
    pathes = []
    for index, markup_value_pair in enumerate(markup_value_pairs):
        path_to_write = output_folder + "/" + str(index)
        pathes.append(path_to_write)
        output_path = path_to_write + "/" + "in.idf"
        os.makedirs(path_to_write)
        copy_files(eplus_basic_folder, path_to_write)
        write_idf(template_idf_path, output_path, markup_value_pair)
    run_eplus_multi(pathes)
