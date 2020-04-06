from scipy.spatial.distance import euclidean
import numpy as np
import re
import matplotlib.pyplot as plt

#Returns an array of the histograms in the k-formule by original order
def getHistograms(raw_line):

    histograms = []
    index = 0

    line = raw_line[2:-2].split(']') #separation of the histograms

    for h in line:  #for each histogram in the line
        histo = h
        if(index == 0):
            histo = histo[1:]   #removing '['
        if(index != 0):
            histo = histo[2:]   #removing ',['
        index += 1
        histograms.append(np.fromstring(histo, dtype=float, sep=','))

    histograms.pop()    #removing empty item
    return histograms   #np.array of floats

#function that reads the kforms in a file
#must be called for each file
#path = k-formlule file path
#returns an array of arrays, each array contains the histograms in a k-formule ordered according to the original file
def readKforms(path):
    with open(path, 'r') as fp:
        line = fp.readline()

        histograms = []     #array of all histograms in the k-formules by original order

        while line: #Reads the file line by line
            histograms.append(getHistograms(line))
            line = fp.readline()
        
        return histograms   #np.array


def rapportSimilitude2(ob1, ob2, angle, second_angle):
    Histo_obj1 = readKforms('../'+str(ob1)+'/kformules/'+str(ob1)+'_'+str(angle)+'.txt')
    Histo_obj2 = readKforms('../'+str(ob2)+'/kformules/'+str(ob2)+'_'+str(second_angle)+'.txt')
    ratios = []
    for kform in range(len(Histo_obj1)):#4 formulas in total
        for histo in range(len(Histo_obj1[kform])):#10 comparaisons in total
            buffer_min = 0
            buffer_max = 0
            for term in range(len(Histo_obj1[kform][histo])):
                buffer_min += min(Histo_obj1[kform][histo][term], Histo_obj2[kform][histo][term])
                buffer_max += max(Histo_obj1[kform][histo][term], Histo_obj2[kform][histo][term])

            ratios.append(buffer_min / buffer_max)  
    return sum(ratios) / 10

def rapportSimilitude(ob1, ob2, angle, second_angle):
    Histo_obj1 = readKforms('../'+str(ob1)+'/kformules/'+str(ob1)+'_'+str(angle)+'.txt')
    Histo_obj2 = readKforms('../'+str(ob2)+'/kformules/'+str(ob2)+'_'+str(second_angle)+'.txt')
    ratios = []
    for kform in range(len(Histo_obj1)):#4 formulas in total
        for histo in range(len(Histo_obj1[kform])):#10 comparaisons in total
            buffer_min = 0
            cardA = 0
            cardB = 0
            for term in range(len(Histo_obj1[kform][histo])):
                buffer_min += min(Histo_obj1[kform][histo][term], Histo_obj2[kform][histo][term])
                cardA += Histo_obj1[kform][histo][term]
                cardB += Histo_obj2[kform][histo][term]
            if(buffer_min == 0 or max(cardA, cardB) == 0):
                ratios.append(0)
            else:
                ratios.append(buffer_min / max(cardA, cardB))  
    return sum(ratios) / 10


def getRapportSimilitude(degrees, ob1, ob2):
    ratios = []

    for angle in range (len(degrees)):
        ratios.append(rapportSimilitude(ob1, ob2, degrees[angle], degrees[angle]))

    return ratios#np.max(ratios)

wset = '2'
wset_lim = 3

degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]
'''
legend = []
for i in range(0, wset_lim+1):
    for j in range(i+1, wset_lim+1):
        rt = getRapportSimilitude(degrees, 'im_'+wset+str(i), 'im_'+wset+str(j))
        plt.plot(degrees, rt)
        legend.append('im_'+wset+str(i)+' & im_'+wset+str(j))
    
plt.legend(legend)
plt.show()
'''
rt = getRapportSimilitude(degrees, 'im_30', 'im_34')
print(rt)