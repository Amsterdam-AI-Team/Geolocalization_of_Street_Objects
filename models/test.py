# Some basic setup
# Import some common libraries
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import cv2
from PIL import Image
import numpy as np
import zipfile
import pandas as pd
import os

# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
# Import some common detectron2 utilities
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor

def draw_bbox(myfile, bboxes, filename):
    """
    Plot bbox in original image
    """
    # Create figure and axes
    fig,ax = plt.subplots(figsize=(10, 10))
    plt.axis('off')

    for box in bboxes:
        # Create a Rectangle patch
        x0, y0, x1, y1 = box
        width = x1 - x0
        height = y1 - y0

        rect = mpl.patches.Rectangle((x0, y0), width, height, linewidth=1,
            edgecolor='r', facecolor='none')

        # Add the patch to the Axes
        ax.add_patch(rect)

    # Read image in grayscale mode
    original_img = np.array(Image.fromarray(cv2.imread(myfile, cv2.IMREAD_GRAYSCALE)))
    # Display the image
    ax.imshow(original_img, cmap = plt.cm.gray)

    fig.savefig(f"output_images/{filename}.png", dpi=200, bbox_inches='tight', pad_inches=0)


def non_max_suppression(boxes, probs=None, overlap_thresh=0.3):
    """
    This is a Python version used to implement the Soft NMS algorithm.
    Original Paper：Soft-NMS--Improving Object Detection With One Line of Code
    """
    # If there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # If the bounding boxes are integers, convert them to floats -- this
    # Is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # Initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Compute the area of the bounding boxes and grab the indexes to sort
    # (in the case that no probabilities are provided, simply sort on the
    # bottom-left y-coordinate)
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = y2

    # If probabilities are provided, sort on them instead
    if probs is not None:
        idxs = probs

    # Sort the indexes
    idxs = np.argsort(idxs)

    # Keep looping while some indexes still remain in the indexes list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the index value
        # to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of the bounding
        # box and the smallest (x, y) coordinates for the end of the bounding
        # box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have overlap greater
        # than the provided overlap threshold
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked
    return boxes[pick].astype("float")

def main():
    """
    An example script on how to iterate over the images in a zip file 
    and get predictions from Faster R-CNN. 
    """

    cfg = get_cfg()
    cfg.merge_from_file(
        "detectron2/configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
    )
    cfg.OUTPUT_DIR = "model_output"
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model.pth")
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1 # Bicycle symbol
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.99

    predictor = DefaultPredictor(cfg)

    # An example on how to use zipfile
    zip_file = zipfile.ZipFile("datasets/panoramas/2019/row3/124300.0,487000.0,125500.0,483000.0.zip")

    rows_list = []
    for name in zip_file.namelist():
        if name.endswith('.jpg'):
            filename = name.split("/")[-1].split(".jpg")[0]

            # Open the images with the openCV reader because BGR order is used in Detectron2
            pic = zip_file.read(name)
            im = cv2.imdecode(np.frombuffer(pic, np.uint8), 1)

            all_instances = outputs['instances'].to('cpu')
            boxes = all_instances.pred_boxes.tensor.numpy()
            #scores = all_instances.scores.numpy()

            # Use Soft-NMS
            #bboxes_window = non_max_suppression(boxes, scores, 0.2)

            for i in range(len(boxes)):
                center_temp = (boxes[i][0] + boxes[i][2]) / 2

                # Save detection row by row
                new_data = {'pano_id' : filename, 'center_bbox' : center_temp}
                rows_list.append(new_data)

            # bboxes rounded to 1 decimal
            #rounded_bboxes = [[np.round(float(i), 1) for i in nested] for nested in boxes]

            # Draw predictions
            #draw_bbox(myfile, rounded_bboxes, filename)

    # Save this file
    df_output = pd.DataFrame(rows_list)
    compression_opts = dict(method='zip', archive_name='bicycle_symbols.csv')
    df_output.to_csv('bicycle_symbols.zip', index=False, compression=compression_opts)

if __name__ == "__main__":
    main()
