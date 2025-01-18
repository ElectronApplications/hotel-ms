# About

This app is an implementation (both backend and frontend) of a hotel management system, allowing you to manage clients, staff, hotel rooms, classes, services, accomodations, reservations, etc.

# Images

![image](https://github.com/user-attachments/assets/af0cbd07-5b0a-4a92-9909-06a6f48e4db4)
![image](https://github.com/user-attachments/assets/d254ebea-f09a-4ddb-a2e9-4e3019b36b8e)
![image](https://github.com/user-attachments/assets/d2b06726-822f-4cbe-9d58-83c8cec3308b)



# Deployment

To deploy the app you need to create the following files in the root directory based on their .example counterparts: `.env` and `local_settings.py`.  
Fill in all of the variable values in .env. To generate DJANGO_SECRET_KEY use the following bash command:  
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
You should also put your domain name in local_settings.py into the variable `CSRF_TRUSTED_ORIGINS`.  

You might also want to layer some of the project files in the layer directory. For example, you can put custom `favicon.ico` file in `layer/frontend/public/favicon.ico`.  
After all that use podman/docker compose to start the app:  
```bash
sudo docker compose build
sudo docker compose up -d
```

The service will be accessible at the port `HOTEL_MS_PORT`.  
You'll be able to login as the superuser with the credentials in the DJANGO_SUPERUSER_* variables.

# Technical

The backend is implemented in python and django and is located in the `backend` directory.  
The frontend is implemented in typescript and vue and is located in the `frontend` directory.  
The following database is used:  
```mermaid
erDiagram
    Client ||--o| User: user_id
    Client ||--|{ Accomodation: client_id
    Client ||--o{ Reservation: client_id

    Accomodation |o--o| Reservation: reservation_id
    Accomodation }|--|| Room: room_id
    Reservation }|--|| Room: room_id

    Accomodation ||--|{ ServiceCard: accomodation_id
    ServiceCard }|--|| Service: service_id

    Room }|--|| ClassInfo: class_id
    Service }|--|{ ClassInfo: mn

    ClassInfo }|--o| Gallery: gallery_id
    Service }|--o| Gallery: gallery_id

    Gallery ||--|{ GalleryImage: gallery_id

    Client {
        string name
        string phone_number
        UserRole role
        Image picture
    }

    Reservation {
        datetime move_in_time
        datetime move_out_time
    }

    Accomodation {
        datetime move_in_time
        datetime move_out_time
        decimal price_to_pay
        boolean was_price_paid
        boolean checked_out
    }

    ServiceCard {
        decimal price_to_pay
        datetime service_time
        boolean was_price_paid
    }

    ClassInfo {
        string class_description
        decimal place_price
    }

    Service {
        string service_description
        decimal service_price
    }

    Room {
        integer room_number
        RoomStatus status
    }

    Gallery {
        string name
    }

    GalleryImage {
        Image picture
    }
```
