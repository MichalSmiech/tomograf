from pydicom import dcmread
import pydicom
import datetime
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import UID
import pydicom._storage_sopclass_uids

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
        self.timestamp = datetime.datetime.fromtimestamp(ds.timestamp)
        self.image = ds.pixel_array

    def save(self,
             filepath,
             family_name,
             given_name,
             comments,
             timestamp,
             image):
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = UID('1.2.840.10008.5.1.4.1.1.2')
        file_meta.MediaStorageSOPInstanceUID = UID("1.2.3")
        file_meta.ImplementationClassUID = UID("1.2.3.4")
        file_meta.TransferSyntaxUID = UID("1.2.840.10008.1.2.1")
        file_meta.FileMetaInformationGroupLength = 206

        ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)

        ds.PatientName = f"{family_name}^{given_name}"
        ds.ImageComments = comments
        ds.timestamp = timestamp.timestamp()
        ds.PixelData = image.tobytes()
        ds.Rows, ds.Columns = image.shape
        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.SamplesPerPixel = 1
        ds.PixelRepresentation = 0
        ds.PhotometricInterpretation = 'MONOCHROME2'
        ds.ImagesInAcquisition = "1"
        ds.InstanceNumber = 1
        ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0


        ds.is_little_endian = True
        ds.is_implicit_VR = False

        ds.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
        ds.PatientID = "123456"

        ds.Modality = "CT"
        ds.SeriesInstanceUID = pydicom.uid.generate_uid()
        ds.StudyInstanceUID = pydicom.uid.generate_uid()
        ds.FrameOfReferenceUID = pydicom.uid.generate_uid()

        ds.read_little_endian = True
        ds.read_encoding = 'iso8859'

        dt = timestamp
        ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')
        ds.ContentTime = timeStr

        pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)
        ds.save_as(filepath)