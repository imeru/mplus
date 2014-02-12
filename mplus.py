from multiprocessing import Pool, cpu_count

def f(x):
    return x*x

if __name__ == '__main__':
    CORES = cpu_count()
    p = Pool(CORES)
    print p.map(f, [1,2,3,100,200,300,400,500])
