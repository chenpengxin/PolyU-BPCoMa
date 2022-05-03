
import os
import numpy as np

from ls2ptsets import LSF
from colorization_error import ColorizationError


if __name__ == '__main__':
    proj_path = os.path.dirname(os.path.dirname(__file__))
    tls_path = target_path = os.path.join(proj_path, "baseline/Area_1/TLS")
    mls_path = source_path = os.path.join(proj_path, "baseline/Area_1/MLS")

    # 1) Geometrical Error
    lsf = LSF(os.path.join(target_path, 'vertexes/vertexes.csv'), os.path.join(source_path, 'vertexes/vertexes.csv'))
    geoErrs, _ = lsf.computeError(lsf.target, lsf.source)

    print('------------------------------------')
    print('1) Geometrical Error')
    print('------------------------------------')
    for i in range(geoErrs.shape[0] // 4):
        fourVertexesErr = np.mean(geoErrs[4 * i: 4 * (i + 1)])
        print('error of target %d: %f m' % (i, fourVertexesErr))
    print('------------------------------------')
    meanErr = geoErrs.mean()
    print('Mean error: %f m' % meanErr)
    print('------------------------------------')

    # 2) Colorization Error
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
