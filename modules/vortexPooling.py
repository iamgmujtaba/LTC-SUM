from keras.models import Sequential
from keras.layers import Conv2D, AveragePooling2D, Dropout, BatchNormalization, concatenate, UpSampling2D

def vortex_pooling(input_x):
    
    layer_1 = Sequential([AveragePooling2D(pool_size=(1, 1), strides=1, padding='valid'),
                         Conv2D(128, kernel_size=1, strides=1, padding='valid', dilation_rate = (1,1)),
                         UpSampling2D(size=(1,1), interpolation='bilinear'),
                         BatchNormalization(axis=-1)
                        ]) (input_x)
    
    layer_2 = Sequential([Conv2D(128, kernel_size=3, strides=1, padding='same', dilation_rate = (1,1)),
                         BatchNormalization(axis=-1)
                        ]) (input_x)
    
    layer_3 = Sequential([AveragePooling2D(pool_size=(1, 1), strides=1, padding='same'),
                         Conv2D(128, kernel_size=3, strides=1, padding='same', dilation_rate = (1,1)),
                         BatchNormalization(axis=-1)
                        ]) (input_x)
    
    layer_4 = Sequential([AveragePooling2D(pool_size=(1, 1), strides=1, padding='same'),
                         Conv2D(128, kernel_size=3, strides=1, padding='same', dilation_rate = (1,1)),
                         BatchNormalization(axis=-1)
                        ]) (input_x)

    layer_5 = Sequential([AveragePooling2D(pool_size=(1, 1), strides=1, padding='same'),
                         Conv2D(128, kernel_size=3, strides=1, padding='same', dilation_rate = (1,1)),
                         BatchNormalization(axis=-1)
                        ]) (input_x)
    
    layer_6 = Sequential([Conv2D(128, kernel_size=3, strides=1, padding='same', dilation_rate = (1,1)),
                        BatchNormalization(axis=3),
                        Dropout(rate=0.2)
                        ]) (input_x)
    
    # Concate
    concat = concatenate([layer_1, layer_2, layer_3, layer_4, layer_5, layer_6], axis=-1) 
    out = UpSampling2D(size=(1,1), interpolation='bilinear') (concat)
    return out