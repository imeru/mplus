import sys
import os
import shutil
from mplus import run_eplus_multi
from make_idf import generate_markup_value_pairs, write_idf, copy_files
from make_idf import prepare_job_folders

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
pathes = prepare_job_folders(output_folder, template_idf_path,
                             eplus_basic_folder, markup_value_pairs)
run_eplus_multi(pathes)
