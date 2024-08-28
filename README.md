# Social-Media-App

This project is a Django-based API for a social network platform. It includes features for user registration, login, managing friend requests, and handling friendships.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (optional but recommended)
- Django 3.2 or higher
- Django RestFramework

### Steps to Install and Run the Project

1. **Clone the Repository**

   Clone the repository to your local machine using:

   git clone https://github.com/yourusername/your-repository.git
   cd your-repository

2. **Create a Virtual Environment**
    
    python -m venv venv
    source venv/bin/activate

3. **Install Dependencies**

    pip install -r requirements.txt

4. **Perform below steps-**

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

5. **API Endpoints**
    User Registration
        - URL: /api/creds/register/
        - Method: POST
        - Body : {
            "email": "admin@gmail.com",
            "password": "admin@A123"
            }

    User Login
        - URL: /api/creds/login/
        - Method: POST
        - Body: {
            "email": "admin@gmail.com",
            "password": "admin@A123"
            }

    Send Friend Request
        - Authentication: Required
        - URL: /api/creds/send-friend-request/
        - Method: POST
        - Body : {
            "receiver_id": 2
            }

    Accept Friend Request
        - Authentication: Required
        - URL: /api/creds/accept-friend-request/
        - Method: POST
        - Body : {
            "request_id": 1
            }
    
    Reject Friend Request
        - Authentication: Required
        - URL: /api/creds/reject-friend-request/
        - Method: POST
        - Body: {
            "request_id": 1
            }
    
    List Friends
        - URL: /api/creds/list-friends/
        - Method: GET
        - Authentication: Required
        - Description: Retrieve a list of friends for the authenticated user.

    List Pending Requests
        - URL: /api/creds/list-pending-requests/
        - Method: GET
        - Authentication: Required
        - Description: Retrieve a list of pending friend requests for the authenticated user.

6. **Models**

    - FriendRequest      
        sender: The user who sent the friend request.
        receiver: The user who received the friend request.
        timestamp: The time when the friend request was sent.

    - Friendship
        user1: One user in the friendship.
        user2: The other user in the friendship.
        created_at: The time when the friendship was created.

7. **Serializers**

    - UserSerializer (For User Info)
    - FriendRequestSerializer (Friend Request Records To Serialize)
    - FriendshipSerializer (FriendShip Records To Serialize)
    - RegisterSerializer (Validate Registered User)










