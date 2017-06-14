FROM python:3
COPY . /opt/frontend
WORKDIR /opt/frontend
RUN pip install -r requirements.txt
CMD python frontend.py
