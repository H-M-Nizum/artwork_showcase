# Local Artwork Showcase
This is a Local Artwork Showcase project using g Django, Django REST Framework, PostgreSQL and JWT-based authentication. This application will 
serve as a digital platform for local artists to share their artworks, including paintings, digital art, and sculptures, with the community

## To Run this project install this Requirements:
      python -m pip install Django
      pip install djangorestframework
      pip install markdown       
      pip install django-filter  
      pip install djangorestframework-simplejwt
      pip install django-cors-headers
    

## To Run this Project follow below:
      mkvirtualenv authenv
      pip install -r requirements.txt
      python manage.py makemigrations
      python manage.py migrate
      python manage.py runserver
    

## API Endpoints

### Artist
    
- **POST** `/registration/`
  - Description: Register a new Artist and genarate JWT token.
- **POST** `/login/`
  - Description: Login an Artist and genarate JWT token.
- **GET** `/profile/`
  - Description: Show an Artist profile.
- **PUT** `/profile/`
  - Description: Update an Artist profile.
- **PATCH** `/profile/`
  - Description: Partial update an Artist profile.

### Artwork
    
- **GET** `/artworks/`
  - Description: Show a list of all Artworks.
- **POST** `/artworks/`
    - Description: Create a new Artwok.
- **GET** `/artworks/{id}/`
    - Description: Show a specific Artwok.
- **PUT** `/artworks/{id}/`
    - Description: Update information of a specific Artwok.
- **PATCH** `/artworks/{id}/`
    - Description: Partial update information of a specific Artwok.
- **DELETE** `/artworks/{id}/`
    - Description: Delete a specific Artwok.

### JWT token
  - **POST** `/api/token/`
    - Description: Generate JWT token obtain pair.
 - **POST** `/api/token/refresh/`
    - Description: Genarate JWT refresh token.
     
       
