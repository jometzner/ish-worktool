FROM python:3-alpine as buildstep
COPY scripts /usr/src/app/scripts/
WORKDIR /usr/src/app/scripts
RUN pip3 install --user --no-cache-dir --requirement Requirements.txt
RUN python3 setup.py install --user

FROM python:3-alpine
COPY --from=buildstep /root/.local /usr/local/
RUN apk add git
ARG displayVersion=
ENV DISPLAY_VERSION=$displayVersion
COPY license /root/work/.dotfiles/license/
COPY gradle /root/work/.dotfiles/gradle/
ENTRYPOINT ["wt"]
