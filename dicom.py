from pydicom import dcmread
import datetime

class DicomFile:
    def __init__(self):
        self.filepath = None
        self.family_name = None
        self.given_name = None
        self.comments = None
        self.timestamp = None
        self.image = None

    def load(self, filepath):
        self.filepath = filepath
        ds = dcmread(filepath)
        self.family_name = ds.PatientName.family_name
        self.given_name = ds.PatientName.given_name
        self.comments = ds.ImageComments
        self.timestamp = ds.timestamp
        self.image = ds.pixel_array








# def read_dicom(path):
#     import matplotlib.pyplot as plt
#     from pydicom import dcmread
#     from pydicom.data import get_testdata_file
#
#     # fpath = get_testdata_file(path)
#     ds = dcmread(path)
#
#     # Normal mode:
#     print()
#     # print(f"File path........: {fpath}")
#     print(f"SOP Class........: {ds.SOPClassUID} ({ds.SOPClassUID.name})")
#     print()
#
#     pat_name = ds.PatientName
#     display_name = pat_name.family_name + ", " + pat_name.given_name
#     print(f"Patient's Name...: {display_name}")
#     print(f"Patient ID.......: {ds.PatientID}")
#     print(f"Modality.........: {ds.Modality}")
#     # print(f"Study Date.......: {ds.StudyDate}")
#     print(f"Image size.......: {ds.Rows} x {ds.Columns}")
#     # print(f"Pixel Spacing....: {ds.PixelSpacing}")
#
#     # use .get() if not sure the item exists, and want a default value if missing
#     print(f"Slice location...: {ds.get('SliceLocation', '(missing)')}")
#
#     # plot the image using matplotlib
#     plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
#     plt.show()
#
# read_dicom('tomograf-dicom/Kropka.dcm')