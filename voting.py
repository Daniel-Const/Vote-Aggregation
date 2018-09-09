
import math
import numpy as np
import sensors
import matplotlib.pyplot as plt

NN = 25  #Number of voters
TT = 288 #Number of Time instances for each temperature reading

# sensors which will make temperature evaluations
def generate_sensors(sensors,NN, TT, temp):

    i = 0
    for x in range(NN):
        for y in range(TT):
            if x < NN - 5:
                sensors[x][y] = temp[i]
            else:
                sensors[x][y] = temp[i] + 100   #add bias for 5 attacking sensors
            i += 1
        i = 0

#Generate Bayesian noise for the sensors under their given variances; vr
def generate_noise(noise, NN, vr):

    for i in range(NN):
        for t in range(288):
            mu, sigma = 0, math.sqrt(vr[i])
            s = np.random.normal(mu,sigma, None)
            noise[i][t] = s

#Temperature data the sensors will be evaluating
def generate_temp(temp, TT):
    for i in range(1, TT + 1):
        reading = 20 + 5 * math.sin(2 * math.pi * (i / 288) - math.pi/2)
        temp[i - 1] = reading

# Add the generated noise to the sensors readings
def add_values(reading, NN, TT, a, b):

    for x in range(NN):
        for y in range(TT):
            reading[x][y] = a[x][y] + b[x][y]
    return reading


def meanCollusion(readings):
    i = 0
    for x in range(TT):
        m = 0
        for y in range(NN - 1):
            m += readings[y][x]
        readings[24][x] = m / (NN - 1)
        i += 1

#Maximum likelyhood estimation for the weights
#requires knowing the variances
def MLW(weights, vr):
    for i in range(NN):
        if i < NN - 5:
            sum = 0
            for j in range(NN - 5):
                sum += float(1 / vr[j])
            weights[i] = float(1/vr[i]) / sum
        else:
            weights[i] = 0

# Weighted Estimate of the readings, using some obtained weights
def weightedEstimate(estimate, weights, readings):
    for t in range(TT):
        for i in range(NN):
            estimate[t] += weights[i] * readings[i][t]

# Root mean squared error calculation
def rms(estimate, temp):
    RMSerrorML = 0
    sum = 0
    for t in range(TT):
        sum += (estimate[t] - temp[t]) * (estimate[t] - temp[t])
    RMSerrorML = math.sqrt(float(sum / TT))
    return RMSerrorML


#variances for 20 "honest" sensors, and 5 attackers
vr = [3.28984, 6.53638, 7.39121, 8.04884, 2.2688, 14.3726, 9.18139, \
12.1686, 12.5904, 1.41815, 8.91135, 10.8204, 5.77766, 9.47927, \
8.33004, 14.7598, 5.13233, 10.7632, 10.9492, 6.51451, 2.90741, \
7.32544, 3.34091, 2.09723, 0.01]


#Generate temperature values
temp = [0 for x in range(288)]
generate_temp(temp, TT)

#create bayesian noise for the Temperature values
noise = [[0 for x in range(288)] for y in range(NN)]
generate_noise(noise, NN, vr)

#Create a list of 'sensors' which will be submitting temperature
#recording evaluations
sensors = [[0 for x in range(TT)] for y in range(NN)]
generate_sensors(sensors,NN, TT, temp)

#creates the readings of these sensors with a bayesian
#distribution according to their given variances.
readings = [[0 for x in range(TT)] for y in range(NN)]
add_values(readings, NN,TT,sensors,noise)

#Maximum Likelihood weight calculations, using the known variances
MLWeights = [0 for x in range(NN)]
MLW(MLWeights, vr)

#Estimation for temperature values using the Maximum Likelihood weights
MLEstimate =  [0 for x in range(TT)]
weightedEstimate(MLEstimate, MLWeights, readings)

#root mean squared error of the Maximum likelihood estimations
rmsError = rms(MLEstimate, temp)

#Find the minimum error giving the most accurate sensor
min = rms(readings[0], temp)
for i in range(NN):
    rmsBest = rms(readings[i], temp)
    if rmsBest < min:
        min = rmsBest

print("RMS error ML ", rmsError)
print("RMS error Best ", min)
mean = [0 for x in range(TT)]

#meanCollusion(readings)

plt.plot(readings[0], 'r')   #Honest data

plt.plot(readings[24], 'g')  #clever mean attack

plt.plot(readings[23], 'g')  #Outlier data

plt.plot(temp, 'b')  #Actual values
plt.show()
