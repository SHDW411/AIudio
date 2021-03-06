import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import os
import csv
from tkinter import *
from tkinter.filedialog import askdirectory
import sys
import datetime
import csv
from tinytag import TinyTag

import musicbrainzngs as mbz


#File chooser
#root = Tk()
#root.minsize(300, 300)

list_of_songs = []
index = 0
current_file = "E:\\05 Perfect Strangers2.wav"
current_file_2 = "E:\\04 - Les chants magnetiques IV.flac"
current_file_3 = "E:\\Gabriel's Oboe.mp3"
current_file_4 = "E:\\01 - The RobotsOGG.ogg"
current_file_5 = "C:\\Users\\Lenovo PC\\Music\\Fleetwood Mac - The Very Best Of.. (2CD)[FLAC]\\Fleetwood Mac - The Very Best Of (CD 1)\\The Very Best Of (CD 1)\\16. Big Love (Live, 1997).mp3"
current_path = ''
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
FOLDER_PATH = r'E:\\Python'
FIELDNAMES = ['name', 'title', 'artist', 'album', 'date', 'genre', 'duration']

def directory_chooser():
    directory = askdirectory()
    os.chdir(directory)

    current_path = directory

    list_of_paths = []

    for format in FORMATS:
        for files in os.listdir(directory):
            if files.endswith(format):
                list_of_paths.append(directory + files)

    return list_of_paths

def make_base():
    with open(FOLDER_PATH + r'\\{}'.format('tags_base.csv'), 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=';')
        csv_writer.writeheader()


def info(current_file):
    curr_tags = {}
    if current_file.endswith('.flac'):
        current_audio = FLAC(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                time = mutagen.File(current_file)
                int_time = int(time.info.length)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                except KeyError:
                    curr_tags[curr_key] = "None"
                except TypeError:
                    curr_tags[curr_key] = "None"
    elif current_file.endswith('.mp3'):
        current_audio = EasyID3(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                time = mutagen.File(current_file)
                int_time = int(time.info.length)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                except KeyError:
                    curr_tags[curr_key] = "None"
                except TypeError:
                    curr_tags[curr_key] = "None"
    elif current_file.endswith('.wav'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                current_audio_aux = TinyTag.get(current_file)
                int_time = int(current_audio_aux.duration)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                except TypeError:
                    try:
                        current_audio_aux = TinyTag.get(current_file)
                        if curr_key == 'title':
                            curr_tags[curr_key] = current_audio_aux.title
                        if curr_key == 'artist':
                            curr_tags[curr_key] = current_audio_aux.artist
                        if curr_key == 'album':
                            curr_tags[curr_key] = current_audio_aux.album
                        if curr_key == 'date':
                            curr_tags[curr_key] = current_audio_aux.year
                        if curr_key == 'genre':
                            curr_tags[curr_key] = current_audio_aux.genre
                    except KeyError:
                        curr_tags[curr_key] = "None"
                    except TypeError:
                        curr_tags[curr_key] = "None"
    elif current_file.endswith('.ogg'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                time = mutagen.File(current_file)
                int_time = int(time.info.length)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                except KeyError:
                    curr_tags[curr_key] = "None"
                except TypeError:
                    curr_tags[curr_key] = "None"
    temp_path = FOLDER_PATH + r'\\{}'.format('tags_base.csv')
    flag = 0
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            ct = 0
            for row in csv_reader:
                 if row['name'] == curr_tags['name']:
                    flag = 1
        if flag == 0:
            with open(temp_path, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
                csv_writer.writerow(curr_tags)
    else:
        make_base()
        with open(temp_path, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            csv_writer.writerow(curr_tags)

    return curr_tags

def update_track(current_file, new_tags):
    curr_tags = {}
    if current_file.endswith('.flac'):
        current_audio = FLAC(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                time = mutagen.File(current_file)
                int_time = int(time.info.length)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                current_audio[curr_key] = new_tags[key]
                current_audio.save()
                curr_tags[curr_key] = str(new_tags[key])
    elif current_file.endswith('.mp3'):
        current_audio = EasyID3(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                time = mutagen.File(current_file)
                int_time = int(time.info.length)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                current_audio[curr_key] = new_tags[key]
                current_audio.save()
                curr_tags[curr_key] = str(new_tags[key])
    elif current_file.endswith('.wav'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                current_audio_aux = TinyTag.get(current_file)
                int_time = int(current_audio_aux.duration)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                curr_tags[curr_key] = str(new_tags[key])
    elif current_file.endswith('.ogg'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
            elif key == 'duration':
                time = mutagen.File(current_file)
                int_time = int(time.info.length)
                duration = datetime.timedelta(seconds=int_time)
                curr_tags[curr_key] = str(duration)
            else:
                current_audio[curr_key] = new_tags[key]
                current_audio.save()
                curr_tags[curr_key] = str(new_tags[key])
    temp_path = FOLDER_PATH + r'\\{}'.format('tags_base.csv')
    templist = []
    point = 0
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            for row in csv_reader:
                if point == 0:
                    pass
                    point += 1
                elif row['name'] == curr_tags['name']:
                    templist.append((curr_tags))

                else:
                    templist.append((row))

        os.remove(temp_path)
        make_base()
        with open(temp_path, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            for row in templist:
                csv_writer.writerow(row)
    else:
        make_base()
        with open(temp_path, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            csv_writer.writerow(curr_tags)

    return curr_tags

def artist_info(current_file): #name/type(Group/Person)/country/Begin/Begin area
    data = []
    key = ['name', 'type', 'country','life-span', 'begin-area']
    mbz.set_useragent("AIudio", "0.1")
    song = info(current_file)
    result = mbz.search_artists(artist=song['artist'])
    describe = result['artist-list'][0]
    for par in key:
        if par == 'life-span':
            try:
                data.append(describe[par]['begin'])
            except KeyError:
                data.append('None')
        elif par == 'begin-area':
            try:
                data.append(describe[par]['name'])
            except KeyError:
                data.append('None')
        else:
            try:
                data.append(describe[par])
            except KeyError:
                data.append('None')
    return data


def dicography(current_file):
    data = []
    mbz.set_useragent("AIudio", "0.1")
    song = info(current_file)
    result = mbz.search_artists(artist=song['artist'])
    describe = result['artist-list'][0]
    artist_id = describe['id']
    try:
        result = mbz.get_artist_by_id(artist_id, includes=["release-groups"], release_type=["album", "ep"])
    except mbz.WebServiceError as exc:
        print("Something went wrong with connection")
    else:
        for release_group in result["artist"]["release-group-list"]:
            data.append(("{title} ({type})".format(title=release_group["title"],type=release_group["type"])))

    return data

def add_to_base():
    list_of_songs = []
    list_of_songs = directory_chooser()
    print(list_of_songs)
    for song in list_of_songs:
        info(song)

def addTagsToMain():
    copy_base = []
    copy_main = []
    curr_file_path = ''

    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'r') as file:
        for line in file:
            contents = file.read()
            if contents.startswith("\""):
                if contents != curr_file_path:
                    curr_file_path = contents
            elif contents.startswith("<"):
                continue
            else:
                copy_main.append(curr_file_path+contents)
    file.close()

    if os.path.exists(FOLDER_PATH + r'\\{}'.format('tags_base.csv')):
        with open(FOLDER_PATH + r'\\{}'.format('tags_base.csv'), 'r') as csv_file:
            point = 0
            csv_reader = csv.DictReader(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            for row in csv_reader:
                if point == 0:
                    pass
                    point += 1
                else:
                    if row['name'].split('\\')[:-1] != curr_file_path:
                        curr_file_path = row['name'].split('\\')[:-1]
                        copy_base.append(((str(row['name'].split('\\')[:-1])).replace("', '","\\")).strip("[\'\"\"\']"))
                    copy_base.append(str(row['name'].split('\\')[-1:]).strip("[\'\"\"\']"))
                    copy_base.append("< {artist}:0 {album}:0 {date}:0 {genre}:0 {duration}:0 >".format(artist=row['artist'], album=row['album'], date=row['date'], genre=row['genre'], duration=row['duration']))

    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'w') as file:
        for i in copy_base:
            print(i)
            file.write(i+"\n")
    file.close()


new_tags_1 = {'title': 'ghdhrtcvrcetwcgrtgcwt', 'artist': 'Roxy music', 'album': 'PASSSAT', 'date': '1.9', 'genre': 'TDI',}



#directory_chooser()
#add_to_base()
#tester = update_track(current_file_4, new_tags_1)
#tester2 = info(current_file_5)
#print(tester2)

#print(artist_info(current_file_4))
#print(dicography(current_file_4))
