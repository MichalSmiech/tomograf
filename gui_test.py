# import PySimpleGUI as sg
#
# filename = sg.popup_get_file('Enter the file you wish to process')
#
#
# sg.popup('You entered', filename)

import io
import os
import numpy
import PySimpleGUI as sg
from scanner import Scanner
from PIL import Image
from matplotlib import cm
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
def main():
    scanner = Scanner()
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
        ],
    ]
    window = sg.Window("Image Viewer", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                scanner.load(values["-FILE-"])
                scanner.create_sinogram()
                # image = Image.open(values["-FILE-"])
                myarray = numpy.array(scanner.sinogram) * 255
                image = Image.fromarray(numpy.uint8(myarray))
                # image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
    window.close()
if __name__ == "__main__":
    main()