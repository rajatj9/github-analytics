FROM ubuntu:18.04
WORKDIR /app
RUN apt-get update -y && apt-get upgrade -y
RUN apt install cloc -y
RUN apt install openjdk-8-jdk -y
RUN apt install wget -y
RUN apt install git -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ADD app.py /app
ADD binaries /app/binaries
ADD scorers /app/scorers
ADD templates /app/templates
ADD results.py /app/
ADD dependencies /app/dependencies
ADD binaries /app/binaries

EXPOSE 5000

CMD python3 scorers/google_java_grader.py