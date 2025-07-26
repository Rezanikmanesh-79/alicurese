
# 🐳 AliCurese – Django Blog with Docker Compose

**AliCurese** is a Django-based blog web application fully containerized using **Docker Compose** for easy setup and deployment.

---

## 🚀 Features

- 📰 Blog post creation, editing, and publishing  
- 🔍 Post filtering and search  
- 🧑‍💼 Django admin panel  
- 🗓 Jalali calendar support (optional)  
- 🌐 Persian (Farsi) language support  
- 🐳 Easy containerized setup with Docker Compose  

---

## 🧰 Technology Stack

- Django 5.x  
- PostgreSQL (in Docker container)  
- Docker & Docker Compose  
- Gunicorn (WSGI server)  
- Nginx (optional, for production)  

---

## 📦 Project Structure

```

alicurese/
├── blog/
├── core/
├── static/
├── templates/
├── media/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py

````

---

## ⚙️ Getting Started with Docker Compose

Make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

1. Clone the repository:

```bash
git clone https://github.com/Rezanikmanesh-79/alicurese.git
cd alicurese
````

2. Build and start the containers:

```bash
docker-compose up --build
```

3. Access the application at:

```
http://localhost:8000/
```

4. To create a Django superuser (admin account), open a shell in the running Django container:

```bash
docker-compose exec web bash
python manage.py createsuperuser
```

---

## 📌 Notes

* Static files and media are handled inside the containers.
* Database data is persisted using Docker volumes.
* Modify `docker-compose.yml` and `.env` (if exists) to configure your environment.

---

## 👨‍💻 Author

**Reza Nikmanesh**
GitHub: [@Rezanikmanesh-79](https://github.com/Rezanikmanesh-79)

---

