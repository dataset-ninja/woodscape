The authors of the **RGB Fisheye** part of a larger **WoodScape** dataset introduce a comprehensive fisheye automotive dataset, designed to facilitate detailed evaluations of computer vision algorithms on fisheye images. This dataset includes four surround-view cameras and addresses nine tasks, including segmentation, depth estimation, 3D bounding box detection, and soiling detection. It offers semantic annotation for over 10,000 images and annotations for other tasks for over 100,000 images. The dataset encourages the community to develop vision algorithms natively on fisheye images, avoiding naive rectification.

<img src="https://github.com/dataset-ninja/woodscape/assets/78355358/ef19e74e-4173-40a0-b82a-7906e0e10c38" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">The full dataset contains four cameras covering 360° accompanied by a HD laser  canner, IMU and GNSS. Annotations are made available for nine tasks, notably 3D object detection, depth estimation (overlaid on front camera) and semantic segmentation as illustrated here.</span>

Fisheye lenses, known for their non-linear mapping and large field of view, introduce radial distortion but are valuable for applications like automotive low-speed maneuvering. The term "fisheye" was coined by Robert Wood in 1906, who invented the fisheye camera. As a homage to Wood, the dataset is named WoodScape.

The high-level goals of the dataset include promoting the development of vision algorithms on fisheye images without undistortion, providing data for multi-camera scenarios, and facilitating multi-task learning for autonomous driving vision tasks. WoodScape originates from three geographical locations, including the USA, Europe, and China, and involves various driving scenarios and sensor configurations. The dataset includes RGB fisheye cameras, a LiDAR, GNSS/IMU systems, and odometry signals.

<img src="https://github.com/dataset-ninja/woodscape/assets/78355358/d52e0870-a1f3-4fe3-a172-5fa2465b8ed0" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Sample images from the surround-view camera network showing wide field of view and 360° coverage.</span>

WoodScape provides labels for multiple autonomous driving tasks, such as semantic segmentation, monocular depth estimation, object detection, visual odometry, visual SLAM, motion segmentation, soiling detection, and end-to-end driving. The dataset is compared with other popular datasets in terms of properties, highlighting its uniqueness and extensive task coverage.

## Dataset Acquisition

The dataset has the diverse origin of data, intrinsic and extrinsic calibrations, and quality checks. The dataset offers images at a resolution of 1MPx with 24-bit depth, and videos that are uncompressed, running at 30 frames per second, with lengths varying from 30 to 120 seconds. Additionally, the dataset includes synthetic data created using precise models of the actual cameras, which allows for the exploration of extra tasks. 

The camera is equipped with a High Dynamic Range (HDR) sensor that operates on a rolling shutter principle and boasts a dynamic range of 120 decibels. It comes with several features such as black level adjustment, automatic exposure control, automatic gain control, compensation for lens shading (also known as optical vignetting), gamma correction, and automatic white balance for color correction. 

The sensors recorded for this dataset are listed below:
* 4x 1MPx RGB fisheye cameras (190◦ horizontal FOV)
* 1x LiDAR rotating at 20Hz (Velodyne HDL-64E)
* 1x GNSS/IMU (NovAtel Propak6 & SPAN-IGM-A1)
* 1x GNSS Positioning with SPS (Garmin 18x)
* Odometry signals from the vehicle bus. 
WoodScape supports multiple recognition tasks with labels for forty classes.

## Dataset Design

Dataset design is considered a complex task, and the authors highlight the importance of careful consistency checks and database splitting for training, model selection, and testing. A sampling strategy aims to create a minimal consistent subset of the training set for efficiency. Data splitting and class balancing strategies are also detailed, providing control over each class's representation within splits. The dataset supports hypothesis evaluation through multiple splits and addresses potential class imbalance issues for specific tasks. The ratio between *train*, validation, and *test* splits is 6:1:3. <i>Please note, that the validation set was not excplicitly provided by the authors.</i>
