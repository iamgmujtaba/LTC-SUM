from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard, CSVLogger, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator

import os

from config import parse_opts

from utils.UCFdata import UCFDataSet
from utils.lib_createDir import prepare_output_dirs, print_config, write_config
from utils.lib_visdata import save_history

from models.efficientNet import create_model

####################################################################
####################################################################
ucf13_data = UCFDataSet()

# Configuration and logging
config = parse_opts()
config = prepare_output_dirs(config)

print_config(config)
write_config(config, os.path.join(config.save_dir, 'config.json'))

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]= config.device

#Train and testing directories
rgb_train = os.path.join(config.dataset_path,'train/')
rgb_test = os.path.join(config.dataset_path,'test/')

# Helper: Save the model.
checkpointer = ModelCheckpoint(
    filepath=os.path.join(config.checkpoint_dir,'{epoch:03d}-{val_loss:.2f}.hdf5'),
    verbose=1,
    save_best_only=True)

# Helper: Save results.
csv_logger = CSVLogger(os.path.join(config.log_dir,'training.log'))

# Helper: Stop when we stop learning.
early_stopper = EarlyStopping(patience=config.early_stopping_patience)

# Helper: TensorBoard
tensorboard = TensorBoard(log_dir=config.log_dir)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

####################################################################
####################################################################

# With data augmentation to prevent overfitting       
def get_generators():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        horizontal_flip=True,
        rotation_range=10.,
        width_shift_range=0.2,
        height_shift_range=0.2)

    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        rgb_train,
        target_size=(config.spatial_size, config.spatial_size),
        color_mode = 'rgb',
        batch_size=config.batch_size,
        classes=ucf13_data.classes,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        rgb_test,
        target_size=(config.spatial_size, config.spatial_size),
        color_mode = 'rgb',
        batch_size=config.batch_size,
        classes=ucf13_data.classes,
        class_mode='categorical')

    return train_generator, validation_generator

####################################################################
####################################################################

if __name__ == "__main__":
    model = create_model(show_summary = True, img_size = config.spatial_size, num_classes = config.num_classes)
    print('\nModel created...\n')
    generators = get_generators()
    train_gen, validation_gen = generators

    hist = model.fit_generator(train_gen,
        steps_per_epoch= 100,
        validation_data= validation_gen,
        validation_steps= 10,
        epochs=config.num_epochs,
        callbacks=[checkpointer, early_stopper, tensorboard, csv_logger, reduce_lr])
    
    model.save(os.path.join(config.save_dir, 'final_model.h5'))

    save_history(hist, os.path.join(config.save_dir, 'evaluate.png'))

