import sys
import os
import shutil
import csv
from sampling import Sampling

def replace_markup(line, markup_value_pairs):
    for markup in markup_value_pairs.keys():
        line = line.replace(markup, str(markup_value_pairs[markup]))
    return line

def generate_markup_values(markup_range_pairs, count):
    markup_values_pairs = {}
    for key in markup_range_pairs:
        markup = key
        ranges = markup_range_pairs[key]
        lhs_normal_sampling = Sampling('normal', 'lhs')
        sampling_values = lhs_normal_sampling.generate(count, ranges)
        markup_values_pairs[markup] = sampling_values
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

def prepare_job_folders(output_folder, template_idf_path,
                        eplus_basic_folder, markup_value_pairs):
    pathes = []
    for index, markup_value_pair in enumerate(markup_value_pairs):
        path_to_write = output_folder + "/" + str(index)
        pathes.append(path_to_write)
        output_path = path_to_write + "/" + "in.idf"
        os.makedirs(path_to_write)
        copy_files(eplus_basic_folder, path_to_write)
        write_idf(template_idf_path, output_path, markup_value_pair)
    return pathes
