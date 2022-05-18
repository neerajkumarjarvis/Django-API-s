FROM python:3.8
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /panna
WORKDIR /panna
COPY . /panna
# create directory.
#RUN mkdir -p /vol/web/
#RUN adduser --disabled-password --gecos '' user
#RUN chown -R user:user /vol/
#RUN chmod -R 755 /vol/web
#USER user
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
