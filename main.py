import os
import tkinter as tk
from pathlib import Path
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from helpers import Automation


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    dirname = Path(__file__).parent
    #destination = filedialog.askdirectory(
    #    title='Select folder with all the individual movies')
    destination = "D:/TMP/"
    actors_folder = filedialog.askdirectory(
        title='Select folder with all the images of the actors')
    t = Automation(genre='', tagline="", user_rating=5, year='2023', date_added="2023-04-08 00:00:00",
                   actor_path=actors_folder, mypath_video=destination)

    t.move_videos_to_single_folder()
    #t.delete_all_images()
    t.make_change_nfo_file(replace_existing=True)
    t.generate_fanart()
    t.generate_poster()