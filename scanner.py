from skimage import io, draw
import math
import numpy as np

class Scanner:
    def __init__(self):
        self.filename = ''
        self.scans_count = 90
        self.detectors_count = 180
        self.detectors_span = 180
        self.detectors_span = float(self.detectors_span) / 360.0 * 2.0 * math.pi
        self.original_img = None
        self.output_img = None
        self.sinogram = []
        self.center = None
        self.radius = None
        self.angle_step = None
        self.set_config()

    def set_config(self, scans_count=None, detectors_count=None, detectors_span=None):
        if scans_count is not None:
            self.scans_count = scans_count
        if detectors_count is not None:
            self.detectors_count = detectors_count
        if detectors_span is not None:
            self.detectors_span = detectors_span
            self.detectors_span = float(self.detectors_span) / 360.0 * 2.0 * math.pi

        self.sinogram = []
        for i in range(self.scans_count):
            self.sinogram.append([])

        self.angle_step = 2.0 * math.pi / self.scans_count

    def load(self, filename):
        self.filename = filename
        self.original_img = io.imread(filename, as_gray=True)

        self.center = (int(self.original_img.shape[0]/2), int(self.original_img.shape[1]/2))
        self.radius = self.center[0] - 1

    def create_sinogram(self):
        for step in range(self.scans_count):
            angle = step * self.angle_step
            emitter_loc_x = int(self.radius * math.cos(angle))
            emitter_loc_x += self.center[0]
            emitter_loc_y = int(self.radius * math.sin(angle))
            emitter_loc_y = self.center[1] - emitter_loc_y
            emitter_loc = (emitter_loc_x, emitter_loc_y)

            scan_max_value = 0
            for i in range(self.detectors_count):
                detector_loc_x = int(self.radius * math.cos(
                    angle + math.pi - self.detectors_span / 2 + i * self.detectors_span / (self.detectors_count - 1)))
                detector_loc_x += self.center[0]
                detector_loc_y = int(self.radius * math.sin(
                    angle + math.pi - self.detectors_span / 2 + i * self.detectors_span / (self.detectors_count - 1)))
                detector_loc_y = self.center[1] - detector_loc_y
                detector_loc = (detector_loc_x, detector_loc_y)

                line_nd = draw.line_nd(emitter_loc, detector_loc, endpoint=True)
                value = 0
                for j in range(len(line_nd[0])):
                    value += self.original_img[line_nd[0][j]][line_nd[1][j]]
                value = value / len(line_nd[0])
                self.sinogram[step].append(value)
                scan_max_value = max(value, scan_max_value)

            for i in range(self.detectors_count):
                self.sinogram[step][i] /= scan_max_value

    def create_output_img(self):
        self.output_img = np.zeros(self.original_img.shape)
        global_max = 0
        for step in range(self.scans_count):
            angle = step * self.angle_step
            emitter_loc_x = int(self.radius * math.cos(angle))
            emitter_loc_x += self.center[0]
            emitter_loc_y = int(self.radius * math.sin(angle))
            emitter_loc_y = self.center[1] - emitter_loc_y
            emitter_loc = (emitter_loc_x, emitter_loc_y)

            for i in range(self.detectors_count):
                detector_loc_x = int(self.radius * math.cos(
                    angle + math.pi - self.detectors_span / 2 + i * self.detectors_span / (self.detectors_count - 1)))
                detector_loc_x += self.center[0]
                detector_loc_y = int(self.radius * math.sin(
                    angle + math.pi - self.detectors_span / 2 + i * self.detectors_span / (self.detectors_count - 1)))
                detector_loc_y = self.center[1] - detector_loc_y
                detector_loc = (detector_loc_x, detector_loc_y)

                line_nd = draw.line_nd(emitter_loc, detector_loc, endpoint=True)
                value = self.sinogram[step][i]
                for j in range(len(line_nd[0])):
                    self.output_img[line_nd[0][j]][line_nd[1][j]] += value
                    global_max = max(self.output_img[line_nd[0][j]][line_nd[1][j]], global_max)

        for i in range(self.output_img.shape[0]):
            for j in range(self.output_img.shape[1]):
                self.output_img[i][j] /= global_max
