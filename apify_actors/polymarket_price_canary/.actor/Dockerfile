# Polymarket Price Canary — Dry-Run Only Actor
#
# This image contains no code path that makes a network call to Polymarket
# or any other external host (see src/validation.py and src/main.py).
# The apify SDK's own calls to the Apify platform (for input/dataset I/O)
# are the only outbound traffic this container ever performs.

FROM apify/actor-python:3.11

COPY requirements.txt ./
RUN echo "Python version:" \
 && python --version \
 && pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python3", "-m", "src"]
