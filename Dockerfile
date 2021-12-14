FROM python:3.9
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . /app
ENTRYPOINT [ "streamlit", "run" ]
CMD ["app.py"]
# CMD ["justtry/streamapp.py"]
# docker build -t epm:latest .
# docker run -p 8501:8501 epm:latest