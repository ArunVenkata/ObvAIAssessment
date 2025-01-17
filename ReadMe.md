# FastAPI Books API

This FastAPI application provides CRUD operations for managing books in an SQLite database (`books.db`). It also includes user authentication and real-time updates using Server-Sent Events (SSE).

## Setup

### Prerequisites

- Python 3.10 or higher
- SQLite

### Installation

1. Clone the repository:

```sh
git clone <repository-url>
cd <repository-directory>
```


2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

4. Set up the environment variables: 
    Refer to the .sample_env file
5. Run the application:

    `fastapi dev main.py`

The application will be available at http://localhost:8000.

## API Documentation
The API documentation is available at http://localhost:8000/docs

### Endpoints

#### Authentication

##### Register
URL: /auth/register
Method: POST
Body:
```javascript
    {
    "username": "your_username",
    "email": "your_email@example.com",
    "full_name": "Your Full Name",
    "password": "your_password"
}
```

Curl Request: 
```sh
curl --location --request POST 'http://localhost:8000/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "your_username",
    "email": "your_email@example.com",
    "full_name": "Your Full Name",
    "password": "your_password"
}'
```

##### Login
URL: /auth/login
Method: POST
Body:
```javascript
{
    "username": "your_username",
    "password": "your_password"
}
```

```sh
curl --location --request POST 'http://localhost:8000/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "your_username",
    "password": "your_password"
}'
```

#### Books
##### Create a Book
URL: /books
Method: POST
Body:
```javascript
{
    "title": "Book Title",
    "author": "Author Name",
    "published_date": "2023-01-01",
    "summary": "Book summary",
    "genre": "Genre"
}
```

Curl Request: 
```sh
curl --location --request POST 'http://localhost:8000/books' \
--header 'Authorization: Bearer your_access_token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Book Title",
    "author": "Author Name",
    "published_date": "2023-01-01",
    "summary": "Book summary",
    "genre": "Genre"
}'
```

##### Retrieve All Books
URL: /books

Method: GET

Query Parameters:

limit (optional): Number of books to retrieve (default: 10)
offset (optional): Number of books to skip (default: 0)

Curl Request: 
```sh
curl --location --request GET 'http://localhost:8000/books?limit=10&offset=0' \
--header 'Authorization: Bearer your_access_token'
```

##### Retrieve a Book by ID

URL: /books/{id}

Method: GET

Curl:

```sh
curl --location --request GET 'http://localhost:8000/books/{id}' \
--header 'Authorization: Bearer your_access_token'
```

##### Update a Book

URL: /books/{id}
Method: PUT
Body:
```javascript
{
    "title": "Updated Title",
    "author": "Updated Author",
    "published_date": "2023-01-01",
    "summary": "Updated summary",
    "genre": "Updated Genre"
}
```

Curl Request: 

```sh
curl --location --request PUT 'http://localhost:8000/books/{id}' \
--header 'Authorization: Bearer your_access_token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Updated Title",
    "author": "Updated Author",
    "published_date": "2023-01-01",
    "summary": "Updated summary",
    "genre": "Updated Genre"
}'
```

##### Partially Update a Book

URL: /books/{id}
Method: PATCH
Body:

```javascript
{
    "title": "Updated Title"
}
```

Curl Request: 
```sh
curl --location --request PATCH 'http://localhost:8000/books/{id}' \
--header 'Authorization: Bearer your_access_token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Updated Title"
}'
```

##### Delete a Book

URL: /books/{id}

Method: DELETE

Curl:

```sh
curl --location --request DELETE 'http://localhost:8000/books/{id}' \
--header 'Authorization: Bearer your_access_token'

```

#### Real-Time Updates

##### Server-Sent Events (SSE)


URL: /sse/events

Method: GET

Curl:
```sh
curl --location --request GET 'http://localhost:8000/sse/events'
```
