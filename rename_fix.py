import os
import argparse

def rename(dir_name, img_fmt):
    files = os.listdir(dir_name)
    img_files = sorted([file for file in files if file.endswith(img_fmt)], key=lambda x:int(x.split('.')[0]))
    # txt_files = sorted([file for file in files if file.endswith('.txt')], key=lambda x:int(x.split('.')[0]))

    total = 0
    for i,file in enumerate(img_files):
    # for i,file in enumerate(txt_files):
        file_int = int(file.split('.')[0])
        if i != file_int:
            print('renaming : ', file.split('.')[0], "->", i)
            os.rename(os.path.join(dir_name, str(file_int)+img_fmt), os.path.join(dir_name, str(i)+img_fmt))
            os.rename(os.path.join(dir_name, str(file_int)+'.txt'), os.path.join(dir_name, str(i)+'.txt'))
            total+=1

    print('total renamed : ',total)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, required=False, default='custom_data')
    parser.add_argument('--img_fmt', type=str, required=False, default=".jpg")
    args = parser.parse_args()
    rename(dir_name=args.out, img_fmt=args.img_fmt)

