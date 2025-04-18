#!/bin/bash

set -e

# Ensure python is available
export PATH="/opt/render/project/.venv/bin:$PATH"

# Run your Python build logic
python3 script.py


#!/bin/bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py collectstatic --noinput
