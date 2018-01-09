import numpy as np
import sys
import os
import math
import cntk

class TestingData :
    input_dim_model = (3, 31, 31)
    input_dim = 3 * 31 * 31
    num_output_classes = 3
    input = cntk.input_variable(input_dim_model)  # สังเกตว่าเราใช้ input_dim_model เป็นพารามิเตอร์แทนการใช้ input_dim
    label = cntk.input_variable(num_output_classes)


    def create_reader(self, path, is_training, input_dim, num_label_classes):
        labelStream = cntk.io.StreamDef(field='label', shape=num_label_classes, is_sparse=False)
        featureStream = cntk.io.StreamDef(field='features', shape=input_dim, is_sparse=False)

        deserailizer = cntk.io.CTFDeserializer(path, cntk.io.StreamDefs(labels=labelStream, features=featureStream))

        return cntk.io.MinibatchSource(deserailizer,
                                       randomize=is_training, max_sweeps=cntk.io.INFINITELY_REPEAT if is_training else 1)


    def number_of_line(self, path):
        file = open(path, 'r')
        f = []
        while True:
            line = file.readline();
            if not line:
                break
            f.append(line)
        return len(f)

    def get_label_from_testing_data(self, path):
        labels =[]
        file_test = open(path)
        while True :
            line = file_test.readline()
            if not line :
                break
            lines = line.split(" ")
            current_label = lines[1] + " " + lines[2] + " " + lines[3]
            labels.append(current_label)
        return labels

    def load(self, path_directory):
        arr = []

        path_file = "testing_features_data.txt"
        size_file = self.number_of_line(path_directory + path_file)
        labels = self.get_label_from_testing_data(path_directory + path_file)

        testing_file = os.path.join(path_directory, path_file)
        reader_test = self.create_reader(testing_file, False, self.input_dim, self.num_output_classes)
        test_input_map = {
            self.input: reader_test.streams.features,
            self.label: reader_test.streams.labels
        }
        data = reader_test.next_minibatch(size_file, input_map=test_input_map)
        data_asarray = data[self.input].asarray()

        for i in range(0, size_file):
            arr.append(np.reshape(data_asarray[i], (3, 31, 31)))


        return arr,labels, size_file