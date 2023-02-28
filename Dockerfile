FROM python:3.10-alpine
ARG displayVersion=
ENV DISPLAY_VERSION=$displayVersion
COPY scripts /usr/src/app/scripts/
COPY pyproject.toml /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install .
RUN apk add git
COPY license /root/work/.dotfiles/license/
COPY gradle /root/work/.dotfiles/gradle/
COPY docker /root/work/.dotfiles/docker/
ENTRYPOINT ["wt"]
