FROM amazon/aws-lambda-python

COPY requirements.txt .

RUN pip install -r requirements.txt