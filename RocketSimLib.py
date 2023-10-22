import math as m
import os
import os.path as p

class Rocket:

    def __init__(self, file_path = "", massI = 1, feulM = 0.1, \
                 thrust = 10, timeMECO = 1, angleI = 1, coeff = 1, \
                 area = 1, samples_ps = 100):

        self.file_path = file_path
        self.massI = massI
        self.feulM = feulM
        self.thrust = thrust
        self.timeMECO = timeMECO
        self.angleI = angleI
        self.coeff = coeff
        self.area = area
        self.samples_ps = samples_ps

        self.AIR_DENSITY = 1.29
        self.GRAVITY = 9.81

        self.Fdrag = [1]
        self.angle = [1]
        self.mass = [1]
        self.accX = [1]
        self.accY = [1]
        self.acc = [1]
        self.veloX = [1]
        self.veloY = [1]
        self.speed = [1]
        self.dist = [1]
        self.alt = [1]

        if not p.exists(file_path):
            os.makedirs(file_path)

        if angleI == 0:
            self.ifAngleIis0(massI, thrust, angleI)
        else:
            # Calculate 1st Stage trajectory
            t = 0
            while self.alt[t - 1] >= 0 and t <= timeMECO * samples_ps:
                self.S1calcVeloX(samples_ps, t)
                self.S1calcVeloY(samples_ps, t)
                self.S1calcSpeed(t)
                self.S1calcDrag(area, coeff, t)
                self.S1calcAngle(angleI, t)
                self.S1calcMass(massI, feulM, timeMECO, samples_ps, t)
                self.S1calcAccX(thrust, t)
                self.S1calcAccY(thrust, t)
                self.S1calcAcc(t)
                self.S1calcDist(samples_ps, t)
                self.S1calcAlt(samples_ps, t)
                t = t + 1
            # Calculate 2nd Stage trajectory
            while self.alt[t - 1] > 0:
                self.S2calcVeloX(samples_ps, t)
                self.S2calcVeloY(samples_ps, t)
                self.S2calcSpeed(t)
                self.S2calcDrag(area, coeff, t)
                self.S2calcAngle(t, angleI)
                self.S2calcMass(massI, feulM, t)
                self.S2calcAccX(t)
                self.S2calcAccY(t)
                self.S2calcAcc(t)
                self.S2calcDist(samples_ps, t)
                self.S2calcAlt(samples_ps, t)
                t = t + 1
            self.setLanding()
        
        # Record Data
        self.recordData(file_path, "Fdrag.txt", self.Fdrag)
        self.recordData(file_path, "angle.txt", self.angle)
        self.recordData(file_path, "mass.txt", self.mass)
        self.recordData(file_path, "accX.txt", self.accX)
        self.recordData(file_path, "accY.txt", self.accY)
        self.recordData(file_path, "acc.txt", self.acc)
        self.recordData(file_path, "veloX.txt", self.veloX)
        self.recordData(file_path, "veloY.txt", self.veloY)
        self.recordData(file_path, "speed.txt", self.speed)
        self.recordData(file_path, "dist.txt", self.dist)
        self.recordData(file_path, "alt.txt", self.alt)

    # If inital angle = 0

    def ifAngleIis0(self, massI, thrust, angleI):
        self.Fdrag = [0]
        self.angle = [angleI]
        self.mass = [massI]
        self.accX = [thrust / massI]
        self.accY = [0]
        self.acc = [thrust / massI]
        self.veloX = [0]
        self.veloY = [0]
        self.speed = [0]
        self.dist = [0]
        self.alt = [0]

    # Set landing condition in data

    def setLanding(self):
        self.alt[-1] = 0

    # Stage 1

    def S1calcVeloX(self, samples_ps, t):
        if t == 0:
            self.veloX[t] = 0
        else:
            self.veloX.append(self.veloX[t - 1] + (self.accX[t - 1] / samples_ps))

    def S1calcVeloY(self, samples_ps, t):
        if t == 0:
            self.veloY[t] = 0
        else:
            self.veloY.append(self.veloY[t - 1] + (self.accY[t - 1] / samples_ps))

    def S1calcSpeed(self, t):
        if t == 0:
            self.speed[t] = 0
        else:
            self.speed.append(m.sqrt((self.veloX[t] ** 2) + (self.veloY[t] ** 2)))

    def S1calcDrag(self, area, coeff, t):
        if t == 0:
            self.Fdrag[t] = 0
        else:
            self.Fdrag.append(0.5 * self.AIR_DENSITY * area \
                        * coeff * (self.speed[t] ** 2))

    def S1calcAngle(self, angleI, t):
        if t == 0:
            self.angle[t] = angleI
        else:
            if angleI == m.pi / 2:
                if self.veloY[t] >= 0:
                    self.angle.append(angleI)
                else:
                    self.angle.append(0 - angleI)
            else:
                self.angle.append(m.atan(self.veloY[t] / self.veloX[t]))

    def S1calcMass(self, massI, feulM, timeMECO, samples_ps, t):
        if t == 0:
            self.mass[t] = massI
        else:
            self.mass.append(self.mass[t - 1] - (feulM / (timeMECO * samples_ps)))

    def S1calcAccX(self, thrust, t):
        if t == 0:
            self.accX[t] = ((thrust - self.Fdrag[t]) / self.mass[t]) \
                           * m.cos(self.angle[t])
        else:
            self.accX.append(((thrust - self.Fdrag[t]) / self.mass[t]) \
                       * m.cos(self.angle[t]))

    def S1calcAccY(self, thrust, t):
        if t == 0:
            self.accY[t] = (((thrust - self.Fdrag[t]) / self.mass[t]) \
                           * m.sin(self.angle[t])) - self.GRAVITY
        else:
            self.accY.append((((thrust - self.Fdrag[t]) / self.mass[t]) \
                       * m.sin(self.angle[t])) - self.GRAVITY)

    def S1calcAcc(self, t):
        if t == 0:
            self.acc[t] = m.sqrt((self.accX[t] ** 2) + (self.accY[t] ** 2))
        else:
            self.acc.append(m.sqrt((self.accX[t] ** 2) + (self.accY[t] ** 2)))

    def S1calcDist(self, samples_ps, t):
        if t == 0:
            self.dist[t] = 0
        else:
            self.dist.append(self.dist[t - 1] + (self.veloX[t] / samples_ps))

    def S1calcAlt(self, samples_ps, t):
        if t == 0:
            self.alt[t] = 0
        else:
            self.alt.append(self.alt[t - 1] + (self.veloY[t] / samples_ps))

    # Stage 2

    def S2calcVeloX(self, samples_ps, t):
        self.veloX.append(self.veloX[t - 1] + (self.accX[t - 1] / samples_ps))

    def S2calcVeloY(self, samples_ps, t):
        self.veloY.append(self.veloY[t - 1] + (self.accY[t - 1] / samples_ps))

    def S2calcSpeed(self, t):
        self.speed.append(m.sqrt((self.veloX[t] ** 2) + (self.veloY[t] ** 2)))

    def S2calcDrag(self, area, coeff, t):
        self.Fdrag.append(0.5 * self.AIR_DENSITY * area \
                        * coeff * (self.speed[t] ** 2))

    def S2calcAngle(self, t, angleI):
        if angleI == m.pi / 2:
            if self.veloY[t] >= 0:
                self.angle.append(angleI)
            else:
                self.angle.append(0 - angleI)
        else:
            self.angle.append(m.atan(self.veloY[t] / self.veloX[t]))

    def S2calcMass(self, massI, feulM, t):
        self.mass.append(massI - feulM)

    def S2calcAccX(self, t):
        self.accX.append(((0 - self.Fdrag[t]) / self.mass[t]) \
                       * m.cos(self.angle[t]))

    def S2calcAccY(self, t):
        self.accY.append((((0 - self.Fdrag[t]) / self.mass[t]) \
                       * m.sin(self.angle[t])) - self.GRAVITY)

    def S2calcAcc(self, t):
        self.acc.append(m.sqrt((self.accX[t] ** 2) + (self.accY[t] ** 2)))

    def S2calcDist(self, samples_ps, t):
        self.dist.append(self.dist[t - 1] + (self.veloX[t] / samples_ps))

    def S2calcAlt(self, samples_ps, t):
        self.alt.append(self.alt[t - 1] + (self.veloY[t] / samples_ps))

    # Recording

    def recordData(self, file_path, file_name, data):
        file = open(p.join(file_path, file_name), 'w', encoding='utf-8')
        for instance in data:
            file.write(str(format(instance, '.5f')) + '\n')
    
    # Reading
    def readData(self, file_path, file_name):
        file = open(p.join(file_path, file_name), 'r', encoding='utf-8')
        return file.readlines()

    # Getters

    def getInitAngle(self):
        return format(self.angleI, '.5f')

    def getMaxDist(self):
        return format(self.dist[-1], '.5f')

    def getTotalTime(self):
        return format(len(self.dist) / self.samples_ps, '.5f')

    def getMaxAlt(self):
        if self.angleI == 0:
            return format(0, '.5f')
        else:
            t = 0
            while self.alt[t + 1] > self.alt[t]:
                t = t + 1
            return format(self.alt[t], '.5f')

    def getApoTime(self):
        if self.angleI == 0:
            return format(0, '.5f')
        else:
            t = 0
            while self.alt[t + 1] > self.alt[t]:
                t = t + 1
            return t / self.samples_ps