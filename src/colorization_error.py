

import os
import glob
import numpy as np
import open3d as o3d
from scipy import spatial
import colorsys

from ls2ptsets import LSF


class ColorizationError(object):
    def __init__(self, target_path, source_path):
        target_vertexes = np.genfromtxt(os.path.join(target_path, "vertexes/vertexes.csv"), delimiter=',', skip_header=1, usecols=(1, 2, 3))
        source_vertexes = np.genfromtxt(os.path.join(source_path, "vertexes/vertexes.csv"), delimiter=',', skip_header=1, usecols=(1, 2, 3))

        target_fnames = sorted(glob.glob(os.path.join(target_path, "raw/*.pts")))
        source_fnames = sorted(glob.glob(os.path.join(source_path, "compressed/*.pts")))

        self.target_vertexes = [target_vertexes[4*i: 4*(i+1)] for i in range(len(target_fnames))]
        self.source_vertexes = [source_vertexes[4 * i: 4 * (i + 1)] for i in range(len(source_fnames))]

        # print("Reading data ...")
        self.target_pts = [np.genfromtxt(fn, delimiter=',') for fn in target_fnames]
        self.source_pts = [np.genfromtxt(fn, delimiter=',') for fn in source_fnames]


    def compteError(self):
        # print("Data loaded, computing ...")
        colorErrs = []

        for i in range(len(self.target_pts)):
            # 1) align
            _, T = LSF.computeError(self.target_vertexes[i][:, :3], self.source_vertexes[i][:, :3])
            target = np.hstack((self.target_pts[i][:, :3] @ T[:3, :3].T + T[:3, 3], self.target_pts[i][:, 3:]))
            source = self.source_pts[i]
            # LSF.displayTwoCloud(target[:, :3], source[:, :3])

            # downsample
            pcd_target = o3d.geometry.PointCloud()
            pcd_target.points = o3d.utility.Vector3dVector(target[:, :3])
            pcd_target.colors = o3d.utility.Vector3dVector(target[:, 3:6] / 255)
            pcd_target = pcd_target.voxel_down_sample(voxel_size=0.01)

            pcd_source = o3d.geometry.PointCloud()
            pcd_source.points = o3d.utility.Vector3dVector(source[:, :3])
            pcd_source.colors = o3d.utility.Vector3dVector(source[:, 3:6] / 255)
            pcd_source = pcd_source.voxel_down_sample(voxel_size=0.01)

            # o3d.visualization.draw_geometries([pcd_target] + [pcd_source])

            target = np.asarray(pcd_target.points)
            target_hue = np.asarray([colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])[0] for rgb in list(np.asarray(pcd_target.colors))])
            source = np.asarray(pcd_source.points)
            source_hue = np.asarray([colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])[0] for rgb in list(np.asarray(pcd_source.colors))])

            # p2p correspondence
            targetKdTree = spatial.KDTree(target)
            _, targetInds = targetKdTree.query(source)
            target_correspondence_hue = target_hue[targetInds]
            colorErrs.append(np.mean(np.abs(source_hue - target_correspondence_hue)))

        return np.asarray(colorErrs)






if __name__ == '__main__':

    tls_path = target_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Target/202203010000_Z6Terrace_RTC360/Targets"
    mls_path = source_path = "/media/peter/Passport1T/Dataset/BPCoMa/TLS_Registered/202203010000_Z6Terrace_RTC360/Baseline"

    CE = ColorizationError(target_path, source_path)
    colorErrs = CE.compteError()

    print('------------------------------------')
    print('2) Colorization Error')
    print('------------------------------------')
    for i, err in enumerate(colorErrs):
        print('error of target %d: %f' % (i, err))
    print('------------------------------------')
    meanErr = colorErrs.mean()
    print('Mean error: %f' % meanErr)
    print('------------------------------------')
