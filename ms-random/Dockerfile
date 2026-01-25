FROM python:3.8-slim
ARG VERSION
RUN useradd -d /opt/ms-random ms-random 
USER ms-random
WORKDIR /opt/ms-random
COPY main.py .
EXPOSE 8080
ENV VERSION=$VERSION
ENTRYPOINT ["python", "/opt/ms-random/main.py" ]
CMD [ "--port", "8080" ]
