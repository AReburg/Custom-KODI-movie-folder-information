import numpy as np
import cv2
import os
from pathlib import Path
from PIL import Image
from os import listdir
from os.path import isfile, join, exists
from random import randrange
import re
import shutil



class Automation():
    def __init__(self, genre, tagline, user_rating, year, date_added, actor_path, mypath_video):
        """ """
        self.genre = genre
        self.tagline = tagline
        self.actor_path = actor_path
        self.actor_list = self.get_actor_list()
        self.role = "Actress"
        self.absolut_path_artwork_actors = 'nfs://10.0.0.1/volume1/videos/actors/'
        self.absolut_path_artwork = 'nfs://10.0.0.1/volume1/TEMP/'
        self.set = ""
        self.uid = "home"
        self.date_added = date_added
        self.year = year
        self.user_rating = user_rating
        self.mypath_video = mypath_video
        self.num_rows_pst = 3
        self.num_col_pst = 1
        self.num_rows_fan = 2
        self.num_col_fan = 2
        self.number_of_poster = 3
        self.subfolders = [f.path for f in os.scandir(self.mypath_video) if f.is_dir()]


    def make_nfo_file(self, file_path, title, duration, width, height, runtime):
        """ Generate NFO File for KODI """

        actors = self.get_actor(title)
        f = open(file_path, "w+")
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n")
        f.write("<movie>\n")
        f.write(f"<title>{title}</title>\n")
        f.write("<originaltitle></originaltitle>\n")
        f.write(f"<userrating>{self.user_rating}</userrating>\n")
        f.write("<top250>0</top250>\n")
        f.write("<outline></outline>\n")
        f.write("<plot></plot>\n")
        f.write(f"<tagline>{self.tagline}</tagline>\n")
        f.write(f"<runtime>{round(runtime)}</runtime>\n")
        #f.write("<thumb aspect=\"poster\" preview=\"\">" +"</thumb>" +'\n')
        f.write("<fanart>\n")
        #for idx in range(self.num_rows_fan * self.num_col_fan):
        #    fanart = f"{title}-fanart{idx}.jpg"
        #    f.write(f"     <thumb preview=\"{self.absolut_path_artwork}{title}/{fanart}\>{self.absolut_path_artwork}{title}/{fanart}</thumb>\n")
        f.write("</fanart>\n")
        f.write("<mpaa></mpaa>\n")
        f.write(f"<playcount>{0}</playcount>\n")
        f.write("<lastplayed></lastplayed>\n")
        f.write("<id></id>\n")
        f.write(f"<uniqueid type=\"home\" default=\"true\">{self.uid}</uniqueid>\n")
        f.write(f"<genre>{self.genre}</genre>\n")
        f.write("<set>\n")
        f.write(f"     <name>{self.set}</name>\n")
        f.write("     <overview></overview>\n")
        f.write("</set>\n")
        f.write("<director></director>\n")
        f.write("<premiered></premiered>\n")
        f.write(f"<year>{self.year}</year>\n")
        f.write("<status></status>\n")
        f.write("<code></code>\n")
        f.write("<aired></aired>\n")
        f.write("<fileinfo>\n")
        f.write("     <streamdetails>\n")
        f.write("         <video>\n")
        f.write("             <codec>h264</codec>\n")
        f.write(f"             <aspect>{round(width/height, 2)}</aspect>\n")
        f.write(f"             <width>{width}</width>\n")
        f.write(f"             <height>{height}</height>\n")
        f.write(f"             <durationinseconds>{round(duration/60)}</durationinseconds>\n") # minutes
        f.write("             <stereomode></stereomode>\n")
        f.write("         </video>\n")
        f.write("     </streamdetails>\n")
        f.write("</fileinfo>\n")
        for idx, i in enumerate(actors):
            f.write("<actor>\n")
            f.write(f"    <name>{i}</name>\n")
            f.write(f"    <role>{self.role}</role>\n")
            f.write(f"    <order>{idx}</order>\n")
            f.write(f"    <thumb>{self.absolut_path_artwork_actors}{i}.jpg</thumb>\n")
            f.write("</actor>\n")
        f.write("</resume>\n")
        f.write("    <position>0.000000</position>\n")
        f.write("    <total>0.000000</total>\n")
        f.write("</resume>\n")
        f.write(f"<showlink>{title}</showlink>\n")
        f.write(f"<dateadded>{self.date_added}</dateadded>\n")
        f.write("</movie>")
        f.close()
        print(f"File: {file_path} created.")


    def generate_poster(self):
        """ generate KODI poster"""
        for idy, z in enumerate(self.subfolders):
            vid = self.get_video_file(z)
            video_path = z + "/" + vid
            path_nfo = z + "/" + os.path.splitext(vid)[0]
            try:
                for k in range(self.number_of_poster):
                    if k == 0:
                        poster_path = f"{path_nfo}-poster.jpg"
                    else:
                        poster_path = f"{path_nfo}-poster{k}.jpg"
                    cap = cv2.VideoCapture(video_path)
                    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    num_images = self.num_rows_pst * self.num_col_pst
                    x = 24*60*4*(k+1) #sekunden die übersprungen werden


                    interval = round((length-x)/num_images)
                    images = []
                    for idx in range(num_images):
                        cap.set(1, x)
                        ret, frame = cap.read()
                        x = x + interval
                        images.append(frame)
                    cap.release()
                    cv2.destroyAllWindows()
                    hori = []

                    for i in range(self.num_rows_pst * self.num_col_pst):
                        if (i % self.num_col_pst) == 0 and i == 0:
                            k = []
                            m = 0
                            for j in range(self.num_col_pst):
                                k.append(images[m])
                                m = m + 1
                            try:
                                hori.append(np.concatenate((k), axis=1))
                            except:
                                pass
                        if (i % self.num_col_pst) == 0 and i > 0:
                            k = []
                            m = 0
                            for j in range(self.num_col_pst):
                                k.append(images[i + m])
                                m = m + 1
                            hori.append(np.concatenate((k), axis=1))
                        Vertical_attachment = np.vstack(hori)
                        filename_thumbnail= str(poster_path)
                        cv2.imwrite(filename_thumbnail, Vertical_attachment)
            except Exception as e:
                print(f"Failed for file: {poster_path}, {e}")
            print("Poster Progress: ", str(round(idy / len(self.subfolders) * 100, 1)), "%")


    def delete_all_images(self):
        """ delete all images in all self.subfolders"""
        for z in self.subfolders:
            for images in os.listdir(z):
                if images.endswith(".jpg"):
                    print("Remove: ", images, "in ", z)
                    os.remove(os.path.join(z, images))


    def get_all_files_in_path(self):
        """ """
        video_files = [f for f in listdir(self.mypath_video) if isfile(join(self.mypath_video, f))]
        return video_files


    def make_video_dir(self, video_name):
        """ """
        path = self.mypath_video + video_name
        path_wo_extension = os.path.splitext(path)[0] #remove extension!!!
        try:
            if not os.path.exists(path_wo_extension):
                os.makedirs(path_wo_extension)
                return path_wo_extension
        except OSError:
            print('Error: Creating directory of data')


    def move_file_to_folder(self, video_name, path):
        vid_from = self.mypath_video + video_name
        vid_to = path + "/" + video_name
        os.rename(vid_from, vid_to)


    def move_videos_to_single_folder(self):
        videos = self.get_all_files_in_path()
        for i in videos:
            self.move_file_to_folder(i, self.make_video_dir(i))


    def get_video_file(self, video):
        return [i for i in os.listdir(video) if i.find(".jpg") == -1 and i.find(".nfo") == -1 and i.find(".db") == -1][0]


    def make_change_nfo_file(self, replace_existing=False):
        for z in self.subfolders:
            vid = self.get_video_file(z)
            video_path = z + "/" + vid
            path_nfo = z + "/" + os.path.splitext(vid)[0] +".nfo"
            title = os.path.splitext(vid)[0]
            cap = cv2.VideoCapture(video_path)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if replace_existing and exists(path_nfo):
                self.make_nfo_file(path_nfo, title=title, duration=length * 24, width=width, height=height,
                                   runtime=length * 24)
            elif not exists(path_nfo):
                self.make_nfo_file(path_nfo, title=title, duration=length * 24, width=width, height=height,
                                   runtime=length * 24)



    def generate_fanart(self):
        for idy, z in enumerate(self.subfolders):
            vid = self.get_video_file(z)
            video_path = z + "/" + vid
            path_nfo = z + "/" + os.path.splitext(vid)[0]
            cap = cv2.VideoCapture(video_path)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            num_images = self.num_rows_fan * self.num_col_fan
            x = 24*60*3 #sekunden die übersprungen werden
            interval = round((length-x)/num_images)
            images = []
            for idx in range(num_images):
                fanart = path_nfo + "-fanart" + str(idx + 1) + ".jpg"
                if not os.path.exists(fanart) or not os.path.exists(path_nfo + "-fanart.jpg"):
                    cap.set(1, x)
                    ret, frame = cap.read()
                    if idx == randrange(1, num_images):
                        cv2.imwrite(str(path_nfo + "-fanart.jpg"), frame)
                    cv2.imwrite(fanart, frame)
                    x = x + interval
                    images.append(frame)
            cap.release()
            cv2.destroyAllWindows()

            clearart_path = path_nfo + "-clearart.jpg"
            if not os.path.exists(clearart_path):
                hori = []
                row_count =0
                try:
                    for i in range(self.num_rows_fan * self.num_col_fan):
                        if (i% self.num_col_fan) == 0 and i == 0:
                            k = []
                            m = 0
                            for j in range(self.num_col_fan):
                                k.append(images[m])
                                m = m+1
                            try:
                                hori.append(np.concatenate((k), axis = 1))
                            except:
                                pass
                            row_count = row_count + self.num_col_fan
                        if (i% self.num_col_fan) == 0 and i > 0:
                            k = []
                            m = 0
                            for j in range(self.num_col_fan):
                                k.append(images[i+m])
                                m=m+1
                            hori.append(np.concatenate((k), axis = 1))
                            row_count = row_count + self.num_col_fan
                    Vertical_attachment =np.vstack(hori)
                    filename_thumbnail = str(clearart_path)
                    cv2.imwrite(filename_thumbnail,Vertical_attachment)
                except:
                    print(f"Failed for file {clearart_path}")
            print(f"Fanart Progress: {round(idy / len(self.subfolders) * 100, 1)} %")


    def get_actor_list(self):
        """ get all the actors from the folder"""
        actors_img = [f for f in listdir(self.actor_path) if isfile(join(self.actor_path, f))]
        return [Path(i).resolve().stem for i in actors_img]


    def get_actor(self, file_name):
        actor_found = []
        word_list = [words.lower() for words in re.split(r"[-._\s]\s*", file_name)]

        for i in self.actor_list:
            if ' ' in i: # double name
                if i.split(" ")[0].lower() in word_list and i.split(" ")[0].lower() in word_list:
                    actor_found.append(i)

            else: # no double name
                if i.lower() in word_list:
                    actor_found.append(i)

        if not actor_found:
            print(f"No actor found. {file_name}")
        return actor_found


    def overwrite_clearart(self):
        for idy, z in enumerate(self.subfolders):
            vid = self.get_video_file(z)
            path_nfo = z + "/" + os.path.splitext(vid)[0]
            from_file = path_nfo + "-clearart.jpg"
            to_file = path_nfo + "-fanart.jpg"
            shutil.copy(from_file, to_file)
            print("Progress: ", str(round(idy / len(self.subfolders) * 100, 1)), "%")


    def overwrite_fanart(self): #make fanart.jpg from fanart1-4.jpg
        for idy, z in enumerate(self.subfolders):
            vid = self.get_video_file(z)
            path_nfo = z + "/" + os.path.splitext(vid)[0]
            from_file = path_nfo + "-fanart" + str(randrange(1, 4,1)) + ".jpg"
            to_file = path_nfo + "-fanart.jpg"
            shutil.copy(from_file, to_file)
            print("Progress: ", str(round(idy / len(self.subfolders) * 100, 1)), "%")
