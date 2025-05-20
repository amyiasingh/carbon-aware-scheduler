FROM python:3.11-slim

# working dir
WORKDIR /app

# copy project files
COPY . /app

RUN pip install --no-cache-dir \
    requests \
    matplotlib \
    torch \
    torchvision \
    pandas

# run the scheduler script
CMD ["python", "scheduler.py"]
