import PySimpleGUI as sg

data = {
    "name": "Thor",
    'description': 'The powerful but arrogant god Thor is cast out of Asgard to live amongst humans in Midgard (Earth), where he soon becomes one of their finest defenders.',
    'genres': ['Action', 'Adventure', 'Fantasy'],
    'stars': [('Chris Hemsworth', 1165110), ('Anthony Hopkins', 1165110), ('Natalie Portman ', 1165110)],
    'writes': [('Ashley Miller (screenplay) (as Ashley Edward Miller)', 1005420),
               ('Zack Stentz (screenplay)            | 6 more credits\xa0»', 1005420)],
    'cast': [{'star': 'Chris Hemsworth', 'star_id': 1165110, 'character': 'Thor', 'character_id': 800369},
             {'star': 'Natalie Portman', 'star_id': 204, 'character': 'Jane Foster', 'character_id': 800369},
             {'star': 'Tom Hiddleston', 'star_id': 1089991, 'character': 'Loki', 'character_id': 800369},
             {'star': 'Anthony Hopkins', 'star_id': 164, 'character': 'Odin', 'character_id': 800369},
             {'star': 'Stellan Skarsgård', 'star_id': 1745, 'character': 'Erik Selvig', 'character_id': 800369},
             {'star': 'Kat Dennings', 'star_id': 993507, 'character': 'Darcy Lewis', 'character_id': 800369},
             {'star': 'Clark Gregg', 'star_id': 163988, 'character': 'Agent Coulson', 'character_id': 800369},
             {'star': 'Colm Feore', 'star_id': 272173, 'character': 'King Laufey', 'character_id': 800369},
             {'star': 'Idris Elba', 'star_id': 252961, 'character': 'Heimdall', 'character_id': 800369},
             {'star': 'Ray Stevenson', 'star_id': 829032, 'character': 'Volstagg', 'character_id': 800369},
             {'star': 'Tadanobu Asano', 'star_id': 38355, 'character': 'Hogun', 'character_id': 800369},
             {'star': 'Josh Dallas', 'star_id': 2796047, 'character': 'Fandral', 'character_id': 800369},
             {'star': 'Jaimie Alexander', 'star_id': 1526352, 'character': 'Sif', 'character_id': 800369},
             {'star': 'Rene Russo', 'star_id': 623, 'character': 'Frigga', 'character_id': 800369},
             {'star': 'Adriana Barraza', 'star_id': 56770, 'character': 'Isabela Alvarez', 'character_id': 800369}],
    'ratings': 1,
    'directors': [('Kenneth Branagh', 110)], 'release_day': '6 May 2011', 'country': 'USA', 'language': 'English',
    'filming_locations': ['Galisteo', 'New Mexico', 'USA'], 'budget': 150000000, 'total_gross': 449326618,
    'duration': 115
}

sg.theme("dark")
tab1_layout = [[sg.Button(f'Some text {i} {j}') for i in range(3) for j in range(3)]]
tab1_layout = []
for i in range(3):
    layout_row = []
    for j in range(3):
        layout_row.append(sg.Button(f'Some text {i} {j}'))
    tab1_layout.append(layout_row)

tab2_layout = [[sg.Text('This is inside tab 2', text_color='yellow', size=(20, 1)), sg.VerticalSeparator(color='red')],
               [sg.HorizontalSeparator(color='red')],
               [sg.In(key='in', text_color='blue')]]
layout = [
    [
        sg.Frame(
            title="Frame",
            pad=(0, 0),
            key='frame',
            layout=
            [[
                sg.TabGroup(
                    pad=((10, 10), (20, 20)),

                    layout=[
                        [
                            sg.Tab("File", layout=tab1_layout),
                            sg.Tab("Edit", layout=[[]]),
                            sg.Tab("View", layout=[[]]),
                            sg.Tab("Navigate", layout=[[]])
                        ]
                    ])
            ]]
        )
    ]

    # [sg.Text(data["name"])],
    # [sg.Text(data["release_day"])]
]
window = sg.Window("Movie Downloader", layout=layout, margins=(100, 100), grab_anywhere=True)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
