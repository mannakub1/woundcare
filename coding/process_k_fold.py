
# coding: utf-8

# In[1]:


import os

class SegmentationFile :

    samples = []
    path, k, directory_name= ["", "", ""]
    len_samples = 0
    file_balance_samples = ""

    def __init__(self, path, k):
        self.directory_name = path
        self.k = k

        self.len_samples = 0
        self.samples = []
        self.file_balance_samples = ""
    # In[2]:

    
    def get_samples(self) :
        while True :
            current_sample = self.file_balance_samples.readline()
            if not current_sample :
                break
            self.samples.append(current_sample)


    # In[3]:


    def create_directory(self, name_directory) :
        if not os.path.exists(name_directory):
            os.makedirs(name_directory)


    # In[4]:


    def clear_file(self, path_file) :
        file = open(path_file, 'w')
        file.write("")


    # In[5]:


    def write_file(self, number, start, last) :
        file_name = self.path+number+"/"

        self.clear_file(file_name+"test"+".txt")
        self.clear_file(file_name+"train"+".txt")

        file_test = open(file_name+"test"+".txt", 'a')
        print(start)
        print(last)
        for i in range(start, last) :
            file_test.write(self.samples[i])

        file_train = open(file_name+"train"+".txt", 'a')
        for i in range(1, start) :
            file_train.write(self.samples[i])
        for i in range(last, self.len_samples) :
            file_train.write(self.samples[i])


    # In[6]:


    def processed(self, k) :
        before_i = 1
        size_k_samples = int(self.len_samples / k)
        for i in range(k) :
            self.create_directory(self.path+"{:d}".format(i+1))
            if not (i+1) == k :
                current_last_sample = (i+1) * size_k_samples
                self.write_file("{:d}".format(i+1), before_i, current_last_sample+1)
            else :
                current_last_sample = self.len_samples
                self.write_file("{:d}".format(i+1), before_i, current_last_sample)
            before_i = current_last_sample+1



    # In[7]:

    def process(self):
        self.path = self.directory_name + "/"


        self.file_balance_samples = open("../training_data/input/features/training_featureds_balance.txt", 'r')

        self.samples = []
        self.get_samples()
        self.len_samples = len(self.samples)
        
        print("size of samples => " + str(self.len_samples))

        ### process k flod
        self.processed(int(self.k))

