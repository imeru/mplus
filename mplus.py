from multiprocessing import Pool, cpu_count
from subprocess import call
import os
import shutil

def run_energyplus(path):
    current_dir = os.getcwd()
    os.chdir(path)
    call(["energyplus"])
    os.chdir(current_dir)

def copy_folder(origin, destination):
    shutil.copytree(origin, destination)

if __name__ == '__main__':
    ORIGIN_DATA = "data"
    pathes = []
    for i in range(4):
        destination = ORIGIN_DATA + "_"  + str(i)
        copy_folder(ORIGIN_DATA, destination)
	pathes.append(destination)
    CORES = cpu_count()
    p = Pool(CORES)
    print p.map(run_energyplus, pathes)
