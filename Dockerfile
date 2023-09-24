FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && \
    xargs -a packages.txt apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
EXPOSE 80
RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp credentials.toml ~/.streamlit/credentials.toml
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["main_app_streamlit.py"]