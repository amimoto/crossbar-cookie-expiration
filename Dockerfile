ARG BASE_CONTAINER=crossbario/crossbar:cpy-amd64
FROM $BASE_CONTAINER

USER root

# Add a few useful commands
RUN    apt-get update \
    && apt-get install -y --no-install-recommends \
               tmux \
               vim-nox \
    && rm -rf ~/.cache \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sL https://deb.nodesource.com/setup_15.x  | bash - \
    && apt-get -y install nodejs \
    && npm install --global gulp-cli


ENTRYPOINT []
CMD /node/run-server-and-test.sh

