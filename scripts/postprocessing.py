"""
Post-processing on the output data of Faster R-CNN 
"""
from src.api_request import get_pano_location
from src.geometry import pixel_to_viewpoint

import csv
import numpy as np
import glob
import os

PANO_WIDTH = 2000 # We used the "panorama_2000" images in Faster R-CNN
NUM_WORKERS = 6
INPUT_FOLDER = "data/faster_r-cnn_output/"
OUTPUT_FOLDER = "data/postprocessing_output/"

def process_csv(input_file):
    """
    Iterate over the input CSV and get: 
    - Camera location information
    - Viewpoint of the camera to the detected object (in degrees)
    """
    rows_list = []
    with open(input_file) as f:
        csv_reader = csv.reader(f, delimiter=",")
        next(f)  # skip the first line
        for row in csv_reader:
            if len(row) < 2:
                print("Broken entry ignored")
                continue
            if len(row) < 3:
                pano_id, center_bbox = row[0], float(row[1])
            else:
                print("Broken entry ignored")
                continue

            location = get_pano_location(pano_id)
            viewpoint_to_object = pixel_to_viewpoint(center_bbox, PANO_WIDTH)

            rows_list.append((location[0], location[1], round(viewpoint_to_object, 2)))

    output_file = OUTPUT_FOLDER + os.path.basename(input_file)
    if os.path.isfile(OUTPUT_FILE):
        print("A file with the specified ouput name already exists.")

    # Save the list of float values
    np.savetxt(output_file, rows_list, delimiter=",", newline="\n", fmt="%s",
        comments="", header="x,y,viewpoint")

def main():
    input_files = glob.glob(INPUT_FOLDER + "*.csv")
    if len(input_files) < 1:
        print("No input file(s) found. Aborting.")
        return

    if len(input_files) == 1:
        process_csv(input_files[0])
    else:
        # Use multiprocessing if two or more input files are found
        import multiprocessing

        p = multiprocessing.Pool(processes = NUM_WORKERS)
        p.map_async(process_csv, input_files)

        p.close()
        p.join()

if __name__ == "__main__":
    main()