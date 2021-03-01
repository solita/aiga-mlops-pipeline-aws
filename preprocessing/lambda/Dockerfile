FROM public.ecr.aws/lambda/python:3.8

RUN pip install --upgrade pip && \
	pip install -t . Pillow 

COPY lambda_resize_image.py ./
CMD ["lambda_resize_image.lambda_handler"] 