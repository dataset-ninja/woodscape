# https://github.com/valeoai/WoodScape

import os
import supervisely as sly
from supervisely.io.json import load_json_file
from supervisely.io.fs import get_file_name_with_ext, get_file_name, dir_exists, file_exists
import numpy as np
from cv2 import connectedComponents
from dotenv import load_dotenv

import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil

from tqdm import tqdm


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "WoodScape"

    train_images_path = "/home/grokhi/rawdata/woodscape/rgb_images"
    test_images_path = "/home/grokhi/rawdata/woodscape/rgb_images_test/rgb_images(test_set)"
    soiling_train_images_path = "/home/grokhi/rawdata/woodscape/soiling_data/train/rgbImages"
    soiling_test_images_path = "/home/grokhi/rawdata/woodscape/soiling_data/test/rgbImages"
    train_masks_path = "/home/grokhi/rawdata/woodscape/instance_annotations/instance_annotations"
    vehicle_info_pathes = "/home/grokhi/rawdata/woodscape/vehicle_info/vehicle_info/rgb_images"
    soiling_train_masks_path = "/home/grokhi/rawdata/woodscape/soiling_data/train/rgbLabels"
    soiling_test_masks_path = "/home/grokhi/rawdata/woodscape/soiling_data/test/rgbLabels"
    images_ext = ".png"
    anns_ext = ".json"
    soiling_folder = "rgbImages"
    masks_folder = "gtLabels"
    batch_size = 30

    classes_names = [
        "road_surface",
        "curb",
        "car",
        "train/tram",
        "truck",
        "other_wheeled_transport",
        "trailer",
        "van",
        "caravan",
        "bus",
        "bicycle",
        "motorcycle",
        "person",
        "rider",
        "grouped_botts_dots",
        "cats_eyes_and_botts_dots",
        "parking_marking",
        "lane_marking",
        "parking_line",
        "other_ground_marking",
        "zebra_crossing",
        "trafficsign_indistingushable",
        "sky",
        "fence",
        "traffic_light_yellow",
        "ego_vehicle",
        "pole",
        "structure",
        "traffic_sign",
        "animal",
        "free_space",
        "traffic_light_red",
        "unknown_traffic_light",
        "movable_object",
        "traffic_light_green",
        "void",
        "grouped_vehicles",
        "grouped_pedestrian_and_animals",
        "grouped_animals",
        "green_strip",
        "nature",
        "construction",
        "Other_NoSight",
    ]

    def create_ann(image_path):
        labels = []
        tags = []

        ann_name = get_file_name(image_path) + anns_ext

        if (
            image_path.split("/")[-2] == "rgb_images"
            or image_path.split("/")[-2] == "rgb_images(test_set)"
        ):
            ds_tag = sly.Tag(rgb_meta)
            tags.append(ds_tag)

            if masks_path is None:
                image_np = sly.imaging.image.read(image_path)[:, :, 0]
                img_height = image_np.shape[0]
                img_wight = image_np.shape[1]

                return sly.Annotation(
                    img_size=(img_height, img_wight), labels=labels, img_tags=tags
                )

            vehicle_info_path = os.path.join(vehicle_info_pathes, ann_name)
            vehicle_info_value = load_json_file(vehicle_info_path)
            vehicle_info_tag = sly.Tag(vehicle_info_meta, value=str(vehicle_info_value))
            tags.append(vehicle_info_tag)

            ann_path = os.path.join(masks_path, ann_name)
            ann = load_json_file(ann_path)[ann_name]
            img_height = ann["image_height"]
            img_wight = ann["image_width"]
            ann_data = ann["annotation"]
            for curr_ann_data in ann_data:
                label_tags = []
                obj_class_name = curr_ann_data["tags"][0].lower()
                obj_class = meta.get_obj_class(obj_class_name)

                if len(curr_ann_data["states"]) > 0:
                    depiction_data = curr_ann_data["states"].get("vehicle-depiction")
                    if depiction_data is None:
                        depiction_data = curr_ann_data["states"].get("person-depiction")
                    if depiction_data is not None:
                        depiction_value = depiction_data["text"]
                        depiction = sly.Tag(depiction_meta, value=depiction_value)
                        label_tags.append(depiction)

                    glass_data = curr_ann_data["states"].get("vehicle-glass")
                    if glass_data is None:
                        glass_data = curr_ann_data["states"].get("person-glass")
                    if glass_data is not None:
                        glass_value = glass_data["text"]
                        glass = sly.Tag(glass_meta, value=glass_value)
                        label_tags.append(glass)

                    occlusion_data = curr_ann_data["states"].get("vehicle-occlusion")
                    if occlusion_data is None:
                        occlusion_data = curr_ann_data["states"].get("person-occlusion")
                    if occlusion_data is not None:
                        occlusion_value = occlusion_data["text"]
                        occlusion = sly.Tag(occlusion_meta, value=occlusion_value)
                        label_tags.append(occlusion)

                    position_data = curr_ann_data["states"].get("vehicle-position")
                    if position_data is None:
                        position_data = curr_ann_data["states"].get("person-position")
                    if position_data is not None:
                        position_value = position_data["text"]
                        position = sly.Tag(position_meta, value=position_value)
                        label_tags.append(position)

                polygons_coords = curr_ann_data["segmentation"]
                exterior = []
                for coords in polygons_coords:
                    for i in range(0, len(coords), 2):
                        exterior.append([int(coords[i + 1]), int(coords[i])])
                poligon = sly.Polygon(exterior)
                label_poly = sly.Label(poligon, obj_class, tags=label_tags)
                labels.append(label_poly)

        else:
            ds_tag = sly.Tag(soiling_meta)
            tags.append(ds_tag)

            mask_path = image_path.replace(soiling_folder, masks_folder)
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            img_height = mask_np.shape[0]
            img_wight = mask_np.shape[1]
            unique_pixels = np.unique(mask_np)
            for curr_pixel in unique_pixels:
                obj_class = idx_to_class[curr_pixel]
                mask = mask_np == curr_pixel
                ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    if curr_bitmap.area > 30:
                        curr_label = sly.Label(curr_bitmap, obj_class)
                        labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    clean = sly.ObjClass("clean", sly.Bitmap, color=(0, 0, 0))
    transparent = sly.ObjClass("transparent", sly.Bitmap, color=(0, 255, 0))
    semi_transparent = sly.ObjClass("semi transparent", sly.Bitmap, color=(0, 0, 255))
    opaque = sly.ObjClass("opaque", sly.Bitmap, color=(255, 0, 0))

    idx_to_class = {0: clean, 1: transparent, 2: semi_transparent, 3: opaque}

    rgb_meta = sly.TagMeta("rgb", sly.TagValueType.NONE)
    soiling_meta = sly.TagMeta("soiling", sly.TagValueType.NONE)
    vehicle_info_meta = sly.TagMeta("vehicle info", sly.TagValueType.ANY_STRING)
    depiction_meta = sly.TagMeta("depiction", sly.TagValueType.ANY_STRING)
    glass_meta = sly.TagMeta("glass", sly.TagValueType.ANY_STRING)
    occlusion_meta = sly.TagMeta("occlusion", sly.TagValueType.ANY_STRING)
    position_meta = sly.TagMeta("position", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        tag_metas=[
            rgb_meta,
            soiling_meta,
            vehicle_info_meta,
            depiction_meta,
            glass_meta,
            occlusion_meta,
            position_meta,
        ],
        obj_classes=[clean, transparent, semi_transparent, opaque],
    )

    for class_name in classes_names:
        obj_class = sly.ObjClass(class_name.lower(), sly.Polygon)
        meta = meta.add_obj_class(obj_class)

    api.project.update_meta(project.id, meta.to_json())

    ds_name_to_data = {
        "train": {
            train_images_path: train_masks_path,
            soiling_train_images_path: soiling_train_masks_path,
        },
        "test": {
            test_images_path: None,
            soiling_test_images_path: soiling_test_masks_path,
        },
    }

    folder_to_prefix = {
        "rgb_images": "rgb_",
        soiling_folder: "soiling_",
        "rgb_images(test_set)": "rgb_",
    }

    for ds_name, ds_data in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        for images_path, masks_path in ds_data.items():
            images_names = os.listdir(images_path)
            prefix = folder_to_prefix[images_path.split("/")[-1]]

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                img_pathes_batch = [
                    os.path.join(images_path, image_name) for image_name in images_names_batch
                ]

                new_images_names_batch = [prefix + im_name for im_name in images_names_batch]

                img_infos = api.image.upload_paths(
                    dataset.id, new_images_names_batch, img_pathes_batch
                )
                img_ids = [im_info.id for im_info in img_infos]

                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(images_names_batch))
    return project
