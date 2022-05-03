'''
@Date   : 26/2/2022 5:14 PM 
@Author : Peter Chen
@Desc   :
'''

import numpy as np
import open3d as o3d


class LSF(object):
    def __init__(self, target_path, source_path):
        self.target = np.genfromtxt(target_path, delimiter=',', skip_header=1, usecols=(1,2,3))
        self.source = np.genfromtxt(source_path, delimiter=',', skip_header=1, usecols=(1,2,3))


    @staticmethod
    def computeError(target, source):
        # LSF.displayTwoCloud(target, source)
        T = LSF.lsf(target, source)
        target = target @ T[:3, :3].T + T[:3, 3]
        # LSF.displayTwoCloud(target, source)
        # p2pErr = np.sqrt(np.sum((target - source) ** 2, axis=1))
        p2pErr = np.linalg.norm(target - source, axis=1)
        return p2pErr, T


    '''
        @Function: Alignment of two point sets with known p2p correspondences.
        @Reference paper: Least-Squares Fitting of Two 3-D Point Sets
        @Authors: K. S. ARUN, T. S. HUANG, AND S. D. BLOSTEIN
        @Implentation: Peter Chen
    '''
    @staticmethod
    def lsf(tgt, src):
        # 1) Decentroid
        target = tgt - tgt.mean(axis=0)
        source = src - src.mean(axis=0)

        # Equation 11: H matrix
        H = np.zeros((3, 3))
        for i in range(target.shape[0]):
            q = target[i].reshape((3, 1))
            q1 = source[i].reshape((1, 3))
            H += q @ q1

        # Equation 12: SVD
        u, s, vh = np.linalg.svd(H)
        # Equation 13
        X = vh.T @ u.T

        if abs(np.linalg.det(X)) - 1 < 0.1:
            R = X
            t = (src.mean(axis=0) - R @ tgt.mean(axis=0)).reshape((3, 1))
            T = np.vstack((np.hstack((R, t)), np.array([[0,0,0,1]])))
            return T
        else:
            print("\nFails.")


    @staticmethod
    def displayTwoCloud(tls, mls):
        pcd_tls = o3d.geometry.PointCloud()
        pcd_tls.points = o3d.utility.Vector3dVector(tls)
        colors = [[0, 0, 0] for i in range(tls.shape[0])]
        pcd_tls.colors = o3d.utility.Vector3dVector(colors)

        pcd_mls = o3d.geometry.PointCloud()
        pcd_mls.points = o3d.utility.Vector3dVector(mls)
        colors = [[1, 0, 0] for i in range(mls.shape[0])]
        pcd_mls.colors = o3d.utility.Vector3dVector(colors)

        o3d.visualization.draw_geometries([pcd_tls] + [pcd_mls])


if __name__ == '__main__':

    tls_path = target_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Target/202203010000_Z6Terrace_RTC360/Targets/vertexes/vertexes.csv"
    mls_path = source_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Registered/202203010000_Z6Terrace_RTC360/Baseline/vertexes/vertexes.csv"

    lsf = LSF(target_path, source_path)
    geoErrs, T = lsf.computeError(lsf.target, lsf.source)

    print('------------------------------------')
    print('1) Geometrical Error')
    print('------------------------------------')
    for i in range(geoErrs.shape[0] // 4):
        fourVertexesErr = np.mean(geoErrs[4*i: 4*(i+1)])
        print('error of target %d: %f m' % (i, fourVertexesErr))
    print('------------------------------------')
    meanErr = geoErrs.mean()
    print('Mean error: %f m' % meanErr)
    print('------------------------------------')

