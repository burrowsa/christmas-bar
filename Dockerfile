FROM node:11.1.0
RUN mkdir /xmasbar
COPY ./package.json /xmasbar
COPY ./package-lock.json /xmasbar
WORKDIR /xmasbar
RUN npm install
COPY ./build /xmasbar/build
COPY ./static /xmasbar/static
COPY ./src /xmasbar/src
COPY ./config /xmasbar/config
COPY ./index.html /xmasbar
COPY ./.babelrc /xmasbar
COPY ./.eslintignore /xmasbar
COPY ./.postcssrc.js /xmasbar
COPY ./.eslintrc.js /xmasbar
RUN npm run build

FROM alpine:3.6
LABEL com.centurylinklabs.watchtower.stop-signal="KILL"
RUN apk add --no-cache python3 python3-dev musl-dev gcc libffi-dev openssl-dev
RUN pip3 install Flask_SocketIO eventlet boto3 flask_ask
RUN addgroup xmasbar && \
    adduser -D -G xmasbar xmasbar
#RUN mkdir /data && chown xmasbar:xmasbar /data
RUN mkdir /xmasbar && chown xmasbar:xmasbar /xmasbar
USER xmasbar
COPY --chown=xmasbar:xmasbar --from=0 ./xmasbar/dist /xmasbar

COPY --chown=xmasbar:xmasbar ./aws.py /xmasbar
COPY --chown=xmasbar:xmasbar ./backend.py /xmasbar
WORKDIR /xmasbar
ENV FLASK_APP="backend.py"
ENTRYPOINT ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
EXPOSE 5000

