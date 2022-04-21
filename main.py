from skimage import io, draw
import math
import matplotlib.pyplot as plt

scans_count = 1000
detectors_count = 30
detectors_span = 180

detectors_span = float(detectors_span) / 360.0 * 2.0 * math.pi
sinogram = []

for i in range(scans_count):
    sinogram.append([])

img = io.imread('tomograf-zdjecia/Kropka.jpg', as_gray=True)

center = (int(img.shape[0]/2), int(img.shape[1]/2))
radius = center[0] - 1

print(center)

angle_step = 2.0 * math.pi / scans_count

for step in range(scans_count):
    angle = step * angle_step
    emitter_loc_x = int(radius * math.cos(angle))
    emitter_loc_x += center[0]
    emitter_loc_y = int(radius * math.sin(angle))
    emitter_loc_y = center[1] - emitter_loc_y
    emitter_loc = (emitter_loc_x, emitter_loc_y)

    detectors_locs = []
    for i in range(detectors_count):
        detector_loc_x = int(radius * math.cos(angle + math.pi - detectors_span / 2 + i * detectors_span / (detectors_count - 1)))
        detector_loc_x += center[0]
        detector_loc_y = int(radius * math.sin(angle + math.pi - detectors_span / 2 + i * detectors_span / (detectors_count - 1)))
        detector_loc_y = center[1] - detector_loc_y
        detectors_locs.append((detector_loc_x, detector_loc_y))

        rr, cc = draw.line(emitter_loc_x, emitter_loc_y, detector_loc_x, detector_loc_y)
        img[rr, cc] = 1

    break

io.imsave('test.jpg', img)







# draw.line_nd((0,0), (10, 3), endpoint=True)