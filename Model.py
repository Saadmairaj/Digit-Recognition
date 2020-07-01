import tensorflow as tf
import numpy as np
import time
import _pickle as pickle

global graph1, model
model = tf.keras.models.Sequential()
Graph1 = tf.get_default_graph()

# accuracy = 0

def Train_Digit():
    global model, Graph1 #, accuracy
    with Graph1.as_default():
        "Tain the model for digit recognition"

        Name = "Digit_Reader-28x28-{}".format( int(time.time()) )

        tensorboard = tf.keras.callbacks.TensorBoard( log_dir="log/{}".format(Name) )

        pickle_in = open("Traindata_x-2","rb")
        x = pickle.load(pickle_in)

        pickle_in = open("Traindata_y-2","rb")
        y = pickle.load(pickle_in)

        x = x / 255.0
        
        model.add( tf.keras.layers.Flatten(input_shape=x[0].shape) )
        model.add( tf.keras.layers.Dense(512, activation=tf.nn.relu) )
        model.add( tf.keras.layers.Dense(512, activation=tf.nn.relu) )
        model.add( tf.keras.layers.Dense( 10, activation=tf.nn.softmax ) )


        model.compile(  optimizer="adam",
                        loss="sparse_categorical_crossentropy",
                        metrics=["accuracy"]    )

        hist = model.fit ( x, y, epochs=3, 
                    batch_size=25, 
                    validation_split=0.3, 
                    # callbacks=[tensorboard] 
                    )
        
        accuracy = hist.history.get('acc')[-1]
        accuracy = float( (int(accuracy * 10000)) / 100 )

        model.save('Digit_Reader1.h5')

        return accuracy

if __name__ == "__main__":
    print(Train_Digit())