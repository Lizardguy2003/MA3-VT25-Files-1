""" MA3.py

Student: Alexander Reider
Mail: acreider2003@gmail.com
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import functools

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    #create coordinates for x and y
    print(f'The Number of points: {n}')
    x = [random.uniform(-1, 1) for _ in range(n)]
    y = [random.uniform(-1, 1) for _ in range(n)]


    #inside the circle, if the sum of the pairs squared is smaller than 1 it is sorted into RED
    pair = list(zip(x, y))
    coordred = [p for p in pair if (p[0]**2 + p[1]**2) < 1]
    xplotred, yplotred = zip(*coordred)

    #Outside the circle, if the sum of the pairs squared is larger than 1 it is sorted into BLUE
    coordblue= [p for p in pair if (p[0]**2 + p[1]**2) > 1]
    xplotblue, yplotblue = zip(*coordblue)

    #Calculating pi
    pi = 4*len(coordred)/n
    
    #Making the plot, and making it square
    fig, ax = plt.subplots()
    ax.plot(xplotred, yplotred, 'ro', xplotblue, yplotblue, 'bo')
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.set_aspect(abs(x1-x0)/abs(y1-y0))
    fig.savefig(f'plot_{n}_points.png')
    plt.show()
    return pi

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    var = 0

    #1. list comprehension; finding random coordinates
    coord = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    
    #2. functools.reduce 3. map 4. lambda; increasing the number of points are inside the sphere by 1 everytime the check passes
    for i in range(n): #squaring all elements in the smaller lists and adding them together
        k = functools.reduce(lambda x,y: x+y , map(lambda p: p**2, coord[i]))
        if k <= 1:
             var += 1

    return (2**d)*var/n

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    return (m.pi**(d/2))/m.gamma((d/2) + 1)

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    
    with future.ProcessPoolExecutor() as ex:
        p = [ex.submit(sphere_volume, int(n/np), d) for _ in range(np)] #n/np to only have total n iterations
        r = [f.result() for f in p]
    return mean(r)

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    #d is the number of dimensions of the sphere
    #np is the number of processes
    

    #using a helper function to use ex.map
    with future.ProcessPoolExecutor() as ex:
        result = list(ex.map(helper, [int(n/np)]*np, [d]*np))
        
    res = sum(result)
        
    vol = (2**d)*res/n
    
    return vol
    
def helper(n, d):
    #same code as above in Ex2
    var = 0
    coord = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    for i in coord:
        k = functools.reduce(lambda x,y: x+y , map(lambda p: p**2, i))
        if k <= 1:
            var += 1
    return var
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    
    print(f"Ex3: Sequential time of {d} and {n}: {(stop-start)}") #it took 7.9 seconds, average 0.79 seonds
    print("What is parallel time?") 
    start2 = pc()
    sphere_volume_parallel1(n, d, 10)
    end2 = pc()
    print(end2-start2)
    
    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    
    start1 = pc()
    sphere_volume_parallel2(n,d,np=10)
    stop1 = pc()
    print(stop1-start1)
    
    
    

if __name__ == '__main__':
	main()
