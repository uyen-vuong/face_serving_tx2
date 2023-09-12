import cv2, os, numpy as np
import onnx, configparser
from onnx import backend
import onnxruntime as ort

class EmotionInference:

    __instance = None 
    @staticmethod
    def getInstance():

        if EmotionInference.__instance is None:
            EmotionInference.__instance = EmotionInference()
        return EmotionInference.__instance 

    def __init__(self) -> None:
        
        print("Loading the model...")
        if ort.get_device() == "gpu":
        # If use CPU instead, change providers=['CUDAExecutionProvider'] into providers=['CPUExecutionProvider']
            self.model = ort.InferenceSession("./source/emotion/emotion-ferplus-8.onnx",
                    providers=['CUDAExecutionProvider'])
        else:
            self.model = ort.InferenceSession("./source/emotion/emotion-ferplus-8.onnx",
                    providers=['CPUExecutionProvider'])
        self.class_table = {0:'neutral', 1:'happiness', 2:'surprise', 3:'sadness', 4: 'anger', 
                    5: 'disgust', 6: 'fear', 7: 'contempt'}
        
        self.warming_up()

    def warming_up(self):
        """
        Warming up model with random and sample data

        input of age_model: 1 x 3 x height x width (height = width = 224), and converted to BGR format
        input of gender_model: 
        The model outputs a (1x8) array of scores corresponding to the 8 emotion classes, where the labels map as follows: 
        emotion_table = {'neutral':0, 'happiness':1, 'surprise':2, 'sadness':3, 'anger':4, 'disgust':5, 'fear':6, 'contempt':7}
        """
        try:
            image= cv2.imread("./test/test.png")
            data = self.preprocess(image)
            self.predict(data)
        except Exception as e:
            print("Exception warming up the model ", e)
    
    def preprocess(self, image):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (64, 64))
        image=  np.array([image])
        image = np.expand_dims(image, axis=0)
        image = image.astype(np.float32)
        return image

    def predict(self, image):
        input_ =  self.preprocess(image)
        input_name =  self.model.get_inputs()[0].name
        emotions =  self.model.run(None, {input_name: input_})
        emotions = emotions[0].argmax(axis=1)
        return emotions
