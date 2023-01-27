import os


dir_name = 'custom_data'

files = os.listdir(dir_name)
img_files = sorted([file for file in files if file.endswith('.jpg')], key=lambda x:int(x.split('.')[0]))
# txt_files = sorted([file for file in files if file.endswith('.txt')], key=lambda x:int(x.split('.')[0]))

for i,file in enumerate(img_files):
# for i,file in enumerate(txt_files):
    file_int = int(file.split('.')[0])
    if i != file_int:
        print('renaming : ', file.split('.')[0], "->", i)
        os.rename(os.path.join(dir_name, str(file_int)+'.jpg'), os.path.join(dir_name, str(i)+'.jpg'))
        os.rename(os.path.join(dir_name, str(file_int)+'.txt'), os.path.join(dir_name, str(i)+'.txt'))

