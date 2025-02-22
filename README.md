# ЛитХаб
![ЛитХаб](https://github.com/klon-22800/asm/blob/main/lithub.png)

## Стэк
**FastAPI**, **Redis**, **PostgresSQL**, **Celery**, **S3**,  **React**, **Docker**

![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![PostgresSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

## Описание 
ЛитХаб - сервис для обмена файлами между студентами и преподавателями университета. Позволяет загружать, хранить и делиться учебными материалами в одном месте, а также поддерживает систему доступа по ролям.

Проект создан для упрощения обмена лекциями, конспектами, методическими материалами и другими документами. Интуитивно понятный интерфейс и удобная система навигации помогают быстро находить нужные файлы и взаимодействовать с образовательным контентом. 

### Макет 
![Макет](https://github.com/klon-22800/asm/blob/main/model.jpg)


## Архитектура

Проект основан на микросервисном подходе с использованием современных технологий:

- FastAPI (Python) – backend-сервер, обрабатывающий запросы, аутентификацию и управление файлами.

- PostgreSQL – реляционная база данных для хранения информации о пользователях, ролях и загруженных файлах.

- Redis – кэширование, хранение сессий пользователей и брокер сообщений для задач Celery.
  
- S3-совместимое хранилище (Selectel) – хранение загруженных файлов и учебных материалов.
  
- Celery – обработка фоновых задач (например, обработка загруженных файлов, генерация превью, рассылка уведомлений).
  
- React (JavaScript) – frontend-приложение с интуитивно понятным интерфейсом для взаимодействия с платформой.
  
- Docker & Docker Compose – контейнеризация сервисов для удобного развертывания и масштабирования.

## Команда 
![capy](https://github.com/klon-22800/asm/blob/main/capy.jpg)

[**Denis**](https://github.com/Drowchik)- team-lead (￢_￢;)
[**Marina**](https://github.com/NozdryakovaMarina) - frontend (ﾉ◕ヮ◕)ﾉ*:･ﾟ
[**Andrey**](https://github.com/klon-22800) - backend (´• ω •`)
[**Ilya**](https://github.com/IluhaZaz) - backend (o･ω･o)
[**Egor**](https://github.com/yui1337)- UI/UX (◕‿◕)

<p align="center">
  <strong>Команда AltF4 © </strong>
</p>
