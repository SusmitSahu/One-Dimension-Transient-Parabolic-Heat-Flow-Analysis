# -*- coding: utf-8 -*-
"""
Created on Sun May 31 02:11:17 2020

@author: Susmit
"""

import math 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
print("Crank Nicolson method for the given problem")
print("=====================================")

print()



alpha = float(input("Enter the coefficient of thermal diffusivity: ")) # 2x10^-5m^2/s
length = float(input("Enter the length of slab(m): ")) # 12cm or 0.12m
upper_limit_time = float(input("Enter the upper limit of time: "))# i.e till what time you want to see the temperature distribuition
delx = float(input("Distance between two consecutive nodes: "))
delt = float(input("Time sepration betwween distance: "))

r = alpha*delt/(delx**2)

T = np.zeros([int(length/delx)+1,int(upper_limit_time/delt)+1])#101X101 with 0 - 100 index values


# Stability criteria is not needed
T[0,0] = 0
T[int(length//delx),0] = 0 # End Boundart conditions 
x = 1

# Defining the [K] matrix also can be called as global stifness matrix
K = np.zeros([int(length/delx)-1,int(length/delx)-1])
#print(K)

for i in range(int(length/delx)-1):
    K[i,i] = r+1

    if i < (int(length/delx) -1) - 1 :
        K[i+1,i] = r/2
        K[i,i+1] = r/2
#print(K) Prints global stifness matrix
print(K)
try:
    inverse_K = np.linalg.inv(K)
except:
    print("matrix is not invertible")
print(inverse_K)

K_crank = np.matmul(inverse_K,-K)
print(K_crank)
x = 0
while(x <= length):
    T[x,0] = 100*(math.sin(math.pi*x/length)) # initial temperature distribution T i = 100 sin (π x/L)
    x += 1
k = 1

while k < int(upper_limit_time/delt):
    T[0,k] = 0
    T[int(length/delx),k] = 0
    k += 1

for time in range(0,int(upper_limit_time/delt)):
    
    for row in range(1,int(length/delx)):
        for coloumn in range(1,int(length/delx)):
           T[row,time+1] = T[row,time+1] + K_crank[row-1,coloumn-1]*T[coloumn,time]# Coloumn here is row
          
matrix_Tflux = np.matrix(T)
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
    
    for row in range(1,int(length/delx)):
        for coloumn in range(1,int(length/delx)):
           Q[row,time+1] =Q[row,time+1] + inverse_K[row-1,coloumn-1]*Q[coloumn,time]# Coloumn here is row
        
        
matrix_Qflux = np.matrix(Q) 
        
        
        
Q = -(K*A*Q)/length
#Saving it in form of execl sheet
temp_Crank = pd.DataFrame(T)
file_path = "C:\\Users\\Susmit\\OneDrive\\Desktop\\Semester 6\\CME\\CME_project\\CrankNicolson_temp.xlsx"
temp_Crank.to_excel(file_path, index = False)
flux_Crank = pd.DataFrame(T)
file_path = "C:\\Users\\Susmit\\OneDrive\\Desktop\\Semester 6\\CME\\CME_project\\CrankNicolson_FLux.xlsx"
flux_Crank.to_excel(file_path, index = False)


#Plotting descriptions 
plot1=plt.figure(1)
plt.xlim(0,int(length/delx))
plt.ylim(-100,100)
plt.grid(True,linewidth = 0.01,which='minor',axis = 'x', color = "c",linestyle = "--")
plt.xlabel("Length across thickness of slab")
plt.ylabel("Tempperature")
plt.plot(T)

plot2 = plt.figure(2)
plt.xlim(0,int(length/delx))
plt.grid(True,linewidth = 0.1, color = "c",linestyle = "--")
plt.xlabel("Length across thickness of slab")
plt.ylabel("Heat Flux")
plt.plot(Q)

