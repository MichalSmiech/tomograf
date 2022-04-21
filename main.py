from skimage import io, draw
import math
import matplotlib.pyplot as plt
import numpy as np

scans_count = 90
detectors_count = 180
detectors_span = 180

detectors_span = float(detectors_span) / 360.0 * 2.0 * math.pi
sinogram = []

for i in range(scans_count):
    sinogram.append([])

img = io.imread('tomograf-zdjecia/Kropka.jpg', as_gray=True)

center = (int(img.shape[0]/2), int(img.shape[1]/2))
radius = center[0] - 1

angle_step = 2.0 * math.pi / scans_count

for step in range(scans_count):
    angle = step * angle_step
    emitter_loc_x = int(radius * math.cos(angle))
    emitter_loc_x += center[0]
    emitter_loc_y = int(radius * math.sin(angle))
    emitter_loc_y = center[1] - emitter_loc_y
    emitter_loc = (emitter_loc_x, emitter_loc_y)

    detector_locs = []
    scan_max = 0
    for i in range(detectors_count):
        detector_loc_x = int(radius * math.cos(angle + math.pi - detectors_span / 2 + i * detectors_span / (detectors_count - 1)))
        detector_loc_x += center[0]
        detector_loc_y = int(radius * math.sin(angle + math.pi - detectors_span / 2 + i * detectors_span / (detectors_count - 1)))
        detector_loc_y = center[1] - detector_loc_y
        detector_loc = (detector_loc_x, detector_loc_y)
        detector_locs.append(detector_loc)

        line_nd = draw.line_nd(emitter_loc, detector_loc, endpoint=True)
        value = 0
        for j in range(len(line_nd[0])):
            value += img[line_nd[0][j]][line_nd[1][j]]
        value = value / len(line_nd[0])
        sinogram[step].append(value)
        scan_max = max(value, scan_max)

    for i in range(detectors_count):
        sinogram[step][i] /= scan_max


io.imsave('test.jpg', np.array(sinogram))







# draw.line_nd((0,0), (10, 3), endpoint=True)