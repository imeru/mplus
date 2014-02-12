from multiprocessing import Pool, cpu_count
from subprocess import call
import os

def run_energyplus(path):
    current_dir = os.getcwd()
    os.chdir(path)
    call(["energyplus"])
    os.chdir(current_dir)

if __name__ == '__main__':
    CORES = cpu_count()
    pathes = ["data", "data2"]
    p = Pool(CORES)
    print p.map(run_energyplus, pathes)
