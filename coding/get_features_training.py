# coding: utf-8

# In[1]:


import cv2
import random
import numpy as np
from os import walk
import os
# In[2]:
class GetFeaturesTrainingInFiles :

    p = ""
    path = "../training_data/input/images/" + p
    path_output = "../training_data/input/features" + p 
    path_write_file = "training_features_data.txt" 
    
    windows_size_rows = 0
    windows_size_cols = 0
    
    kernel = np.ones((7, 7), np.int8)
    
    samples_contour = []
    samples_inner = []
    samples_outer = []

    def __init__(self, path):
        self.p = path
        self.path = "../training_data/input/images/" + path +"/"
        self.path_output = "../training_data/input/features/" + path + "/" 
        self.path_write_file = "training_features_data.txt" 
        
        ### kernel for prepare morphological
        self.kernel = np.ones((7, 7), np.int8)

        ### set windows size
        self.windows_size_rows = 31
        self.windows_size_cols = 31

        ### array samples
        # label_samples = []
        # feature_samples = []
        self.samples_contour = []
        self.samples_inner = []
        self.samples_outer = []
       

    def path(self):
        return self.path

    def path_output(self):
        return self.path_output


    # In[3]:


    def get_image_RGB(self, name):
        img_rgb = cv2.imread(name)
        b, g, r = cv2.split(img_rgb)
        return cv2.merge([r, g, b])


    # In[4]:


    def half_windows_size(self, windows_size_rows, windows_size_cols):
        return int(windows_size_rows / 2 + 1), int(windows_size_cols / 2 + 1)


    # In[5]:


    def get_pixels(self, img, i, windows_size_rows, windows_size_cols):
        rows, cols = i
        str = ""
        half_windows_size_rows, half_windows_size_cols = self.half_windows_size(windows_size_rows, windows_size_cols)
        # print("[{:d}, {:d}], ".format(rows, cols))
        features = ""
        for r in range(windows_size_rows):
            current_row = rows + r - half_windows_size_rows
            str += "{:2d} ".format(r + 1)
            for c in range(windows_size_cols):
                current_col = cols + c - half_windows_size_cols
                color_r, color_g, color_b = img[current_row, current_col]
                features += "{:3d} {:3d} {:3d} ".format(color_r, color_g, color_b)
                str += "[{:3d}, {:3d}, {:3d}], ".format(color_r, color_g,
                                                        color_b)  # str += "[{:3d}, {:3d}], ".format(c1, r1)
                # str += "[{:3d}, {:3d}], ".format(current_row, current_col)
            str += "\n"
        # print(str)
        # print(">>>>>>>>>>>>>>>>")
        return features


    # In[6]:


    def process_image_contour(self, img_gray):
        contour_img = np.ndarray(img_gray.shape, np.uint8)
        _, contours, hier = cv2.findContours(img_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contour_lengths = [len(c) for c in contours]
        max_length_index = np.argmax(contour_lengths)

        contour_img.fill(0)
        cv2.drawContours(contour_img, contours, -1, (255, 255, 255), 1)
        # cv2.imwrite(mask_folder + "/" + "f2_contour.png", contour_img)
        return contour_img


    # In[7]:


    def process_image_inner(self, img_gray):
        img_erosion = cv2.erode(img_gray, self.kernel, iterations=1)
        img_dilation = cv2.dilate(img_gray, self.kernel, iterations=1)

        img_dilation = self.swap_color(img_dilation)

        # cv2.imwrite(mask_folder + "/" + "f2_erosion.png", img_erosion)
        # cv2.imwrite(mask_folder + "/" + "f2_dilation.png", img_dilation)

        return img_erosion, img_dilation


    # In[8]:


    def swap_color(self, img_dilation):
        rows, cols = img_dilation.shape
        for row in range(rows):
            for col in range(cols):
                if img_dilation[row, col] == 0:
                    img_dilation[row, col] = 255
                elif img_dilation[row, col] == 255:
                    img_dilation[row, col] = 0
        return img_dilation


    # In[9]:


    def random_pixel_target(self, pixel_target_list, size_pixel_img_contour):
        random.shuffle(pixel_target_list)
        new_pixel_target_list = []

        for a in range(size_pixel_img_contour):
            new_pixel_target_list.append(pixel_target_list[a])
            # print(new_pixel_target_list[a])

        return new_pixel_target_list


    # In[10]:


    def is_pixel_target(self, pixel):
        return pixel == 255


    # In[11]:


    def get_pixels_target(self, img):
        rows, cols = img.shape
        half_windows_size_rows, half_windows_size_cols = self.half_windows_size(self.windows_size_rows,self. windows_size_cols)
        pixel_target_list = []
        for row in range(rows):
            for col in range(cols):
                if (self.is_pixel_target(img[row, col])):
                    if half_windows_size_rows <= row & row <= rows - half_windows_size_rows:
                        if half_windows_size_rows <= col & col <= cols - half_windows_size_cols:
                            pixel_target_list.append([row, col])

        return pixel_target_list


    # In[12]:


    def get_sample_contour(self, label, features, pixel_target):
        self.samples_contour.append(self.get_sample(label, features, pixel_target))


    def get_sample_inner(self, label, features, pixel_target):
        self.samples_inner.append(self.get_sample(label, features, pixel_target))


    def get_sample_outer(self, label, features, pixel_target):
        self.samples_outer.append(self.get_sample(label, features, pixel_target))


    def get_sample(self, label, features, pixel_target):
        return "|label " + label + " |coordinate " + "{:d} {:d} ".format(pixel_target[0], pixel_target[1]) + "|features " + features + "\n"

    def clear_file(self, path_write_file_features):
        file_label = open(path_write_file_features, 'w')
    
    def shuffle_samples(self, array):
        return random.shuffle(array)

    def write_samples(self, path_write_file_lable, path_write_file_features):
        self.clear_file(path_write_file_features)
        file = open(path_write_file_features, 'a')
        
        self.shuffle_samples(self.samples_contour)
        self.shuffle_samples(self.samples_inner)
        self.shuffle_samples(self.samples_outer)
        
        for index in range(len(self.samples_contour)):
            file.write(self.samples_contour[index])
            file.write(self.samples_inner[index])
            file.write(self.samples_outer[index])
           
            # file_label = open(path_write_file_lable, 'a')
            # file_features = open(path_write_file_features, 'a')

            # shuffle_samples(label_samples)
            # shuffle_samples(feature_samples)

            # for sample in label_samples :
            #     file_label.write(sample)
            #
            # for sample in feature_samples :
            #     file_features.write(sample)


    def get_features_contour(self, img_rgb, pixel_target_list, windows_size_rows, windows_size_cols, label):
        for pixel_target in pixel_target_list:
            self.get_sample_contour(label, self.get_pixels(img_rgb, pixel_target, windows_size_rows, windows_size_cols), pixel_target)
#         print("contour size -> " + str(len(self.samples_contour)))
        return len(pixel_target_list)


    # In[15]:


    def get_features_inner(self, img_rgb, pixel_target_list, windows_size_rows, windows_size_cols, label, size_pixel_img_contour):
        pixel_target_list = self.random_pixel_target(pixel_target_list, size_pixel_img_contour)
        for pixel_target in pixel_target_list:
            self.get_sample_inner(label, self.get_pixels(img_rgb, pixel_target, windows_size_rows, windows_size_cols), pixel_target)
#         print("inner size -> " + str(len(self.samples_inner)))


    # In[16]:


    def get_features_outer(self, img_rgb, pixel_target_list, windows_size_rows, windows_size_cols, label, size_pixel_img_contour):
        pixel_target_list = self.random_pixel_target(pixel_target_list, size_pixel_img_contour)

        for pixel_target in pixel_target_list:
            self.get_sample_outer(label, self.get_pixels(img_rgb, pixel_target, windows_size_rows, windows_size_cols), pixel_target)
#         print("outer size -> " + str(len(self.samples_outer)))


    # In[17]:


    def process_get_sample(self, img_rgb, img_gray, windows_size_rows, windwos_size_cols, path_write_file_lable, path_write_file_features):
        img_erosion, img_dilation = self.process_image_inner(img_gray)
        size_pixel_img_contour = self.get_features_contour(img_rgb, self.get_pixels_target(self.process_image_contour(img_gray)), windows_size_rows, windwos_size_cols, "0 0 1")
        self.get_features_inner(img_rgb, self.get_pixels_target(img_erosion), windows_size_rows, windwos_size_cols, "0 1 0", size_pixel_img_contour)
        self.get_features_outer(img_rgb, self.get_pixels_target(img_dilation), windows_size_rows, windwos_size_cols, "1 0 0", size_pixel_img_contour)
        print("contour size -> " + str(len(self.samples_contour)) +", inner size -> " + str(len(self.samples_inner)) + ", outer size -> " + str(len(self.samples_outer)))
        self.write_samples(path_write_file_lable, path_write_file_features)


    # In[18]:


    def process_read_image(self, filename_rgb, filename_gray, filename):
        print("start => " + self.path+filename_rgb)
#         print(self.path+filename_rgb)
        img_rgb = self.get_image_RGB(self.path + filename_rgb)
        
        img_gray = cv2.imread(self.path + filename_gray, cv2.IMREAD_GRAYSCALE)
        self.process_get_sample(img_rgb, img_gray, self.windows_size_rows, self.windows_size_cols, self.path + "traning_data_label_" + filename + ".txt",self.path_output + "training_features_data_" + filename + ".txt")
        print("finished " +self.path_output + "training_features_data" + filename + ".txt"+ "\n>>>>>>>>>>")


    # In[19]:


    def extract_filename(self, current_filename):
        return current_filename.split('.')


    def is_file_image(self, filename, filetype):
        if ((filename.find('_') == -1) & ((filetype == "png") | (filetype == "jpg"))):
            return True
        return False


    # In[20]:


    def initialize_samples(self,):
        self.samples_contour = []
        self.samples_inner = []
        self.samples_outer = []


    # In[ ]:

    def process(self) :
        if not os.path.exists(self.path_output):
            os.makedirs(self.path_output)
        filenames = []
        for (dirpath, dirnames, filename) in walk(self.path):
            filenames.extend(filename)

        # In[ ]:


        for current_filename in filenames:
            filename, filetype = self.extract_filename(current_filename)
            if self.is_file_image(filename, filetype):
                self.initialize_samples()
                img_gray = filename + "_gray." + filetype
                self.process_read_image(current_filename, img_gray, filename)
        
        print("finsihed get features from image to files")

