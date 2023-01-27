import json 
 
with open('toy_human_coco.json', 'r') as coco_f:
    data = json.load(coco_f)
print(len(data['images']), len(data['annotations']))

img_id_path_map = {i["id"] : i["path"] for i in data["images"]}
# print(img_id_path_map)

min_cat_id = min([c["id"] for c in data["categories"]])
print('min_cat_id :',min_cat_id)

cat_id_map = {c['name'] : c['id'] for c in data["categories"]}
print(cat_id_map)
# categories = list(cat_id_map.keys())
# print(categories)

for a in data['annotations']:
    path = img_id_path_map[a["image_id"]]
    category_id = a["category_id"]-min_cat_id
    
    # coco format of bbox - xmin, ymin, w, h
    bbox = a['bbox']
    w, h = a['width'], a['height']
    
    # print(path.split('/')[-1].replace(".jpg",""))    
    with open('yolo_data/'+path.split('/')[-1].replace(".jpg","")+".txt", 'a') as f:
        # yolov4 format of bbox = xcenter, ycenter, w, h
        xc = (bbox[0]+bbox[2]/2)/w
        yc = (bbox[1]+bbox[3]/2)/h
        f.write(str(category_id)+" "+str(xc)+" "+str(yc)+" "+str(bbox[2]/w)+" "+str(bbox[3]/h)+"\n")
 