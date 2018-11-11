FROM node:11.1.0
RUN mkdir /xmasbar
COPY ./package.json /xmasbar
COPY ./package-lock.json /xmasbar
WORKDIR /xmasbar
RUN npm install
COPY ./build /xmasbar
COPY ./static /xmasbar
COPY ./src /xmasbar
COPY ./config /xmasbar
COPY ./index.html /xmasbar
RUN npm run build

FROM alpine:3.6
RUN apk add --no-cache python3 python3-dev musl-dev gcc libffi-dev openssl-dev
RUN pip3 install Flask_SocketIO eventlet boto3 flask_ask
RUN addgroup xmasbar && \
    adduser -D -G xmasbar xmasbar
RUN mkdir /data && chown xmasbar:xmasbar /data
USER xmasbar
COPY ./dot_aws_config.txt /home/xmasbar/.aws/config
COPY ./dot_aws_credentials.txt /home/xmasbar/.aws/credentials
COPY --from=0 ./xmasbar/dist /xmasbar

COPY ./aws.py /xmasbar
COPY ./backend.py /xmasbar
WORKDIR /xmasbar
ENV FLASK_APP="backend.py"
ENTRYPOINT ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
EXPOSE 5000

