import os.path

import numpy as np


def extract(path):
    txt = os.path.join(path, "vertexes_copy_from_cloudcompare.txt")
    csv = os.path.join(path, "vertexes.csv")

    with open(txt, 'r') as f:
        lines = f.readlines()

    pts = []
    for line in lines:
        if line[0] != 'P':
            continue
        ptstr = line[line.find('(')+1: line.find(')')].split(';')
        pts.append(ptstr)

    pts = np.asarray(pts)



    with open(csv, 'wb') as f:
        header = bytes("ID,X,Y,Z\n", encoding="utf8")
        f.write(header)

        for i, pt in enumerate(pts):
            id_xyz = str(i+1) + ',' + str(pt[0]) + ',' + str(pt[1]) + ',' + str(pt[2]) + '\n'
            id_xyz = bytes(id_xyz, encoding="utf8")
            f.write(id_xyz)




if __name__ == '__main__':
    TLS_targets_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Target/202203070000_Tunnel_RTC360/Targets/vertexes"
    MLS_targets_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Registered/202203010000_Z6Terrace_RTC360/Baseline/vertexes"

    extract(MLS_targets_path)