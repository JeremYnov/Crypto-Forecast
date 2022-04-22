FROM python:3.8

#RUN  apt update -y; \
     #apt upgrade -y; 
     #apk add python3; \
     #python3 -m ensurepip --upgrade; \
     #pip3 --no-cache-dir install --upgrade pip setuptools wheel;

#------------------------------------------------ Création des répertoires dans le conteneur ---------------------------
RUN mkdir cryptoForecast

#------------------------------------------------ Installation des paquets et de l'application -------------------------
COPY requirements.txt /cryptoForecast/requirements.txt

RUN pip install -r /cryptoForecast/requirements.txt

# COPY ./app.py /cryptoForecast/app.py
# COPY ./mongo_connector.py /cryptoForecast/mongo_connector.py
# COPY .env /cryptoForecast
# COPY ./scripts /cryptoForecast
# RUN touch /cryptoForecast/__init__.py
#------------------------------------------------ Initialisation des scripts automatiques ------------------------------
#Intialisation des données btc

CMD [ "python3", "/home/script_update_btc_datas.py", "True"]

#-------------------------------------------- Lancement de l'application -----------------------------------------------
#ENTRYPOINT [ "python" ]

#CMD [ "app.py" ]