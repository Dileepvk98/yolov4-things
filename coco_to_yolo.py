import json 
 
with open('toy_human_coco.json', 'r') as coco_f:
    data = json.load(coco_f)
 
print(len(data['images']), len(data['annotations']))
 
# yolo_f = open('toy_human_yolo.txt', 'w')
 
for i in range(len(data['images'])):
    path = data['images'][i]['path']
    category_id = data['images'][i]['category_ids'][0]
    
    # coco format of bbox - xmin, ymin, w, h
    bbox = data['annotations'][i]['bbox']
    w, h = data['annotations'][i]['width'], data['annotations'][i]['height']
    
    # print(path.split('/')[-1].replace(".jpg",""))
    
    with open('yolo_data/'+path.split('/')[-1].replace(".jpg","")+".txt", 'w') as f:
        # yolov4 format of bbox = xcenter, ycenter, w, h
        xc = (bbox[0]+bbox[2]/2)/w
        yc = (bbox[1]+bbox[3]/2)/h
        f.write(str(0)+" "+str(xc)+" "+str(yc)+" "+str(bbox[2]/w)+" "+str(bbox[3]/h)+"\n")
    
    # yolo_f.write(str(0)+" "+str(bbox[0]/w)+" "+str(bbox[1]/h)+" "+str(bbox[2]/w)+" "+str(bbox[3]/h)+"\n")
 