FROM python:3.8-slim
ARG VERSION
RUN useradd -d /opt/ms-temperature ms-temperature 
USER ms-temperature
WORKDIR /opt/ms-temperature
COPY main.py .
EXPOSE 8080
ENV VERSION=$VERSION
ENTRYPOINT ["python", "/opt/ms-temperature/main.py" ]
CMD [ "--port", "8080" ]
