#Démarrage du Docker sur linux
#sudo service docker start

#Connaitre le nombre de docker running
#sudo docker ps

#Connaitre les docker même arrêtés
#sudo docker ps -a

#Création de l'image
#sudo docker build -t hadock404/image:v1 .

#Lancement du container
#sudo docker run -dp 8081:8000 -ti --name image hadock404/image:v1

#Pousser le container sur DockerHub
#sudo docker push hadock404/image:v1

#Arrêter un container
#sudo docker stop nom_container

#Supprimer container
#sudo docker rm nom_container

#Lister les images
#sudo docker images

#Supprimer une image
#sudo docker rmi id_image

FROM python:3.10-slim

WORKDIR /app

COPY packages/requirements.txt .
RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]