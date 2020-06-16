# -*- coding: utf-8 -*-
"""
Created on Sun May 31 02:11:17 2020

@author: Susmit
"""

import math 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from statistics import mean


print("Explicit Method for the given problem")
print("=====================================")

print()



alpha = float(input("Enter the coefficient of thermal diffusivity: ")) # 2x10^-5m^2/s
length = float(input("Enter the length of slab(m): ")) # 12cm or 0.12m
upper_limit_time = float(input("Enter the upper limit of time: "))# i.e till what time you want to see the temperature distribuition
delx = float(input("Distance between two consecutive nodes: "))
delt = float(input("Time sepration betwween distance: "))

r = alpha*delt/(delx**2)

T = np.zeros([int(length/delx)+1,int(upper_limit_time/delt)+1])#101X101 with 0 - 100 index values


while (alpha*delt/(delx**2)>0.5):#Stability criteria get's failed choose delx and delt again
    
    print("Choose delx and delt again as the solution won't convergence")
    delx = float(input("Distance between two consecutive nodes: "))
    delt = float(input("Time sepration betwween distance: "))
    #T[space,time]
T[0,0] = 0
T[int(length//delx),0] = 0 # End Boundart conditions 
x = delx
y = 1
while(x<=int(length/delx)):
    
    T[y,0] = 100*(math.sin(math.pi*x/length)) # initial temperature distribution T i = 100 sin (π x/L)
    x += delx
    y+=1
    if y == int(length/delx):
            break
for time in range(0,int(upper_limit_time/delt)):
    
    for space in range(1,int(length//delx)+1):

        
        T[space,time+1] = T[space,time] + r*(T[space-1,time] - 2*T[space,time] + T[space+1,time])

matrix_temp = np.matrix(T)

# Heat Flux Calculation
#Ti=100sin(π x/L)
#dTi/dx = (100pi*cos(π x/L)/L)
K = 80 #Thermal Conductivity of steel K = 80 Wm/k
A = 1 # Unit area face
Q = np.zeros([int(length/delx)+1,int(upper_limit_time/delt)+1])
#Calculate dT/dx given Inital Temperature distribution 
y = 1
while(x<=int(length/delx)):
    
    Q[y,0] = 100*math.pi*(math.cos(math.pi*x/length))*(1/length) # initial temperature distribution T i = 100 sin (π x/L)
    x += delx
    y+=1
    if y == int(length/delx):
            break
for time in range(0,int(upper_limit_time/delt)):
    
    for space in range(1,int(length//delx)+1):

        
        Q[space,time+1] = Q[space,time] + r*(Q[space-1,time] - 2*Q[space,time] + Q[space+1,time])
        
Q = -(K*A*Q)/length

matrix_Qflux = np.matrix(Q)

temp_explicit = pd.DataFrame(T)
file_path = "C:\\Users\\Susmit\\OneDrive\\Desktop\\Semester 6\\CME\\CME_project\\explicit_temp.xlsx"
temp_explicit.to_excel(file_path, index = False)

Flux_explicit = pd.DataFrame(Q)
file_path = "C:\\Users\\Susmit\\OneDrive\\Desktop\\Semester 6\\CME\\CME_project\\explicit_flux.xlsx"
Flux_explicit.to_excel(file_path, index = False)
#with open("C:\\Users\\Susmit\\OneDrive\\Desktop\\Semester 6\\CME\\CME_project\\explicit_temp.csv",'wb') as f:
#    for line in matrix_temp:
#            np.savetxt(f, line ,fmt = '%0.6f')

#Plotting descriptions 
    
plot1=plt.figure(1)
plt.xlim(0,int(length/delx))
plt.ylim(0,100)
plt.grid(True,linewidth = 0.01, color = "c",linestyle = "--")
plt.xlabel("Length across thickness of slab")
plt.ylabel("Tempperature")
plt.plot(T)

plot = plt.figure(2)
plt.xlim(0,int(length/delx))
plt.grid(True,linewidth = 0.01, color = "c",linestyle = "--")
plt.xlabel("Length across thickness of slab")
plt.ylabel("Heat Flux")
plt.plot(Q)


# Average interpolation of all time step at particular instance

#x_instant = np.zeros(int(length/delx)+1)
#
#for time in range(int(length/delx)+1):
#    average = mean(T[time,:])
#    x_instant[time] = average
    

