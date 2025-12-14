# Chat App

This project is a real-time chat application created as part of my internship at **Oasis Infobyte**.

## Description

This web-based chat application allows users to communicate in real-time. Users can create an account, log in, and then create or join chat rooms to send and receive messages instantly. The application is built using Python with the Flask framework and Flask-SocketIO for real-time communication.

## Features

*   User authentication (signup and login)
*   Create unique chat rooms
*   Join existing chat rooms using a room code
*   Real-time messaging with multiple users
*   User profile customization (profile picture)
*   See when users join or leave a room
*   Messages are timestamped
*   Empty rooms are automatically deleted

## Technologies Used

*   **Backend:** Python, Flask, Flask-SocketIO
*   **Frontend:** HTML, CSS, JavaScript
*   **Database:** (In-memory dictionaries for simplicity, not a persistent database)

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Abhimanyu-1G/OIBSIP.git
    ```
2. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

4.  Open your web browser and navigate to `http://127.0.0.1:5000` to use the application.

## Folder Structure

```
ChatApp/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── animation.js
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── lounge.html
│   ├── room.html
│   └── account.html
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Author

[Abhimanyu Singh Chouhan]
