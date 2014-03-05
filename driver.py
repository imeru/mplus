import sys
import os
import shutil
from mplus import run_eplus_multi
from make_idf import generate_markup_value_pairs, write_idf, copy_files

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
