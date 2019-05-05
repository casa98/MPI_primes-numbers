from mpi4py import MPI
import sys
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()  # Quantity of processes
rank = comm.Get_rank()  # Processes (a number for each process counting from 0 t0 (size -1))

n = int(sys.argv[1])    # Limit number to calculate prime numbers
aux = 2     #  Beginning number to start calculating primes
times = 0   # How many numbers a process verifies
total = 0   # Total prime numbers calculated by each process


def prime(num):     # Calculate is number is prime (basic algorithm)
    for i in range(2, num//2+1):
        if (num % i) == 0: 
            break
    else:
        return True
    return False

start = time.time() # To measure time execution

'''
    The coming piece of code is like the base case
    Process 0 (root) will control everything, it'll send numbers 
    to the other processes to check id they're prime or not.
    Root will not make calculations.
    When a process end calculating a number, send info back to root
    and then when root gets this, it sends another number to that process
    In this first part, root sends and do no receives anything back (it does but
    on the general block code inside the 'while loop' which will iterate while
    aux <= n).

'''

if rank == 0:   # if root
    for i in range(1, size):
        comm.send(aux, dest=i)  # Sends a number to processes to check primality
        aux = aux + 1   # Next process will receive the coming number (2->3->4->5->...->n)
else:   # if other processes (these ones get the numbers sent and check it)
    data = comm.recv(source = 0)    # get the number from root (always process 0)
    if data <= n:
        if(prime(data)):
            total = total + 1   # Increments the primes quantity
        times = times + 1   # Quantity of iterations made by each process
    comm.send(rank, dest = 0)   # Give something back to root (the rank in this case)
    # Hasta acá, cada process tiene un valor inicial para empezar a trabajar

aux = comm.bcast(aux, root=0)   # Ahora aux es el mismo para todos

#####################################################################################################33333
#   GENERAL ALGORITHM

while aux < n:
    if rank == 0:
        for i in range(1, size): 
            data = comm.recv()
            comm.send(aux, dest = data)
            aux = aux + 1
    else:
        data = comm.recv(source = 0)
        if data <= n:
            if(prime(data)):
                total = total + 1
            times = times + 1
        comm.send(rank, dest = 0)
    aux = comm.bcast(aux, root=0) 

# Why the following code? (This could be optimized)
'''
When the last round of numbers is being calculated,
I do not need to get an answer from other processes to root
You'll not find a line sending info to root inside the 'else'

    I could not get at what moment inside the loop above,
    when to stop sending answer back to root.
    I made it easy (not as good) and made another specific case below.

'''

if rank == 0:
    for i in range(1, size): 
        data = comm.recv()
        comm.send(aux, dest = data)
        aux = aux + 1
else:
    data = comm.recv(source = 0)
    if data <= n:
        if(prime(data)):
            total = total + 1
        times = times + 1


# Sum up the total of prime numbers that each process got
total_primos = comm.reduce(total, op=MPI.SUM, root=0)


if rank == 0:
    print(round(time.time()-start, 5), "seconds")
    print("Total number of primes: ", total_primos)
else:
    print("Process", rank, "executed", times, "times")

    



