FROM python:latest

RUN pip install uvicorn
RUN pip install fastapi
RUN pip install pydantic
RUN pip install httpx
RUN pip install pytest



LABEL Maintainer="wafda.mufti"


WORKDIR .

COPY main.py ./

CMD [ "python", "./main.py"]

