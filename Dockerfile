FROM python:3

EXPOSE 5000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT [ "flask", "--app", "main.py","run", "--host=0.0.0.0"]
