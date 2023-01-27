import json 
import os
import shutil
 
OUTPUT_DIR = 'custom_data'
COCO_JSON_PATH = 'toy_human_coco.json'
# INPUT_IMG_DIR = 'toy_human'

TRAIN_FILE_PATH = 'train.txt'
TEST_FILE_PATH = 'test.txt'
BKUP_PATH = '/saved_weights'

# img_formats = ['.jpg', '.jpeg', '.png', '.bmp']
img_format = ".jpg"

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

for a in data['annotations']:
    path = img_id_path_map[a["image_id"]][0]
    img_fn = img_id_path_map[a["image_id"]][1]
    category_id = a["category_id"]-min_cat_id
    # coco format of bbox - xmin, ymin, w, h
    bbox = a['bbox']
    w, h = a['width'], a['height']
           
    try:
        if not os.path.exists(os.path.join(OUTPUT_DIR, img_fn)):
            shutil.copyfile(path, os.path.join(OUTPUT_DIR, img_fn))
            with open(OUTPUT_DIR+'/'+img_fn.replace(img_format,".txt"), 'a') as f:
                # yolov4 format of bbox = xcenter, ycenter, w, h
                xc, yc = (bbox[0]+bbox[2]/2)/w, (bbox[1]+bbox[3]/2)/h
                f.write(str(category_id)+" "+str(xc)+" "+str(yc)+" "+str(bbox[2]/w)+" "+str(bbox[3]/h)+"\n")
                total+=1
    except Exception as e:
        print(e)
        skipped+=1
 
with open('custom_data.names', 'w') as f:
    f.writelines(c+'\n' for c in categories)

with open('custom_data.data', 'w') as f:
    f.write('classes = '+str(len(categories))+'\n')
    f.write('train = '+TRAIN_FILE_PATH+'\n')
    f.write('test = '+TEST_FILE_PATH+'\n')
    f.write('names = custom_data.names\n')
    f.write('backup = '+BKUP_PATH+'\n')

print('\ntotal converted : ',total)
print('skipped due to error : ',skipped)
print('\nrun rename_fix.py if file names are not continuos [optional]')
print('run train_test_split.py to generate train and test files')