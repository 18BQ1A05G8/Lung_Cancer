from tkinter.tix import COLUMN
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from tensorflow import keras
from keras.models import model_from_json
import pandas as np
from . import views
import warnings
warnings.filterwarnings('ignore')
import pickle

# Create your views here.

def home(request):
    return render(request,"index.html")
def deserialize():
    json_file = open('servey/data/model/ann_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("servey/data/model/ann_model.h5")
    return loaded_model
def results(request):

    # #RandomForest model
    pickle_in = open('servey/data/model.pkl', 'rb')
    RF_model = pickle.load(pickle_in)
    #ANN model
    ANN_model=deserialize() 

    dict={}
    if request.method=="POST":
        name=request.POST["NAME"]
        GENDER = int(request.POST["GENDER"])
        AGE = int(request.POST["AGE"])
        SMOKING = int(request.POST["SMOKING"])
        YELLOW_FINGERS = int(request.POST["YELLOW_FINGERS"])
        ANXIETY = int(request.POST["ANXIETY"])
        PEER_PRESSURE = int(request.POST["PEER_PRESSURE"])
        CHRONIC_DISEASE = int(request.POST["CHRONIC_DISEASE"])
        FATIGUE = int(request.POST["FATIGUE"])
        ALLERGY = int(request.POST["ALLERGY"])
        WHEEZING = int(request.POST["WHEEZING"])
        ALCOHOL_CONSUMING = int(request.POST["ALCOHOL_CONSUMING"])
        COUGHING = int(request.POST["COUGHING"])
        SHORTNESS_OF_BREATH = int(request.POST["SHORTNESS_OF_BREATH"])
        SWALLOWING_DIFFICULTY = int(request.POST["SWALLOWING_DIFFICULTY"])
        CHEST_PAIN = int(request.POST["CHEST_PAIN"])
        AGE=(AGE-21)//(87-21)
        
        if ANXIETY>5:
            ANXIETY=1
        else:
            ANXIETY=0
        if FATIGUE>5:
            FATIGUE=1
        else:
            FATIGUE=0
        input=[GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY,PEER_PRESSURE,CHRONIC_DISEASE, FATIGUE, ALLERGY, WHEEZING,
        ALCOHOL_CONSUMING, COUGHING,
        SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY, CHEST_PAIN]
        res_rf = RF_model.predict([input])
        res_ann= ANN_model.predict([input])[0]
        print(res_ann)
        print(res_rf)
        score=round(res_ann[0]*100,2)
        print(score)
        # score=0
        if score > 50:
            res_ann=1
        else:
            res_ann=0
        dict={
        'name':name,
        'res_rf':res_rf[0],
        'res_ann':res_ann,
        'cough':COUGHING,
        'score':score,
        'input':input
        }
        pickle_in.closed
        return render(request, 'results.html', dict)
    else:
        return render(request,'index.html') 
