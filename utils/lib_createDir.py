import json as simplejson
import os
import time
import shutil
####################################################################
####################################################################
def print_config(config):
    print('#'*60)
    print('Training configuration:')
    for k,v  in vars(config).items():
        print('  {:>20} {}'.format(k, v))
    print('#'*60)

def write_config(config, json_path):
    with open(json_path, 'w') as f:
        f.write(simplejson.dumps(vars(config), indent=4, sort_keys=True))

def output_subdir(config):
    prefix = time.strftime("%Y_%m_%d_%H%M")
    subdir = "{}_{}_{}".format(prefix, config.dataset, config.model)
    return os.path.join(config.save_dir, subdir)

def prepare_output_dirs(config):
    # Set output directories
    config.save_dir = output_subdir(config)
    config.checkpoint_dir = os.path.join(config.save_dir, 'checkpoints')
    config.log_dir = os.path.join(config.save_dir, 'logs')

    # And create them
    if os.path.exists(config.save_dir):
        # Only occurs when experiment started the same minute
        shutil.rmtree(config.save_dir)

    os.mkdir(config.save_dir)
    os.mkdir(config.checkpoint_dir)
    os.mkdir(config.log_dir)
    return config

####################################################################
####################################################################
# create directory for hls server files to download
def output_walter_subdir(config, movie_id):
    prefix = time.strftime("%Y_%m_%d") 
    subdir = "{}_{}".format(prefix, movie_id)
    return os.path.join(config.movie_path, subdir)

def prepare_walter_dirs(config, movie_id):
    # Set output directories
    config.movie_path = output_walter_subdir(config, movie_id)
    config.container_dir = os.path.join(config.movie_path, 'container')
    config.segments_dir = os.path.join(config.movie_path, 'segments')
    config.thumbnail_dir = os.path.join(config.movie_path, 'thumbnail')
    
    try:
        if not os.path.exists(config.movie_path):
            os.mkdir(config.movie_path)
            os.mkdir(config.container_dir)
            os.mkdir(config.segments_dir)
            os.mkdir(config.thumbnail_dir)
    except OSError as error: 
            print('path already exists: ', error)
    
    return config
