import PySimpleGUI as sg
import requests
import random
from bs4 import BeautifulSoup

def crawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    WatchList = []
    list = soup.find("ul", {"class": "poster-list -p125 -grid -scaled128"})
    if list == None:
        return None

    list_content = list.find_all("li")

    for item in list_content:
        WatchList.append(item.find("img")["alt"])

    return WatchList

def gui():
    layout = [
        [sg.Text("Enter your letter box username:"), sg.InputText(key="input")],
        [sg.Text("Output:"), sg.Multiline(size=(30,2), key='output', no_scrollbar=True)],
        [sg.Button("Select Random Movie", key='process')]
    ]

    window = sg.Window("Random Movie Selector", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'process':
            url = "https://letterboxd.com/" + values['input'] + "/watchlist/"

            movies = crawler(url)

            if movies == None:
                window['output'].print('no movies in watchlist')
            
            else:
                movie_num = random.randint(0, len(movies)-1)
                random_movie = movies[movie_num]

                window['output'].print(random_movie)

gui()