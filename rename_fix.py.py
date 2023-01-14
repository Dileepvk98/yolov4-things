import os

files = os.listdir('toy_human/')
# files = os.listdir('yolo_data/')
img_files = sorted([file for file in files if file.endswith('.jpg')], key=lambda x:int(x.split('.')[0]))
# txt_files = sorted([file for file in files if file.endswith('.txt')], key=lambda x:int(x.split('.')[0]))

for i,file in enumerate(img_files):
# for i,file in enumerate(txt_files):
    print(i, file)
    file_int = int(file.split('.')[0])
    if i != file_int:
        print('renaming..')
        os.rename('toy_human/'+str(file_int)+'.jpg', 'toy_human/'+str(i)+'.jpg')
        os.rename('toy_human/'+str(file_int)+'.txt', 'toy_human/'+str(i)+'.txt')

