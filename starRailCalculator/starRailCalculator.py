import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np



def GetDamage(attack, critRate, critDmg):
    return round(attack * (1 - critRate) + attack * critRate * critDmg, 4)

def GetCritStats(atk, baseCritRate, baseCritDmg, critRateIncrement, critDmgIncrement):
    CritRate = []
    CritDmg = []
    plotXAxis = []
    plotYAxis = []

    critRate = baseCritRate
    while critRate < 1:
        plotYAxis.append(critRate * 100)
        critDmg = baseCritDmg
        crCritRate = round(critRate + critRateIncrement, 2)
        CritRateRow = []
        CritDmgRow = []

        while critDmg < 3:
            plotXAxis.append(critDmg * 100 - 100)
            beforeDmg = atk * (1 - critRate) + atk * critRate * critDmg
            crCritDmg = round(critDmg + critDmgIncrement, 2)
            if crCritRate > 1: crCritRate = 1
            CritRateRow.append(GetDamage(atk, crCritRate, critDmg) - beforeDmg)
            CritDmgRow.append(GetDamage(atk, critRate, crCritDmg) - beforeDmg)
            
            critDmg = crCritDmg
        critRate = round(critRate + critRateIncrement, 2)
        CritRate.append(CritRateRow)
        CritDmg.append(CritDmgRow)
        if  critRate > 1: critRate = 1
    return CritRate, CritDmg, plotXAxis, plotYAxis



def DrawGraph(CritRate, CritDmg, atk, XAxis, YAxis):
    best = []
    for i in range(len(CritRate)):
        bestRow = []
        for y in range(len(CritRate[i])):
            if CritRate[i][y] > CritDmg[i][y]:
                if CritRate[i][y] > atk:
                    bestRow.append(1)
                else:
                    bestRow.append(2)
            else:
                if CritDmg[i][y] > atk:
                    bestRow.append(0)
                else:
                    bestRow.append(2)
        best.append(bestRow)

    cMap = ListedColormap(['#13274f', '#ce1141', '#e7a801'])
    imgplot = plt.imshow(best, aspect="auto", cmap=cMap, extent=[XAxis[0], XAxis[-1], YAxis[-1], YAxis[0]])
    #plt.plot(plotAxis, CritRate, label="Crit rate")
    #plt.plot(plotAxis, CritDmg, label="Crit damage")
    plt.xlabel("Crit damage")
    plt.ylabel("Crit rate")
    plt.colorbar()
    plt.show()

def CompareStatIncreases(baseAtk, crAtk, critRate, critDmg, atkInc, rateInc, dmgInc):
    baseDamage = GetDamage(crAtk, critRate, critDmg)
    atkWin = round(GetDamage(crAtk + baseAtk * atkInc, critRate, critDmg) - baseDamage)
    rateWin = round(GetDamage(crAtk, critRate + rateInc, critDmg) - baseDamage)
    dmgWin = round(GetDamage(crAtk, critRate, critDmg + dmgInc) - baseDamage)
    text = " is the most beinificial stat increase"
    if (atkWin > rateWin and atkWin > dmgWin):
        text = "Atk stat" + text
    elif (rateWin > dmgWin):
        text = "Crit rate stat" + text
    else:
        text = "Crit damage stat" + text
    print(text)
    print("Atk increase results in", atkWin, "more damage")
    print("Crit rate increase results in", rateWin, "more damage")
    print("Crit damage increase results in", dmgWin, "more damage")


baseAtk = 1200
crAtk = 2000
atkIncBase = 13.333
critRate = 0
critDmg = 1.5
critRateIncrement = 0.01
critDmgIncrement = 0.02
critRateCompare = 0.324
critDmgCompare = 0.648

CritRate, CritDmg, XAxis, YAxis = GetCritStats(crAtk, critRate, critDmg, critRateIncrement, critDmgIncrement)
DrawGraph(CritRate, CritDmg, atkIncBase, XAxis, YAxis)

baseAtk = 1169
crAtk = 3289
critRate = 0.571
critDmg = 2.638
atkInc = 0.04
rateInc = 0.03
dmgInc = 0.06
CompareStatIncreases(baseAtk, crAtk, critRate, critDmg, atkInc, rateInc, dmgInc)