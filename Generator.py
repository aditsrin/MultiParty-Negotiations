import xml.etree.ElementTree as ET
import numpy as np
def utilitygen(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    allist = []
    weights = []
    for issues in root.iter('issue'):
        # print(issues.attrib['index'])
        temp = []
        for child in issues:
            # print(child.attrib)
            temp.append(float(child.attrib['evaluation']))
        temp = [i/max(temp) for i in temp]
        allist.append(temp)
    weights = []
    for weight in root.iter('weight'):
        weights.append(float(weight.attrib['value']))
    for j in range(0,len(allist)):
        allist[j] = [i*weights[j] for i in allist[j]]
    # print(allist)
    ans = {}
    t=1
    for i in allist[0]:
        for j in allist[1]:
            for k in allist[2]:
                ans[t] = i+j+k
                t+=1
    return ans

