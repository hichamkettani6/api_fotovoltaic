FROM python:3.12

ENV PYTHONPATH="/app"

RUN pip install --upgrade fastapi
RUN pip install --upgrade celery
RUN pip install --upgrade websockets
RUN pip install --upgrade requests
RUN pip install --upgrade uvicorn
RUN pip install --upgrade redis
RUN pip install --upgrade jinja2


CMD ["uvicorn", "app.api_grafici_fotovoltaico:app", "--reload", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--forwarded-allow-ips='*'"]
