FROM python:3.10
LABEL AUTHOR=6hl

# Create directories
RUN mkdir /app
WORKDIR /app

# Copy repo dir into image
COPY . /app

# Install app
RUN python -m pip install .
RUN python -m pip install openai beautifulsoup4 flask gunicorn gpt4all
ENV PATH="/usr/local/bin/:${PATH}"

ENV PYTHONUNBUFFERED=TRUE

EXPOSE 8080
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]