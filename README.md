## Microservice Architecture

# prerequisites
 - docker 
 - python
 - kubectl
 - mysql or postgresql
 - kubernetes cluster ( kind, minikube, eks, aks)
 - k9s ( dashboard) 

we focus on architecture so we deploy our services in local cluster with minikube.
   

# 1. Auth service
  - create a python/src/auth repo 
  - python3 -m venv venv
  - source ./venv/bin/activate 
  - env | grep VIRTUAL
  - we can install for vim configuration:  
      - pip install pylint
      - pip install jedi
    - pip install pyjwt (allow you to encode & decode json web tokens)
    - pip install flask
    - pip install flask_mysqldb

    so in server.py we configure our first authentication server
    then we create a init.sql and we create a user and database and table
      - for connecting to the database : mysql -u root > show databases;
      - mysql -u root < init.sql
        -> show databases;
        ->use auth;
        -> show tables;
        -> describe user;
        -> select * from user;
      - mysql -uroot -e "DROP USER auth_user@localhost"
      - mysql -uroot -e "DROP DATABASE auth"

      - Basic Auth
      - JSON web tokens

      - create a Dockerfile
      - pip3 freeze > requirements.txt ( run it inside the virtual envirements)

      - docker build .
      -docker tag <imagename:latest>
      - docker push rhosrow/auth:latest

Create a kubernetes manifest files for deployment of auth app.
so we create a deployment , configmap, secret and service yaml files 
and the we deploy it in minikube
    - minikube start --kubernetes-version=v1.30.0 --driver=docker
    - kubectl apply -f ./
    - kubectl get pods


# 2. gateway 
   python3 -m venv venv 
   source ./venv/bin/activate
   env | grep ENV
   pip3 install jedi 
   pip3 install pylint
   touch server.py

   then we install all dependencies
          import os, gridfs, pika, json
          from flask import Flask, request, jsonify
          from flask_pymongo import PyMongo
          from auth import validate
          from auth_svc import access
          from storage import util


     we make a 3 folder for storage & auth_svc & auth

     
      - create a Dockerfile
      - pip3 freeze > requirements.txt ( run it inside the virtual envirements)

      then kubernetes manifest with ingress 

        - minikube addons list
        - minikube addons enable ingress
        - kubectl apply -f ./




# 3. rabbitmq

we need statfulset for rabbit because if pods fails , the messages dont be droped too

 - kubectl scale deployment --replicas=0 gateway

 I create all of the rabbitmq manifests
 and then run again gateway pods
 