from mpi4py import MPI
import sys
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = int(sys.argv[1])
aux = 2
times = 0
total = 0


def prime(num):
    for i in range(2, num//2+1):
        if (num % i) == 0: 
            break
    else:
        return True
    return False

start = 0
if rank == 0:
    start = time.time()

if rank == 0:
    for i in range(1, size):
        comm.send(aux, dest=i)
        aux = aux + 1
else:
    data = comm.recv(source = 0) 
    val = [rank, data]
    if val[1] <= n:
        if(prime(val[1])):
            total = total + 1
        times = times + 1
    comm.send(rank, dest = 0)   # Give something back to root (the rank in this case)
    # Hasta acá, cada process tiene un valor inicial para empezar a trabajar

aux = comm.bcast(aux, root=0)   # Ahora aux es el mismo para todos

#####################################################################################################33333

while aux < n:
    if rank == 0:
        for i in range(1, size): # Better if I knew how many sent something to root.
            data = comm.recv()
            comm.send(aux, dest = data)
            aux = aux + 1
    else:
        data = comm.recv(source = 0)
        val = [rank, data]
        if val[1] <= n:
            if(prime(val[1])):
                total = total + 1
            times = times + 1
        comm.send(rank, dest = 0)
    aux = comm.bcast(aux, root=0) 


if rank == 0:
    for i in range(1, size): # Better if I knew how many sent something to root.
        data = comm.recv()
        comm.send(aux, dest = data)
        aux = aux + 1
else:
    data = comm.recv(source = 0) 
    val = [rank, data]
    if val[1] <= n:
        if(prime(val[1])):
            total = total + 1
        times = times + 1



total_primos = comm.reduce(total, op=MPI.SUM, root=0)


if rank == 0:
    print(round(time.time()-start, 5), "seconds")
    print("Total number of primes: ", total_primos)
else:
    print("Process", rank, "executed",times, "times")

    



