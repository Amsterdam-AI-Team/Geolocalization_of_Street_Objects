import datetime
import json
import os
import os.path

from PIL import Image

def main(input_dir, out_dir, im_dir):
    created = datetime.datetime.today().strftime("%Y/%m/%d")
    out_dic = {
                "info":{
                    "description" : "BicycleSymbols",
                    "date_created" : created
                },
                "images" : [],
                "categories": [{
                    "supercategory": "bicycle",
                    "id": 0,
                    "name": "bicycle"
                }],
                "annotations" : []
              }
    
    all_list = os.listdir(input_dir)
    l_list = [f for f in all_list if ".txt" in f]
    
    an_idx = 0

    for im_idx, label in enumerate(l_list):
        file_name = os.path.splitext(label)[0] + ".jpg"

        # Not necesarry for this dataset, all images are same dimensions
        im = Image.open(os.path.join(im_dir, file_name))
        width = im.width
        height = im.height
        
        image = dict(
            id = im_idx,
            width = width,
            height = height,
            file_name = file_name
        )
        out_dic["images"].append(image)

        with open(os.path.join(input_dir,label), mode = 'r')as f:
            anno_list = f.readlines()
            
            test = 0
            for anno in anno_list:
                #print(test)
                test = test + 1
                anno = anno.strip().split()
                
                for i in range(1, 5):
                    anno[i] = float(anno[i])
                
                # "class x y w h"
                # x, y: the upper-left coordinates of the bounding box
                # width, height: the dimensions of your bounding box
                x = anno[1]
                y = anno[2]
                w = anno[3] - anno[1]
                h = anno[4] - anno[2]
                
                cls = anno[0]

                annotation = dict(
                    id = an_idx,
                    category_id = int(cls),
                    image_id = im_idx,
                    bbox = [x, y, w, h],
                    area = w * h,
                    iscrowd = 0
                )
                out_dic["annotations"].append(annotation)
                an_idx += 1

    with open(out_dir, mode="w")as f:
        # dump = json.dumps(out_dic)
        # print(type(dump))
        json.dump(out_dic, f, indent=2)
    
    print(f"{an_idx+1} annotations created for {im_idx} images.")

if __name__ == "__main__":
    # TODO add argparse
    input_dir = "all_labels_yolo"
    out_dir = "all.json"
    im_dir = "all/"

    main(input_dir, out_dir, im_dir)