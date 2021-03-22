import PySimpleGUI as sg

from Scrapers.FileList.FilelistTorrentData import FileListTorrentData

first_line_colum = [
    [sg.Text("Welcome to Movie Downloader using FileList")],
    [sg.Text("Enter movie name : "), sg.In(size=(25, 1), enable_events=True, key="movie_name")],
    [sg.Text("Destination folder : "), sg.In(size=(25, 1), enable_events=True, key="destiantion"),
     sg.FolderBrowse("Chose files")],
    [sg.Submit("Start scraper", button_color=('white', 'red'), key='scrape')]
]

theme_column = [
    [sg.Text("Click a theme from the list below", justification="center"),
     sg.Listbox(values=sg.theme_list(), size=(20, 12), key="themes", enable_events=True)]
]


class FileListTorrentUI():
    def __init__(self, data: FileListTorrentData):
        self.data = data

    def get_layout(self):
        layout = [
            [sg.Text(f"Name : {self.data.name}")],
            [sg.Text(f'Size: {self.data.size}')],
            [sg.Text(f'Dw Speed: {self.data.download_speed}')],
            [sg.Text(f'Freeleech: {self.data.has_freeleech}')],
        ]

        return layout


# scraper = FileListScraper()
example = FileListTorrentData(name="Thor", size=10, seeders=500, has_freeleech=True,
                              download_speed=10.4, download_link="", duration=10)
example_ui = FileListTorrentUI(example)
stuff = []
options = [
    [sg.Listbox(stuff)],
]
layout_good = [
    [
        sg.Column(first_line_colum),
        sg.VSeparator(),
        sg.Column(options),
        sg.Column(theme_column)
    ]
]
sg.set_options(margins=(0, 0), element_padding=(0, 0))
layout = [
    [sg.Button("Hei click me", pad=(0,0,0,0))],
    [sg.Button("Hei click me", pad=(0,0,0,0))],
    [sg.Button("Hei click me", pad=(0,0,0,0))],
]
window = sg.Window("Movie Downloader", layout=layout, margins=(200, 200), resizable=True, grab_anywhere=True)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == 'scrape':
        file_name = values['movie_name']
        # data = scraper.scrape(file_name)
        # window['options'].update(data)
