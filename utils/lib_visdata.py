import matplotlib.pyplot as plt
import itertools
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import seaborn as sns


def data_disribution(df_attr, save_dir):
    plt.title('Female or Male')
    sns.countplot(y='Male', data=df_attr, color="r")

    plt.savefig(save_dir, format='png')

def visualize_dataAug(sample_image, save_dir):
    datagen =  ImageDataGenerator(
                shear_range=0.2,
                zoom_range=0.2,
                rotation_range=30.,
                width_shift_range=0.2,
                height_shift_range=0.2,
                horizontal_flip=True)

    # load one image and reshape
    img = load_img(sample_image)
    x = img_to_array(img)/255.
    x = x.reshape((1,) + x.shape)

    # plot 10 augmented images of the loaded iamge
    plt.figure(figsize=(20,10))
    plt.suptitle('Data Augmentation', fontsize=28)

    i = 0
    for batch in datagen.flow(x, batch_size=1):
        plt.subplot(3, 5, i+1)
        plt.grid(False)
        plt.imshow( batch.reshape(218, 178, 3))
        
        if i == 9:
            break
        i += 1
    
    plt.savefig(save_dir, format='png', bbox_inches='tight')



# Plot and save keras trainning history
def save_history(hist, save_dir, lw = 3):
    plt.figure(figsize=(10,10))

    plt.subplot(2,1,1)
    plt.plot(hist.history['acc'], label='training', marker = '*', linewidth = lw)
    plt.plot(hist.history['val_acc'], label='validation', marker = 'o', linewidth = lw)
    plt.title('Accuracy Comparison')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.grid(True)
    plt.legend(fontsize = 'x-large')

    plt.subplot(2,1,2)
    plt.plot(hist.history['loss'], label='training', marker = '*', linewidth = lw)
    plt.plot(hist.history['val_loss'], label='validation', marker = 'o', linewidth = lw)
    plt.title('Loss Comparison')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.legend(fontsize = 'x-large')

    plt.tight_layout()
    plt.savefig(save_dir, format='png', bbox_inches='tight')

####################################################################
####################################################################
def plot_confusion_matrix(save_dir,cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.figure(figsize=(10,10))

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(save_dir, format='png', bbox_inches='tight')
    