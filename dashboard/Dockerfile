FROM python

WORKDIR /app

# Copy requirements files across
COPY requirements.txt .

# Install requirements file across 
RUN pip3 install -r requirements.txt

# Copy ETL script
COPY app.py .

EXPOSE 8501

# Run main pipeline script
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]