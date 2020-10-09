# Object Detection and Geospatial Localization from Panoramic Images
In this repository, an approach is implemented to automatically detect and geolocate public objects, solely based on publicly available panoramic images. The objects of interest are assumed to be stationary, compact and observable from several locations each. In this project the objects being detected are bicycle symbols. The implementation consists of two main parts:
1. Bicycle symbol detection in panoramic images using Faster R-CNN, a state-of-the-art object detection algorithm.
2. A refactored Python implementation of the MRF-based triangulation procedure to estimate object geolocations, introduced in "Automatic Discovery and Geotagging of Objects from Street View Imagery" by V. A. Krylov, E. Kenny, R. Dahyot.


---

### Project Folder Structure

This project contains six folders, one `README.md`, one `requirements.txt` and one file entitled `main.py`. The Python file ([`main.py`](main.py)) runs the second part of this project to geolocate objects. In this structure we have a `data` folder and an `output` folder to physically separate the inputs and outputs:

1.  [`data`](./data): Folder for raw, unprocessed data
2.  [`output`](./output): Folder for the output data

There are four other folders in the structure:

3. [`src`](./src): Folder for all source files specific to this project
4. [`examples`](./examples): Folder for example code and visualizations
5. [`models`](./models): Folder for the Faster R-CNN implementation
6. [`scripts`](./scripts): Folder for the helper files


---

## Pipeline
#### Faster R-CNN object detection
A pre-trained Faster R-CNN model is further fine-tuned on a dataset of panoramic images with annotated bicycle symbols. Along with the Faster R-CNN output of the predicted bicycle symbols, additional information is essential for the next step of the pipeline. This is performed by utilizing ([`./scripts/postprocessing.py`](./scripts/postprocessing.py)).

![](https://github.com/Amsterdam-AI-Team/Geolocalization/blob/master/examples/faster_r-cnn.gif)

#### Geolocate objects 
Each line in the input CSV file (i.e. output of previous pipeline step) defines a detected object by four values of type float: camera location RD-coordinates (X, Y), viewpoints in degrees towards the object in the panoramic image and the depth estimate. The latter may be omitted or set to zero. A sample input file is provided in the [`data`](./data) folder.

The output CSV file contains a list of RD-coordinates (X, Y) of identified objects of interests and a score value for each of these. The score is the number of individual views contributing to an object (for each of the discovered objects this value is greater or equal than 2).

The system was evaluated on a [`dataset`](https://api.data.amsterdam.nl/panorama/panoramas/?bbox=109400.00,494450.00,136550.00,474000.00&page=1&srid=28992&tags=mission-2019%2Csurface-land) of 667.690 panoramic images captured in 2019. The estimated location data of bicycle symbols in Amsterdam can be found here: ([`./output/bicycle_symbol_locations_2019.csv`](./output/bicycle_symbol_locations_2019.csv)).

---

## Examples
To visualize the viewpoint directions of one panoramic image, use:

    usage: visualize_viewpoints.py [-b] [--bbox] [-p --pano_id]
    example: python3 -m examples.visualize_viewpoints -b "440,607,530,653" -p "TMX7316010203-001542_pano_0000_000191"

To visualize the viewpoint directions and possible object intersections of multiple panoramic images, use:

    usage: visualize_intersections.py [-c] [--csv_file]
    example: python3 -m examples.visualize_intersections -c "data/faster_r-cnn_output/bicycle_symbols.csv"


---

## Demo 
The satellite view below shows an estimated location of a bicycle symbol.
![](https://github.com/Amsterdam-AI-Team/Geolocalization/blob/master/examples/satellite_zoom.gif)


---
