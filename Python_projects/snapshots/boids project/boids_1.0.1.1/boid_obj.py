import pygame as pg
import math as mat
import random as rand
Vec = pg.Vector2

def SafeNormalize(vector):
    if vector.length() == 0:
        return Vec(0,0)
    else: 
        return Vec(vector.normalize())

# SLIDERS:
# align strength
# max vel
# conform/avoid strength
# wall avoid strength
# wall box
# adaptive conform (deactivates within radius)

class Boid:
    def __init__(
            self, id, surface, 
            gamePos=Vec(0,0), 
            velocity=Vec(0,0), dirCol=(0,0,0)
        ):
        self.id = id
        self.screen = surface
        self.pos = Vec(gamePos)
        self.vel = Vec(velocity)
        self.acc = Vec(0,0)
        self.font = None
        self.dirCol = dirCol
        self.speedMult = rand.uniform(0.5,1.5)

    def FontInit(self):
        if self.font is None:
            self.font = pg.font.SysFont("Consolas", 12)

    def Dir(self):
        return SafeNormalize(self.vel.copy())

    def Accelerate(self, boidList, avoidRadius, viewRadius, maxVel, mousePos, mouseAvoid, flatAvoid, conformStrength):
        self.acc = (
            self.Conform(boidList, viewRadius, conformStrength) + 
            self.WallAvoid(50, 20, maxVel) + 
            self.WallAvoid(150, 2.5, maxVel)
        )
        if mouseAvoid:
            self.acc += self.MouseAvoid(mousePos, avoidRadius, maxVel)
        if flatAvoid:
            self.acc += self.FlatAvoid(boidList, avoidRadius, maxVel)
        else:
            self.acc += self.ScaleAvoid(boidList, avoidRadius, maxVel)
    
    def Move(self, dt, boidList, alignRadius, maxVel, alignStrength):
        self.Align(boidList, alignRadius, dt, alignStrength)
        self.vel *= 1.5 ** dt 
        if self.vel.length() > self.speedMult * maxVel:
            self.vel.scale_to_length(maxVel)
        self.vel += self.acc * dt
        self.pos += self.vel * dt

    def GetNearBoid(self, boidList, radius, pos=False):
        nearBoidList = []
        for boid in boidList:
            if boid.id != self.id and (boid.pos - self.pos).length() <= radius:
                if pos:
                    nearBoidList.append(boid.pos)
                else:
                    nearBoidList.append(boid)
        return nearBoidList

    def Conform(self, boidList, viewRadius, conformStrength):
        nearBoidList = self.GetNearBoid(boidList, viewRadius, True)
        avgPos = Vec(0,0)
        if len(nearBoidList) > 0:
            for boidPos in nearBoidList:
                avgPos += boidPos - self.pos
            avgPos /= len(nearBoidList)
        return conformStrength * avgPos

    def FlatAvoid(self, boidList, avoidRadius, maxVel):
        nearBoidList = self.GetNearBoid(boidList, avoidRadius, True)
        boidRepel = Vec(0,0)
        if len(nearBoidList) > 0:
            for boidPos in nearBoidList:
                posDiff = boidPos - self.pos
                if posDiff != 0:
                    boidRepel -= (posDiff / posDiff.length())
            boidRepel = SafeNormalize(boidRepel)
        return boidRepel * 10 * maxVel

    def ScaleAvoid(self, boidList, avoidRadius, maxVel):
        nearBoidList = self.GetNearBoid(boidList, avoidRadius, True)
        boidRepel = Vec(0,0)
        if len(nearBoidList) > 0:
            for boidPos in nearBoidList:
                posDiff = boidPos - self.pos
                if posDiff != 0:
                    boidRepel -= (SafeNormalize(posDiff) * ((avoidRadius - posDiff.length()) / avoidRadius))
        return boidRepel * 10 * maxVel
    
    def MouseAvoid(self, mousePos, avoidRadius, maxVel):
        boidRepel = Vec(0,0)
        if (mousePos - self.pos).length() <= 4 * avoidRadius:
            posDiff = mousePos - self.pos
            boidRepel = -1 * SafeNormalize(posDiff)
            return boidRepel * 6 * maxVel
        else:
            return (0,0)
    
    def Align(self, boidList, alignRadius, dt, alignStrength):
        nearBoidList = self.GetNearBoid(boidList, alignRadius)
        if len(nearBoidList) > 0 and self.vel.length() > 0:
            avgDir = Vec(0,0)
            for boid in nearBoidList:
                avgDir += SafeNormalize(boid.vel)
            avgDir = SafeNormalize(avgDir)
            newDir = SafeNormalize(avgDir * alignStrength * dt + self.Dir())
            if newDir.length() > 0 and self.vel.length() > 0:
                self.vel = newDir * self.vel.length()

    def WallAvoid(self, radius, repel, maxVel):
        screenDimensions = Vec(self.screen.get_size())
        wallRepel = Vec(0,0)
        if self.pos.x > screenDimensions.x - radius:
            wallRepel.x -= repel * maxVel
        elif self.pos.x < radius:
            wallRepel.x += repel * maxVel
        if self.pos.y > screenDimensions.y - radius:
            wallRepel.y -= repel * maxVel
        elif self.pos.y < radius:
            wallRepel.y += repel * maxVel
        return wallRepel 

    def DrawSelf(self, directionLine=False):
        if directionLine:
            pg.draw.circle(self.screen, (221, 195, 185), self.pos + self.Dir() * 3, 2)
            pg.draw.circle(self.screen, self.dirCol, self.pos + self.Dir() * -2, 3)
            pg.draw.circle(self.screen, self.dirCol, self.pos, 3)
#            pg.draw.line(
#                self.screen, 
#                self.dirCol, 
#                self.pos, 
#                self.pos + (self.Dir() * 10)
#            )

    def DrawLines(
            self, boidList, mousePos,
            avoidRadius, viewRadius, alignRadius,
            conformStrength,
            conformCircle=False, 
            avoidCircle=False,  
            conformLine=False, 
            avoidLine=False,
            alignLine=False,
            alignCircle=False,
            mouseAvoidLine=False
        ):
        if avoidCircle:
            pg.draw.circle(
                self.screen, 
                (128,0,0), 
                self.pos, 
                0.5 * avoidRadius, 
                1
            )
        if conformCircle:
            pg.draw.circle(
                self.screen,
                (0,0,128),
                self.pos,
                viewRadius,
                1
            )
        if alignCircle:
            pg.draw.circle(
                self.screen, 
                (128,128,0), 
                self.pos, 
                alignRadius, 
                1
            )
        if alignLine:
            boidList2 = [boid for boid in boidList if boid.id < self.id]
            for boidPos in self.GetNearBoid(boidList, alignRadius, True):
                pg.draw.line(
                    self.screen, 
                    (64,64,192), 
                    self.pos, 
                    boidPos
                )
        if avoidLine:
            boidList2 = [boid for boid in boidList if boid.id < self.id]
            for boidPos in self.GetNearBoid(boidList2, avoidRadius, True):
                pg.draw.line(
                    self.screen, 
                    (255,128,0), 
                    self.pos, 
                    boidPos
                )
            if mouseAvoidLine:
                if (mousePos - self.pos).length() <= 4 * avoidRadius:
                    pg.draw.line(
                        self.screen, 
                        (128,64,0), 
                        self.pos, 
                        mousePos
                    )
        if conformLine:
            if conformStrength != 0:
                pg.draw.line(
                    self.screen, 
                    (128,255,0), 
                    self.pos, 
                    self.pos + self.Conform(boidList, viewRadius, conformStrength)/conformStrength, 
                    1
            )