import os
import random
import argparse

def train_test_split(split_perc, dir_name, img_format, trainf, testf):
    split_perc/=100
    files = os.listdir(dir_name)
    img_files = sorted([file for file in files if file.endswith(img_format)], key=lambda x:int(x.split('.')[0]))
    test_files_idx = random.sample(range(0, len(img_files)),int(split_perc*len(img_files)))
    # print(img_files)
    # print(test_files_idx)
    # print(len(img_files))
    with open(testf, 'w') as test_f:
        with open(trainf, 'w') as train_f:
            for i, f in enumerate(img_files):
                if i in test_files_idx:
                    test_f.write(os.path.join(dir_name,f)+'\n')
                else:
                    train_f.write(os.path.join(dir_name,f)+'\n')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, required=False, default='custom_data')
    parser.add_argument('--train_f', type=str, required=False, default='train.txt')
    parser.add_argument('--test_f', type=str, required=False, default='test.txt')
    parser.add_argument('--img_fmt', type=str, required=False, default=".jpg")
    args = parser.parse_args()
    _ = train_test_split(split_perc = int(input('enter test data% [0-100] : ')), dir_name=args.out, img_format=args.img_fmt, trainf=args.train_f, testf=args.test_f)