
import tensorflow as tf
import numpy as np
import _pickle as pickle


def fetch_mnist():
    """returns 28x28 images of handwritten digits 0-9."""
    return tf.keras.datasets.mnist


def dataset_1():
    "1 - Training Data only train data from mnist"
    (x, y), (x_test, y_test) = fetch_mnist().load_data()
    x = np.array(x).reshape(-1, 28, 28, 1)

    pickle_out = open("Traindata_x-1", "wb")
    pickle.dump(x, pickle_out)
    pickle_out.close()

    pickle_out = open("Traindata_y-1", "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()


def dataset_2():
    "2 - Training Data of combined train and test data from mnist"
    (x_train, y_train), (x_test, y_test) = fetch_mnist().load_data()

    x1 = []
    y1 = []

    for i in x_train:
        x1.append(i)
    for i in x_test:
        x1.append(i)
    for i in y_train:
        y1.append(i)
    for i in y_test:
        y1.append(i)

    x1 = np.array(x1).reshape(-1, 28, 28, 1)
    y1 = np.array(y1)

    pickle_out = open("Traindata_x-2", "wb")
    pickle.dump(x1, pickle_out)
    pickle_out.close()

    pickle_out = open("Traindata_y-2", "wb")
    pickle.dump(y1, pickle_out)
    pickle_out.close()


def add(image, label):
    "Add more data to 2nd dataset for more accurate prediction"

    pickle_in = open("Traindata_x-2", "rb")
    x = pickle.load(pickle_in)

    pickle_in = open("Traindata_y-2", "rb")
    y = pickle.load(pickle_in)

    x = np.array(x).reshape(-1, 28, 28)

    x1 = []
    y1 = []

    for i in x:
        x1.append(i)
    for i in y:
        y1.append(i)

    try:
        x1.insert(0, image)
        y1.insert(0, label)
    except:
        pass

    x1 = np.array(x1).reshape(-1, 28, 28, 1)
    y1 = np.array(y1)

    pickle_out = open("Traindata_x-2", "wb")
    pickle.dump(x1, pickle_out)
    pickle_out.close()

    pickle_out = open("Traindata_y-2", "wb")
    pickle.dump(y1, pickle_out)
    pickle_out.close()


#  =======================================================  #

if __name__ == "__main__":
    dataset_1()
    dataset_2()
