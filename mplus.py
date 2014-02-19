from multiprocessing import Pool, cpu_count
from subprocess import call
import os
import shutil

def run_eplus(path):
    current_dir = os.getcwd()
    os.chdir(path)
    call(["energyplus"])
    os.chdir(current_dir)

def run_eplus_multi(pathes):
    p = Pool(cpu_count())
    result = p.map(run_eplus, pathes)
    return result

def copy_folder(origin, destination):
    shutil.copytree(origin, destination)

if __name__ == '__main__':
    ORIGIN_DATA = "data"
    pathes = []
    for i in range(4):
        destination = ORIGIN_DATA + "_"  + str(i)
        copy_folder(ORIGIN_DATA, destination)
	pathes.append(destination)
    run_eplus_multi(pathes)
