# SPDX-License-Identifier: MIT

import cv2
import onnxruntime as ort
import argparse
import numpy as np
from dependencies.box_utils import predict

class LightWeightDetection:

    __instance = None 

    @staticmethod
    def getInstance():
        if LightWeightDetection.__instance is None:
            LightWeightDetection.__instance = LightWeightDetection()
        return LightWeightDetection.__instance
    
    def __init__(self) -> None:
        # ------------------------------------------------------------------------------------------------------------------------------------------------
        # Face detection using UltraFace-320 onnx model
        face_detector_onnx = "./source/ultraface/version-RFB-640.onnx"
        # Start from ORT 1.10, ORT requires explicitly setting the providers parameter if you want to use execution providers
        # other than the default CPU provider (as opposed to the previous behavior of providers getting set/registered by default
        # based on the build flags) when instantiating InferenceSession.
        # For example, if NVIDIA GPU is available and ORT Python package is built with CUDA, then call API as following:
        # ort.InferenceSession(path/to/model, providers=['CUDAExecutionProvider'])
        print("Loading the model...")
        if ort.get_device() == "gpu":
        # If use CPU instead, change providers=['CUDAExecutionProvider'] into providers=['CPUExecutionProvider']
            self.model = ort.InferenceSession(face_detector_onnx,
                    providers=['CUDAExecutionProvider'])
        else:
            self.model = ort.InferenceSession(face_detector_onnx,
                    providers=['CPUExecutionProvider'])

    # scale current rectangle to box
    def scale(self, box):
        width = box[2] - box[0]
        height = box[3] - box[1]
        maximum = max(width, height)
        dx = int((maximum - width)/2)
        dy = int((maximum - height)/2)
        bboxes = [box[0] - dx, box[1] - dy, box[2] + dx, box[3] + dy]
        return bboxes

    # crop image
    def cropImage(self, image, box):
        num = image[box[1]:box[3], box[0]:box[2]]
        return num

    # face detection method
    def predict(self, orig_image, threshold = 0.5):
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640, 480))
        image_mean = np.array([127, 127, 127])
        image = (image - image_mean) / 128
        image = np.transpose(image, [2, 0, 1])
        image = np.expand_dims(image, axis=0)
        image = image.astype(np.float32)

        input_name = self.model.get_inputs()[0].name
        confidences, boxes = self.model.run(None, {input_name: image})
        boxes, labels, probs = predict(orig_image.shape[1], orig_image.shape[0], confidences, boxes, threshold)
        boxes = [self.scale(boxes[i, :]) for i in range(boxes.shape[0])]
        return boxes, labels, probs
# ------------------------------------------------------------------------------------------------------------------------------------------------
# Main void

# parser=argparse.ArgumentParser()
# parser.add_argument("-i", "--image", type=str, required=False, help="input image")
# args=parser.parse_args()

# img_path = args.image if args.image else "dependencies/1.jpg"
# color = (255, 128, 0)

# orig_image = cv2.imread(img_path)
# boxes, labels, probs = faceDetector(orig_image)

# for i in range(boxes.shape[0]):
#     box = scale(boxes[i, :])
#     cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), color, 4)
#     cv2.imshow('', orig_image)

