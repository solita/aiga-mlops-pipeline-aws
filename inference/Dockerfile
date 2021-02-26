FROM daisukekobayashi/darknet:gpu


# Download the SKU110K image set

# RUN apt-get update -y && \
# 	apt-get upgrade -y && \
# 	apt-get install -y wget

# RUN mkdir SKU110K \
# 	&& cd SKU110K \
# 	&& mkdir raw \
# 	&& mkdir done \
# 	&& wget http://trax-geometry.s3.amazonaws.com/cvpr_challenge/SKU110K_fixed.tar.gz \
# 	&& tar -zxvf SKU110K_fixed.tar.gz --directory raw \
# 	&& rm SKU110K_fixed.tar.gz 


# Download pretrained weights

# WORKDIR darknet

# RUN wget https://solitabay.solita.fi/index.php/s/rQ646gAicerjeRW/download && \
# 	mv download darknet53.conv.74

# ENTRYPOINT ["./darknet", "detect", "cfg/yolov3.cfg", "yolov3.weights", "data/dog.jpg"]


# RUN pip3 install sagemaker-training
# COPY train.py /opt/ml/code/train.py
# ENV SAGEMAKER_PROGRAM train.py

# ADD ./requirements.txt .
# RUN pip3 install -r requirements.txt

# ENV PYTHONUNBUFFERED=TRUE

# ADD resize_images.py /
# ENTRYPOINT ["python3", "/resize_images.py"]