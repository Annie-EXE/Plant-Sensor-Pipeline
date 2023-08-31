FROM amazon/aws-lambda-python

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir /ETL

COPY extract.py .

COPY transform.py .

COPY load.py .

COPY lambda_function.py .