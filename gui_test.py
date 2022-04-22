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
        [sg.Column(
            [
                [sg.Text("Obraz wejściowy")],
                [sg.Image(key="-INPUT_IMG-")],
            ],
        ),
        sg.Column(
            [
                [sg.Text("Sinogram")],
                [sg.Image(key="-SINOGRAM-")],
            ],
        ),
        sg.Column(
            [
                [sg.Text("Obraz wyjściowy")],
                [sg.Image(key="-OUTPUT_IMG-")],
            ],
        )],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
        ],
        [
            sg.Text("Liczba detektorów:"),
            sg.Input(size=(25, 1), key="-DETECTORS_COUNT-", default_text='180'),
        ],
        [
            sg.Text("Liczba skanów:"),
            sg.Input(size=(25, 1), key="-SCANS_COUNT-", default_text='90'),
        ],
        [
            sg.Text("Rozwartośc układu [stopnie]:"),
            sg.Input(size=(25, 1), key="-DETECTORS_SPAN-", default_text='180'),
        ],
        [
            sg.Text("Postępu obrotu emitera"),
            sg.Slider(orientation='horizontal', key='-SLIDER-', range=(1, 90), enable_events=True),
            sg.Button("Load"),
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
                image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-INPUT_IMG-"].update(data=bio.getvalue())

                scanner.set_config(scans_count=int(values['-SCANS_COUNT-']),
                                   detectors_count=int(values['-DETECTORS_COUNT-']),
                                   detectors_span=int(values['-DETECTORS_SPAN-']))
                window.Element("-SLIDER-").Update(range=(1, scanner.scans_count))
                scanner.load(filename)
                scanner.create_sinogram()
                # image = Image.open(values["-FILE-"])
                myarray = numpy.array(scanner.sinogram) * 255
                image = Image.fromarray(numpy.uint8(myarray))
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-SINOGRAM-"].update(data=bio.getvalue())

                scanner.create_output_img()
                myarray = numpy.array(scanner.output_img) * 255
                image = Image.fromarray(numpy.uint8(myarray))
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-OUTPUT_IMG-"].update(data=bio.getvalue())
        if event == 'Load':
            filename = values["-FILE-"]
            scan_steps = int(values["-SLIDER-"])
            scanner.set_config(scan_steps=scan_steps)
            window.Element("-SLIDER-").Update(range=(1, scanner.scans_count))
            scanner.load(filename)
            scanner.create_sinogram()
            # image = Image.open(values["-FILE-"])
            myarray = numpy.array(scanner.sinogram) * 255
            image = Image.fromarray(numpy.uint8(myarray))
            image.thumbnail((400, 400))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-SINOGRAM-"].update(data=bio.getvalue())

            scanner.create_output_img()
            myarray = numpy.array(scanner.output_img) * 255
            image = Image.fromarray(numpy.uint8(myarray))
            image.thumbnail((400, 400))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-OUTPUT_IMG-"].update(data=bio.getvalue())


    window.close()
if __name__ == "__main__":
    main()