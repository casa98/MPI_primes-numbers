from mpi4py import MPI
import sys
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = int(sys.argv[1])
aux = 2


def prime(num):
    for i in range(2, num//2+1):
        if (num % i) == 0: 
            break
    else: 
        print(num, "is a prime number") 

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
        prime(val[1])
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
            prime(val[1])
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
        prime(val[1])

#aux = comm.bcast(aux, root=0) 
if rank == 0:
    print(time.time()-start)


