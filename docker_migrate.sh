#!/usr/bin/env bash
/etc/init.d/postgresql start
cd smc-back
/root/.pyenv/versions/app/bin/python manage.py collectstatic --noinput
/root/.pyenv/versions/app/bin/python manage.py migrate --noinput
