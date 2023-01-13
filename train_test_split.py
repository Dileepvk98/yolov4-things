import os
import random

split_perc = 0.1
files = os.listdir('toy_human/')
img_files = sorted([file for file in files if file.endswith('.jpg')], key=lambda x:int(x.split('.')[0]))
test_files_idx = random.sample(range(0, len(img_files)),int(split_perc*len(img_files)))
# print(img_files)
# print(test_files_idx)
# print(len(img_files))
with open('test.txt', 'w') as test_f:
    with open('train.txt', 'w') as train_f:
        for i, f in enumerate(img_files):
            if i in test_files_idx:
                test_f.write('../toy_human/'+f+'\n')
            else:
                train_f.write('../toy_human/'+f+'\n')