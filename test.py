import efficientnet.keras as efn
from keras.models import load_model
import numpy as np

import os
import time
import csv
import operator 

from utils.UCFdata import UCFDataSet
from utils.lib_createDir import prepare_walter_dirs
from utils.lib_hls import get_container_csv, download_containers, segments_to_download, download_segments, natural_keys
from utils.lib_thumbnails import extract_thumbnails, process_image
from modules.SGDW import SGDW

from config import parse_opts

ucf_data = UCFDataSet()

config = parse_opts()
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]= config.device

model_path ='./output/037-0.96.hdf5'
model = load_model(model_path, custom_objects={'SGDW': SGDW})

ac01 = '' 
wt09 = '18_Vengeance_Valley_1951'
fb01 = ''
cr01 = ''

event_01 = 0
event_02 = 0
event_03 = 0

segment_event_01 = 0
segment_event_02 = 0
segment_event_03 = 0

if (config.genre == 'wt'):
    movies = [wt09]
    pref_01 = 'Rid_Race'
    pref_02 = 'Arc_Pun'
    pref_03 = 'Rid_Race_Arc_Pun'
elif (config.genre == 'ac'):
    movies = [ac01]
    pref_01 = 'Arc_Pun'
    pref_02 = 'Tai_Nun'
    pref_03 = 'Arc_Pun_Tai_Nun'
elif (config.genre == 'fb'):
    movies = [fb01]
    pref_01 = 'Jug'
    pref_02 = 'Pen'
    pref_03 = 'Jug_Pen'
elif (config.genre == 'cr'):
    movies = [cr01]
    pref_01 = 'Bow'
    pref_02 = 'Shot'
    pref_03 = 'Bow_Shot'

####################################################################
def event_recognition():
    global event_01
    global event_02
    global event_03

    data_event_01 = []
    data_event_02 = []
    data_event_03 = []
    
    for fileName in os.listdir(config.thumbnail_dir):
        # Turn the image into an array.
        image_arr = process_image(os.path.join(config.thumbnail_dir,fileName), (config.spatial_size, config.spatial_size, 3))
        image_arr = np.expand_dims(image_arr, axis=0)
       
        # Predict.
        predictions = model.predict([image_arr])

        label_predictions = {}
        for i, label in enumerate(ucf_data.classes):
            label_predictions[label] = predictions[0][i]

        sorted_lps = sorted(label_predictions.items(), key=operator.itemgetter(1), reverse=True)
        
        for i, class_prediction in enumerate(sorted_lps):
            i += 1

            if (config.genre == 'wt'): # western movies
                if  str(class_prediction[0])== str('HorseRiding') or str(class_prediction[0])== str('HorseRace'):
                    if float(class_prediction[1]) >= 0.95:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_01.append([fileName])
                        event_01 +=1

                if  str(class_prediction[0])== str('Archery') or str(class_prediction[0])== str('Punch'):
                    if float(class_prediction[1]) >= 0.95:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_02.append([fileName])
                        event_02 +=1

                if  str(class_prediction[0])== str('HorseRiding') or str(class_prediction[0])== str('HorseRace') or str(class_prediction[0])== str('Archery') or str(class_prediction[0])== str('Punch'):
                    if float(class_prediction[1]) >= 0.95:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_03.append([fileName])
                        event_03 +=1

            elif (config.genre == 'ac'):# action movies
                if  str(class_prediction[0])== str('Archery') or str(class_prediction[0])== str('Punch'):
                    if float(class_prediction[1]) >= 0.65:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_01.append([fileName])
                        event_01 +=1

                if  str(class_prediction[0])== str('TaiChi') or str(class_prediction[0])== str('Nunchucks'):
                    if float(class_prediction[1]) >= 0.65:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_02.append([fileName])
                        event_02 +=1

                if  str(class_prediction[0])== str('Archery') or str(class_prediction[0])== str('Punch') or str(class_prediction[0])== str('TaiChi') or str(class_prediction[0])== str('Nunchucks'):
                    if float(class_prediction[1]) >= 0.65:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_03.append([fileName])
                        event_03 +=1

            elif (config.genre == 'fb'): # football movies
                if  str(class_prediction[0])== str('SoccerJuggling'):
                    if float(class_prediction[1]) >= 0.90:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_01.append([fileName])
                        event_01 +=1

                if  str(class_prediction[0])== str('SoccerPenalty'):
                    if float(class_prediction[1]) >= 0.90:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_02.append([fileName])
                        event_02 +=1

                if  str(class_prediction[0])== str('SoccerJuggling') or str(class_prediction[0])== str('SoccerPenalty'):
                    if float(class_prediction[1]) >= 0.90:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_03.append([fileName])
                        event_03 +=1

            elif (config.genre == 'cr'): # cricket movies
                if  str(class_prediction[0])== str('CricketBowling'):
                    if float(class_prediction[1]) >= 0.80:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_01.append([fileName])
                        event_01 +=1

                if  str(class_prediction[0])== str('CricketShot'):
                    if float(class_prediction[1]) >= 0.80:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_02.append([fileName])
                        event_02 +=1

                if  str(class_prediction[0])== str('CricketBowling') or str(class_prediction[0])== str('CricketShot'):
                    if float(class_prediction[1]) >= 0.80:     
                        print(os.path.join(config.thumbnail_dir,fileName),': '+ "%s: %.2f" % (class_prediction[0], class_prediction[1]))
                        data_event_03.append([fileName])
                        event_03 +=1

    with open(os.path.join(config.movie_path, 'detect_thumbs_' + pref_01 + '.csv'), 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(data_event_01, key=natural_keys))


    with open(os.path.join(config.movie_path, 'detect_thumbs_' + pref_02 + '.csv'), 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(data_event_02, key=natural_keys))
        

    with open(os.path.join(config.movie_path, 'detect_thumbs_' + pref_03 + '.csv'), 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(data_event_03, key=natural_keys))


def seg_download():
    global segment_event_01
    global segment_event_02
    global segment_event_03

    segments_csv_list = os.path.join(config.movie_path,'segments_list_'+ pref_01 +'.csv')
    detect_thumbnail_csv = os.path.join(config.movie_path,'detect_thumbs_'+ pref_01 +'.csv')
    if event_01 > 0:
        segment_event_01 = segments_to_download(segments_csv_list, detect_thumbnail_csv)
        # if segment_event_01 > 0:
        download_segments(movie_url +'segments/', segments_csv_list, os.path.join(config.segments_dir, pref_01))


    segments_csv_list2 = os.path.join(config.movie_path,'segments_list_'+ pref_02 +'.csv')
    detect_thumbnail_csv2 = os.path.join(config.movie_path,'detect_thumbs_'+ pref_02 +'.csv')
    if event_02 > 0:
        segment_event_02 = segments_to_download(segments_csv_list2, detect_thumbnail_csv2)
        # if segment_event_02 > 0:
        download_segments(movie_url +'segments/', segments_csv_list2, os.path.join(config.segments_dir, pref_02))


    segments_csv_list3 = os.path.join(config.movie_path,'segments_list_'+ pref_03 +'.csv')
    detect_thumbnail_csv3 = os.path.join(config.movie_path,'detect_thumbs_'+ pref_03 +'.csv')
    
    if event_03 > 0:
        segment_event_03 =  (segments_csv_list3, detect_thumbnail_csv3)
        # if segment_event_03 > 0:
        download_segments(movie_url +'segments/', segments_csv_list3, os.path.join(config.segments_dir, pref_03))


def ts_to_mp4(segment_path):
    if event_01 > 0:
        cat_command_1 = ('cat ' + segment_path +'/' + pref_01 +'/out*.ts > '+ segment_path +'/' + pref_01 + '/combine.ts')
        ffm_command_1 = 'ffmpeg -i '+ segment_path +'/' + pref_01 +'/combine.ts -acodec copy -vcodec copy '+ segment_path +'/' + pref_01 + '/summary.mp4'
        os.system(cat_command_1)
        os.system(ffm_command_1)

    if event_02 > 0:
        cat_command_2 = ('cat ' + segment_path +'/' + pref_02 +'/out*.ts > '+ segment_path +'/' + pref_02 + '/combine.ts')
        ffm_command_2 = 'ffmpeg -i '+ segment_path +'/' + pref_02 +'/combine.ts -acodec copy -vcodec copy '+ segment_path +'/' + pref_02 + '/summary.mp4'
        os.system(cat_command_2)
        os.system(ffm_command_2)

    if event_03 > 0:
        cat_command_3 = ('cat ' + segment_path +'/' + pref_03 +'/out*.ts > '+ segment_path +'/' + pref_03 + '/combine.ts')
        ffm_command_3 = 'ffmpeg -i '+ segment_path +'/' + pref_03 +'/combine.ts -acodec copy -vcodec copy '+ segment_path +'/' + pref_03 + '/summary.mp4'
        os.system(cat_command_3)
        os.system(ffm_command_3)

####################################################################
def main(movie_dir):
    text_file = open(os.path.join(movie_dir,'processing_time.txt'), "w")
    text_file.write(movie_dir)
    text_file.write('\n')
    
    start1 = time.time()
    get_container_csv(containers_csv_url, config.movie_path)
    download_containers(containers_url,config.movie_path, config.container_dir)
    end1 = time.time()
    t1 = round(end1 - start1, 2)
    text_file.write('Download  TC sec: ' + str(t1) + '     mint: ' + str(round(t1/60,2)) )
    text_file.write('\n')
    
    start2 = time.time()
    extract_thumbnails(config.container_dir, config.thumbnail_dir)
    end2 = time.time()
    t2 = round(end2 - start2, 2)
    text_file.write('Extract   T  sec: ' + str(t2) + '     mint: ' + str(round(t2/60,2)) )
    text_file.write('\n')

    start3 = time.time()
    event_recognition()
    end3 = time.time()
    t3 = round(end3 - start3, 2)
    text_file.write('Recognize E  sec: ' + str(t3) + '   mint: ' + str(round(t3/60,2)) )
    text_file.write('\n')

    start4 = time.time()
    seg_download()
    end4 = time.time()
    t4 = round(end4 - start4, 2)
    text_file.write('Download  S  sec: ' + str(t4) + '     mint: ' + str(round(t4/60,2)) )
    text_file.write('\n')

    start5 = time.time()
    ts_to_mp4(config.segments_dir)
    end5 = time.time()
    t5 = round(end5 - start5, 2)
    text_file.write('Aggregate S  sec: ' + str(t5) + '     mint: ' + str(round(t5/60,2)) )
    text_file.write('\n')
    sum_t = t1 + t2 + t3 + t4 + t5
    text_file.write('Sum          sec: ' + str(round(sum_t,2)) + '   mint: ' + str(round(sum_t/60,2)))
    text_file.write('\n')
    text_file.write('\n')

    text_file.write('Pref 01 detect thumbnails : '+ str(event_01) + '   download segments :' + str(segment_event_01))
    text_file.write('\n')
    text_file.write('Pref 02 detect thumbnails : '+ str(event_02) + '   download segments :' + str(segment_event_02))
    text_file.write('\n')
    text_file.write('Pref 03 detect thumbnails : '+ str(event_03) + '  download segments :' + str(segment_event_03))
    text_file.close()

####################################################################
if __name__ == "__main__":
    count = 0

    while count < len(movies):
        print('-'*80)
        print('-'*80)
        print(count, ':',movies [count])

        if count > 0:
            config = parse_opts()
        #Create director for movie
        config = prepare_walter_dirs(config, movies [count])

        containers_csv_url = os.path.join(config.walter_ip, movies [count], 'container_list.csv')   
        containers_url = os.path.join(config.walter_ip,movies [count],'thumbnails/')
        movie_url = os.path.join(config.walter_ip, movies [count])

        try: 
            os.mkdir(os.path.join(config.segments_dir, pref_01))
            os.mkdir(os.path.join(config.segments_dir, pref_02))
            os.mkdir(os.path.join(config.segments_dir, pref_03))
        except OSError as error: 
            print('path already exists: ', error) 
        
        main(config.movie_path)
        count += 1    

