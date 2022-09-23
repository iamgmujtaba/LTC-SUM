import os
import csv
import re
from urllib.request import urlopen
import requests


####################################################################
####################################################################
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',str(text)) ]

####################################################################
####################################################################
# download csv from walter for specifc movie
def get_container_csv(movie_url, dest_path):
    file_name = movie_url.split('/')[-1]

    u = urlopen(movie_url)
    f = open(os.path.join(dest_path,file_name), 'wb')
    resp = requests.get(movie_url)
    
    file_size = int(resp.headers['content-length'])

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)

####################################################################
# download container images from walter fro the specific movie
def containers_to_download(cont_list_csv, movie_path):
    with open(os.path.join(movie_path,cont_list_csv)) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            row_count = sum(1 for row in readCSV)
            print("Images to download: %s"%(row_count+1))

def download_containers(movie_thumb_url,movie_path, thumb_dest_dir):
    cont_list_csv = 'container_list.csv'
    containers_to_download(cont_list_csv, movie_path)

    with open(os.path.join(movie_path,cont_list_csv)) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            try:
                t_url = movie_thumb_url+str(row).strip('[]').strip("'")
                file_name = t_url.split('/')[-1]

                u = urlopen(t_url)
                f = open(os.path.join(thumb_dest_dir,file_name), 'wb')
                resp = requests.get(t_url)
                
                file_size = int(resp.headers['content-length'])
            
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                    status = status + chr(8)*(len(status)+1)
                f.close()
            except:
                pass
    print("Download complted: ", thumb_dest_dir)

####################################################################
def segments_to_download(segment_csv, detect_thumbnail_csv):
    data_segment = []
    count = 0
    cur_line_seg = 0
    with open(detect_thumbnail_csv, newline='') as f_left:
        reader_left = csv.reader(f_left, delimiter=',')
        with open(detect_thumbnail_csv, newline='') as f_right:
            reader_right = csv.reader(f_right, delimiter=',')
            for row in reader_left:
                for compare_row in reader_right:
                    try:
                        row = next(reader_left)
                        cur_line = str(" ".join(compare_row)).strip('[]').strip("'")
                        cur_line_name = cur_line.split('_')
                        cur_line_frame = int(cur_line_name[1]) * 25 + int(cur_line_name[2].split(".")[0])
                        cur_line_seg = int(cur_line_frame/10)

                        nex_line = str(row).strip('[]').strip("'")
                        nex_line_name = nex_line.split('_')
                        nex_line_frame = int(nex_line_name[1]) * 25 + int(nex_line_name[2].split(".")[0])
                        nex_line_seg = int(nex_line_frame/10)

                        if cur_line_seg != nex_line_seg:
                            segment_name = "out"+ '{:02}'.format(cur_line_seg)+".ts"
                            data_segment.append([segment_name]) 
                            count += 1
                    except:
                        segment_name = "out"+ '{:02}'.format(cur_line_seg)+".ts"
                        data_segment.append([segment_name])
                        count += 1
                        break
                    
                f_right.seek(0)

    with open(segment_csv, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_segment)
        fout.close()
    
    return count

def download_segments(movie_url, segment_csv, segments_dest):
    try: 
        f = open(segment_csv, "r+")
        reader = csv.reader(f)
        pre_line = next(reader)
        x = 10
        while(True) and x >0:
            try:
                cur_line = next(reader)
                if pre_line != cur_line:
                    
                    segment_name = str(pre_line).strip('[]').strip("'")
                    seg_url = os.path.join(movie_url, segment_name)

                    print('downloading segment: ', seg_url)
                    
                    u = urlopen(seg_url)
                    f = open(os.path.join(segments_dest,segment_name), 'wb')
                    resp = requests.get(seg_url)

                    file_size = int(resp.headers['content-length'])
                
                    file_size_dl = 0
                    block_sz = 8192
                    while True:
                        buffer = u.read(block_sz)
                        if not buffer:
                            break

                        file_size_dl += len(buffer)
                        f.write(buffer)
                        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                        status = status + chr(8)*(len(status)+1)
                pre_line = cur_line
                x -=1
            except :
                break
    except:
        pass

