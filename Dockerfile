FROM alpine:3.6
RUN apk add --no-cache python3 python3-dev musl-dev gcc
RUN pip3 install Flask_SocketIO eventlet
RUN addgroup xmasbar && \
    adduser -D -G xmasbar xmasbar
RUN mkdir /data && chown xmasbar:xmasbar /data
USER xmasbar
COPY ./dist /xmasbar
COPY ./backend.py /xmasbar
WORKDIR /xmasbar
ENV FLASK_APP="backend.py"
ENTRYPOINT ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
EXPOSE 5000

