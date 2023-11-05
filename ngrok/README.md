# Creación de la API con Flask

## 1. Introducción

Esta fase se centra en el desarrollo y despliegue de una API construida con Flask. Esta API facilita la interacción entre la aplicación y la base de datos NoSQL MongoDB. El proyecto ha sido contenerizado con Docker y actualmente está desplegado en un Synology DS224+ como contenedor Docker. Para proporcionar acceso externo a la API, se ha establecido un túnel desde el puerto local hacia Ngrok.

## 2. Tecnologías Implementadas

- **[Flask API](https://flask.palletsprojects.com/en/2.0.x/):** El corazón de esta fase es la API construida con Flask, un micro framework de Python, que permite la definición y gestión de rutas y funciones personalizadas para cada ruta.

- **[MongoDB](https://www.mongodb.com/):** La API se comunica con una base de datos NoSQL MongoDB para almacenar y recuperar datos necesarios para las operaciones de la aplicación.

- **[JWT (JSON Web Tokens)](https://jwt.io/):** Para asegurar la comunicación con la API, se implementó la autenticación mediante tokens JWT que garantiza que solo las solicitudes autorizadas sean procesadas.

- **[Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/):** Se utilizó Docker para contenerizar la aplicación y Docker Compose para gestionar los servicios de la aplicación y de Ngrok, facilitando el despliegue y la gestión del entorno.

- **[Ngrok](https://ngrok.com/):** Para exponer la API al mundo exterior, se estableció un túnel del puerto local a Ngrok, permitiendo el acceso remoto seguro a la API.

## 3. Referencias a Otros Proyectos

Este proyecto es una parte integral del ecosistema más amplio que incluye otras fases y aplicaciones. Para más detalles sobre cómo esta fase se integra con los demás componentes, se puede referir a:

- [Proyecto Principal - Chatbot StreamLit](https://github.com/GRKdev/StreamLit-Api)
- [Script para la Preparación de Datos](https://github.com/GRKdev/Script-SQL-API)

La Fase 3 se alinea con los objetivos globales del proyecto, proporcionando una API robusta y segura que facilita la interacción eficiente entre los usuarios, el chatbot y la base de datos.

---

# Creation of the API with Flask

## 1. Introduction

This phase focuses on the development and deployment of an API built with Flask. This API facilitates interaction between the application and the NoSQL MongoDB database. The project has been containerized with Docker and is currently deployed on a Synology DS224+ as a Docker container. To provide external access to the API, a tunnel has been established from the local port to Ngrok.

## 2. Implemented Technologies

- **[Flask API](https://flask.palletsprojects.com/en/2.0.x/):** The core of this phase is the API built with Flask, a micro framework of Python, which allows the definition and management of routes and custom functions for each route.

- **[MongoDB](https://www.mongodb.com/):** The API communicates with a NoSQL MongoDB database to store and retrieve necessary data for the application's operations.

- **[JWT (JSON Web Tokens)](https://jwt.io/):** To secure communication with the API, JWT token authentication was implemented, ensuring that only authorized requests are processed.

- **[Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/):** Docker was used to containerize the application, and Docker Compose was used to manage the application and Ngrok services, facilitating the deployment and management of the environment.

- **[Ngrok](https://ngrok.com/):** To expose the API to the outside world, a tunnel from the local port to Ngrok was established, allowing secure remote access to the API.

## 3. References to Other Projects

This project is an integral part of the broader ecosystem that includes other phases and applications. For more details on how this phase integrates with the other components, you can refer to:

- [API Docker Ngrok](https://github.com/GRKdev/api-docker-ngrok)
- [Main Project - Chatbot StreamLit](https://github.com/GRKdev/StreamLit-Api)
- [Script for Data Preparation](https://github.com/GRKdev/Script-SQL-API)

Phase 3 aligns with the global objectives of the project, providing a robust and secure API that facilitates efficient interaction between users, the chatbot, and the database.