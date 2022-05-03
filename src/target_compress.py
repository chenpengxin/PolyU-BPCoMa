
import os
import glob

import numpy as np
from tqdm import tqdm

class TargetCompress(object):
    def __init__(self, target_path, target_compressed_path):
        self.target_fnames = sorted(glob.glob(os.path.join(target_path, '*.pts')))
        self.target_compressed_fnames = [os.path.join(target_compressed_path, fname[fname.rfind('/')+1:]) for fname in self.target_fnames]


    def compress(self):
        print("Compressing ... ")
        with tqdm(total=len(self.target_fnames)) as pbar:
            for i, fname in enumerate(self.target_fnames):
                # x, y, z, r, g, b, intensity
                pts = np.genfromtxt(fname, delimiter=',')
                xyz = pts[:, :3]
                _, eigenvectors, centroid = self.pca(xyz)
                normal = eigenvectors[:, 2].reshape((3, 1))
                CP = xyz - centroid.reshape((1, 3))
                XP = CP @ normal @ normal.T
                xyz = xyz - XP
                pts[:, :3] = xyz
                np.savetxt(self.target_compressed_fnames[i], pts, fmt='%10.5f', delimiter=' ')
                pbar.update()
        print("\nDone.")
        return



    # 计算 点云的最小成分方向，即法向量方向
    @staticmethod
    def pca(data, sort=True):
        # Decentriod
        centroid = np.array(np.mean(data, axis=0))
        X = np.array(data - centroid)

        # Variance and SVD
        # H: Variance along each feature direction
        # H: symmetric ==> u.transpose() == vh
        H = np.dot(X.transpose(), X) / data.shape[0]
        u, s, vh = np.linalg.svd(H)
        eigenvalues = s  # default as descending order
        eigenvectors = u

        if sort:
            sort = eigenvalues.argsort()[::-1]  # descending order
            eigenvalues = eigenvalues[sort]
            eigenvectors = eigenvectors[:, sort]
        return eigenvalues, eigenvectors, centroid



if __name__ == '__main__':
    target_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Registered/202203010000_Z6Terrace_RTC360/Baseline/raw"
    target_compressed_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Registered/202203010000_Z6Terrace_RTC360/Baseline/compressed"
    TC = TargetCompress(target_path, target_compressed_path)
    TC.compress()