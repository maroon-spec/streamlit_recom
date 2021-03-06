import streamlit as st 
import numpy as np 
from PIL import Image
import base64
import io

import os
import requests
import numpy as np
import pandas as pd

#Copy and paste this code from the MLflow real-time inference UI. Make sure to save Bearer token from 
def create_tf_serving_json(data):
  return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

def score_model(dataset):
  token = os.environ.get("DATABRICKS_TOKEN")
  url = 'https://e2-demo-tokyo.cloud.databricks.com/model/jmaru_tfsim/1/invocations'
  headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}'}
  data_json = dataset.to_dict(orient='split') if isinstance(dataset, pd.DataFrame) else create_tf_serving_json(dataset)
  response = requests.request(method='POST', headers=headers, url=url, json=data_json)
  if response.status_code != 200:
    raise Exception(f'Request failed with status {response.status_code}, {response.text}')
  return response.json()

def render_response_image(i):
#“””response is the returned JSON object. We can loop through this object and return the reshaped numpy array for each recommended image which can then be rendered”””

    single_image_string = ret[i]["0"]
    image_array = np.frombuffer(bytes.fromhex(single_image_string), dtype=np.float32)
    image_reshaped = np.reshape(image_array, (28,28))
    st.image(image_reshaped, width=100)
st.image("images/heading.png")

#Source: https://discuss.streamlit.io/t/png-bytes-io-numpy-conversion-using-file-uploader/1409
img_file_buffer = st.file_uploader('Upload a PNG image', type='png')
if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    img_array = np.array(image)
    st.write("Uploaded Image: ")
    st.image(image, width = 100)
# To convert to a string based IO:
    byteIO = io.BytesIO()
    image.save(byteIO, format='PNG')
    img_str = base64.b64encode(byteIO.getvalue())


    model_input  =  img_str.decode("utf-8")

    df = pd.DataFrame.from_dict({"input": [model_input] })

    ret = score_model(df) 

    st.write("Recommended Items")
    #st.write(ret)

    col0, col1, col2, col3, col4 = st.columns(5)

    with col0:
        render_response_image(0)
    with col1:
        render_response_image(1)
    with col2:
        render_response_image(2)
    with col3:
        render_response_image(3)
    with col4:
        render_response_image(4)


    
