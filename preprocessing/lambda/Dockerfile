FROM public.ecr.aws/lambda/python:3.8

RUN pip install --upgrade pip && \
	pip install -t . Pillow 

RUN mkdir /tmp/input && mkdir /tmp/output 
#&& chmod a+rw input output

COPY resize_image.py ./
CMD ["resize_image.lambda_handler"] 