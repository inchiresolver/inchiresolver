#!/bin/bash

if ! id "app" >/dev/null 2>&1; then
    groupadd -g $CHEMBIENCE_GID app && \
    useradd --shell /bin/bash -u $CHEMBIENCE_UID -g $CHEMBIENCE_GID -o -c "" -M app
fi

mkdir -p /home/app/backup
chown -R app.app /home/app

export PYTHONPATH=/home/app:/home/app/scripts:/home/app/scripts/lib:/share:$PYTHONPATH

exec "$@"

