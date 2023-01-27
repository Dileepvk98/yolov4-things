import json 
import os
import shutil
import argparse
from zipfile import ZipFile

from rename_fix import rename
from train_test_split import train_test_split

parser = argparse.ArgumentParser(description='convert coco format dataset to yolo v4/v3 format')
parser.add_argument('--out_dir', type=str, required=False, default='custom_data', help='name of output zipfile')
parser.add_argument('--coco_json', type=str, required=True, help='json file name of coco dataset')
parser.add_argument('--train_f', type=str, required=False, default='train.txt', help='file containg path of img for trainig')
parser.add_argument('--test_f', type=str, required=False, default='test.txt', help='file containg path of img for testing')
parser.add_argument('--bkup_dir', type=str, required=False, default='saved_weights', help='dir name to save weights during training and resume')
parser.add_argument('--img_fmt', type=str, required=False, default=".jpg", help='.jpg, .jpeg, .png, .bmp')
args = parser.parse_args()

OUTPUT_DIR = args.out_dir
COCO_JSON_PATH = args.coco_json
TRAIN_FILE_PATH = args.train_f
TEST_FILE_PATH = args.test_f
BKUP_PATH = args.bkup_dir
# img_formats = ['.jpg', '.jpeg', '.png', '.bmp']
img_format = args.img_fmt

if os.path.exists(OUTPUT_DIR):
    if len(os.listdir(OUTPUT_DIR)) > 0:
        ow = input('directory already exists! Overwrite (y/N) : ')
        if ow !='y':
            print('exiting...')
            exit()
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)
else:
    os.mkdir(OUTPUT_DIR)
        
with open(COCO_JSON_PATH, 'r') as coco_f:
    data = json.load(coco_f)
    print('no. of images : ', len(data['images']))
    print('no. of annotations: ', len(data['annotations']))

img_id_path_map = {i["id"] : (i["path"], i["file_name"])  for i in data["images"]}
# print(img_id_path_map)
min_cat_id = min([c["id"] for c in data["categories"]])
print('min_cat_id :',min_cat_id)

cat_id_map = {c['name'] : c['id']-min_cat_id for c in data["categories"]}
print(cat_id_map)
categories = list(cat_id_map.keys())
# print(categories)
skipped = 0
total = 0

# convert 
    # coco format  of  bbox = xmin, ymin, w, h
    # to
    # yolov4 format of bbox = xcenter, ycenter, w, h
for a in data['annotations']:
    path = img_id_path_map[a["image_id"]][0]
    img_fn = img_id_path_map[a["image_id"]][1]
    category_id = a["category_id"]-min_cat_id
    bbox = a['bbox']
    w, h = a['width'], a['height']
    try:
        if not os.path.exists(os.path.join(OUTPUT_DIR, img_fn)):
            shutil.copyfile(path, os.path.join(OUTPUT_DIR, img_fn))
            with open(OUTPUT_DIR+'/'+img_fn.replace(img_format,".txt"), 'a') as f:
                xc, yc = (bbox[0]+bbox[2]/2)/w, (bbox[1]+bbox[3]/2)/h
                f.write(str(category_id)+" "+str(xc)+" "+str(yc)+" "+str(bbox[2]/w)+" "+str(bbox[3]/h)+"\n")
                total+=1
    except Exception as e:
        print(e)
        skipped+=1
 
# create config files 
with open(OUTPUT_DIR+'.names', 'w') as f:
    f.writelines(c+'\n' for c in categories)

with open(OUTPUT_DIR+'.data', 'w') as f:
    f.write('classes = '+str(len(categories))+'\n')
    f.write('train = '+TRAIN_FILE_PATH+'\n')
    f.write('test = '+TEST_FILE_PATH+'\n')
    f.write('names = '+OUTPUT_DIR+'.names\n')
    f.write('backup = '+BKUP_PATH+'\n')

print('\ntotal converted : ',total)
print('skipped due to error : ',skipped)

# fixing filenames
try:rename(OUTPUT_DIR, img_format)
except Exception as e:print('error :',e)

# splitting into train and test set 
try:split = train_test_split(int(input('enter test data% [0-100] : ')), OUTPUT_DIR, img_format, TRAIN_FILE_PATH, TEST_FILE_PATH)
except Exception as e:print('error : ',e);split = False

print('creating zip file...')
if os.path.exists(OUTPUT_DIR+'.zip'):
    os.remove(OUTPUT_DIR+'.zip')
    print('deleted existing '+OUTPUT_DIR+'.zip')

# shutil.make_archive(OUTPUT_DIR+'.zip', 'zip', OUTPUT_DIR)
with ZipFile(OUTPUT_DIR+'.zip', 'w') as zipObj:
    for folderName, subfolders, filenames in os.walk(OUTPUT_DIR):
       for filename in filenames:
           filePath = os.path.join(folderName, filename)
           zipObj.write(OUTPUT_DIR)
           zipObj.write(os.path.join(OUTPUT_DIR, filename), os.path.join(OUTPUT_DIR,os.path.basename(filePath)))
           
    zipObj.write(OUTPUT_DIR+'.data')
    zipObj.write(OUTPUT_DIR+'.names')
    if split:
        zipObj.write(TRAIN_FILE_PATH)
        zipObj.write(TEST_FILE_PATH)
    else:print('train, text.txt not found')
        
print('deleting excess files...')        
os.remove(TRAIN_FILE_PATH)
os.remove(TEST_FILE_PATH)
os.remove(OUTPUT_DIR+'.names')
os.remove(OUTPUT_DIR+'.data')
shutil.rmtree(OUTPUT_DIR)

print('done')