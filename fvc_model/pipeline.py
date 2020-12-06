from fvc_model.neural_network import nn_model
from loader.loader import load_scan
from train import correct_dim_size
from tqdm import tqdm

import tensorflow as tf
import scipy.signal
import numpy as np
import os

def fvc_pipeline(patient, categorical_data):
    target_scan_size = (128, 64, 64, 1)
    model = nn_model(
        scan_size=target_scan_size,
        backbone_weights="/projectnb/ece601/F-PuPS/Hellman_working_directory/ec601-term-project/segmentation/weight_lung",
    )

    patient_data = {"data": [[], []]}

    scan_data = load_scan(patient)

    slice_dim = scan_data.shape[1]

    # Cropping or padding to appropriate size
    for axis_idx, _ in enumerate(scan_data.shape):
        scan_data = correct_dim_size(scan_data, target_scan_size[axis_idx], axis_idx)

    scan_data = scan_data / 255.
    scan_data = np.expand_dims(scan_data, axis=-1)

    patient_data["data"][0].appen(scan_data)

    data_pt = [
        categorical_data["weeks"],
        categorical_data["age"],
        float(sex_to_int(categorical_data["sex"])),
        float(smoking_status_to_int(categorical_data["smoking_status"])),
    ]
    patient_data["data"][1].append(data_pt)
    predictions = model.predict(test_arr)