import os
import random

def train_test_split(split_perc, dir_name, img_format):
    files = os.listdir(dir_name)
    img_files = sorted([file for file in files if file.endswith(img_format)], key=lambda x:int(x.split('.')[0]))
    test_files_idx = random.sample(range(0, len(img_files)),int(split_perc*len(img_files)))
    # print(img_files)
    # print(test_files_idx)
    # print(len(img_files))
    with open('test.txt', 'w') as test_f:
        with open('train.txt', 'w') as train_f:
            for i, f in enumerate(img_files):
                if i in test_files_idx:
                    test_f.write(os.path.join(dir_name,f)+'\n')
                else:
                    train_f.write(os.path.join(dir_name,f)+'\n')


if __name__ == '__main__':
    train_test_split(split_perc = 0.15, dir_name='custom_data', img_format='.jpg')