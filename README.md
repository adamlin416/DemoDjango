# Django demo shopping backend

## Description

This is a demo project, an order system backend.

## Quick Start
I've included the migrate command and a custom command for permission management in `entrypoint.sh`.  
So simply execute:
```
docker-compose up -d
```

Once all containers are started, API is ready on http://localhost:8000  
Visit API document via http://localhost:8000/api/schema/redoc  

Run unit test by:
```
docker exec -it demobotrista-web sh -c "cd ./demobotrista && python manage.py test"
```

Run docke compose to gracefully bring down containers
```
docker-compose down
```


## Business Features Overview
### Authentication:
`POST /api/token/`: Accepts user credentials to return an access and refresh JSON web token pair.  
`POST /api/token/refresh/`: Accepts a refresh token and returns a new access token if the refresh token is valid.  
`POST /api/token/verify/:` Accepts a token to verify its validity.  
### Orders:
`GET /orders/`: Lists all orders (managers only).  
`POST /orders/`: Creates a new order (customers only).  
### Products:
`GET /products/`: Lists all products, with optional filters for price or stock.  
`POST /products/`: Creates a new product (managers only).  
`GET /products/{id}/`: Retrieves a product by ID.  
`PUT /products/{id}/`: Updates a product by ID (managers only).  
`DELETE /products/{id}/`: Deletes a product by ID (managers only).  
### Users:
`GET /users/`: Lists all users (managers only).  
`POST /users/`: Creates a new user.  
`GET /users/{id}/`: Retrieves a user's information if id is their ID.  
`PUT /users/{id}/`: Updates a user's own information if id is their ID.  
`DELETE /users/{id}/`: Deletes a user's own account if id is their ID.  
## Security
All operations(except for user create) requiring authentication are protected using JWT (JSON Web Token).


## Technical Features
- All APIs are covered by unit tests, completed using the rest_framework.test module, which is based on the unittest module.
- Implements RFC 7807 for concise error handling using Django Middleware.
- Custom permission control and authentication inherited from Django's built-in authentication system.
- Utilizes serializers for data handling.
- Uses serializers and drf-spectacular to manage serialization and auto-generate documentation.

# TODOs
In a production environment, I would generally implement the following features and tools:  
**Logging and Monitoring**:  
  - Logging collection using ELK Stack or a cloud-based solution.
  - Monitoring indices with Prometheus and Grafana or other similar tools.

**Server Configuration**:
  - Web server setup using Gunicorn and Nginx for enhanced performance and reliability.

**Architecture**:
  - Utilizing Kubernetes (K8s) or other server architectures like ECS for scalable cluster management, enabling dynamic scale-in and scale-out capabilities.

**Caching**:
  - Implementing caching mechanisms to improve response times and reduce database load.