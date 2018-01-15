
# coding: utf-8

# In[1]:

class BalanceSample :

    new_line = []

    name, root_path, root_path, path_write_file = ["","","",""]
    file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10, = ["","","","","","","","","",""]
    
    def __init__(self, path):
        self.new_line = []
        self.name = path
        self.root_path = "../training_data/input/features/"+ self.name + "/"
        self.path_write_file = "../training_data/input/features/training_featureds_balance.txt"
        
        print(self.root_path)
        
        filename = "training_features_data_"
        
        self.file_1 = open(self.root_path+filename + self.name +"1.txt", 'r')
        self.file_2 = open(self.root_path+filename + self.name +"2.txt", 'r')
        self.file_3 = open(self.root_path+filename + self.name +"3.txt", 'r')
        self.file_4 = open(self.root_path+filename + self.name +"4.txt", 'r')
        self.file_5 = open(self.root_path+filename + self.name +"5.txt", 'r')
        self.file_6 = open(self.root_path+filename + self.name +"6.txt", 'r')
        self.file_7 = open(self.root_path+filename + self.name +"7.txt", 'r')
        self.file_8 = open(self.root_path+filename + self.name +"8.txt", 'r')
        self.file_9 = open(self.root_path+filename + self.name +"9.txt", 'r')
        self.file_10 = open(self.root_path+filename + self.name +"10.txt", 'r')
       


    # In[2]:


    def get_lines(self,file, line_1, count) :
        self.new_line.append(line_1)
        while count < 2 :
            current_line = file.readline()
            count += 1
            if current_line :
                self.new_line.append(current_line)


    # In[3]:


    def guard_get_lines(self,file) :
        current_line = file.readline()
        if not current_line :
            return 1
        else :
            self.get_lines(file, current_line, 0)
            return 0


    # In[4]:


    def clear_file(self, path_write_file):
        file = open(path_write_file, 'w')


    # In[5]:

    def process(self):
        self.clear_file(self.path_write_file)

        while True:
            count = 0
            count += self.guard_get_lines(self.file_1)
            count += self.guard_get_lines(self.file_2)
            count += self.guard_get_lines(self.file_3)
            count += self.guard_get_lines(self.file_4)
            count += self.guard_get_lines(self.file_5)
            count += self.guard_get_lines(self.file_6)
            count += self.guard_get_lines(self.file_7)
            count += self.guard_get_lines(self.file_8)
            count += self.guard_get_lines(self.file_9)
            count += self.guard_get_lines(self.file_10)
            if count == 1:
                break

        file_ = open(self.path_write_file, 'a')

        for line in self.new_line :
            file_.write(line)

        print("finished process")

