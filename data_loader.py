import numpy as np
import scipy.misc
import imageio
import cv2
import csv

class DataLoader():
    def __init__(self, dataset_name, img_res=96):
        self.dataset_name = dataset_name
        self.img_res = img_res
        self.paths = []
        self.values = []

    def load_batch(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "val"

        with open(self.dataset_name + "/" + data_type + ".csv", "r") as file:
            self.paths=[]
            self.values = []
            file.seek(0)

            reader = csv.reader(file, delimiter=",")
            for index, row in enumerate(reader):
                for i, r in enumerate(row[1:7]):
                    row[i + 1] = int(r)

                path, value = row

                self.values.append(value)
                self.paths.append(path)
        self.values = np.array(self.values)
        self.n_batches = int(len(self.paths) / batch_size)

        for idx in range(self.n_batches - 1):
            batch_paths = self.paths[idx * batch_size:(idx + 1) * batch_size]
            values = self.values[idx * batch_size:(idx + 1) * batch_size]

            imgs = []
            v = []
            for img_path in batch_paths:
                img = self.imread(img_path)
                #img = scipy.misc.imresize(img, (224, 224))
                imgs.append(img)
            """
            for value in values:
                value_ohe = self.one_hot_encode(value,num_classes=2)
                self.values.append(value_ohe)
            """
            for value in values:
                value_ohe = self.one_hot_encode(value,num_classes=4)
                v.append(value_ohe)

            imgs = np.array(imgs) / 127.5 - 1.
            values_n = np.array(v)
            #values.reshape(4)

            yield imgs, values_n

    def load_data(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "val"

        with open(self.dataset_name + "/" + data_type + ".csv", "r") as file:
            self.paths = []
            self.values = []
            file.seek(0)

            reader = csv.reader(file, delimiter=",")
            for index, row in enumerate(reader):
                for i, r in enumerate(row[1:2]):
                    row[i + 1] = int(r)

                path, value = row
                self.values.append(value)
                self.paths.append(path)

        indices = (len(self.values)*np.random.rand(batch_size)).astype(int)
        values = self.values[indices]

        v = []
        imgs = []
        for idx in indices:
            img = self.imread(self.paths[idx])
            imgs.append(img)
        imgs = np.array(imgs) / 127.5 - 1.

        return imgs, values

    def imread(self, path):
        return scipy.misc.imread(path).astype(np.float)

    def one_hot_encode(self, y, num_classes=0):
        return np.squeeze(np.eye(num_classes)[y.reshape(-1)])