# 📝 Todo App


## 🌟 Overview 🌟
The Todo App is a simple web application that allows users to manage their tasks. Users can create an account, log in, add tasks, mark tasks as complete, and move a top-level task under another top-level task. The application is built using Flask and SQLAlchemy, with SQLite as the database.


## 📹 Demo Video
<iframe width="560" height="315" src="https://www.loom.com/embed/f9a243ded85a4c5f839672afc68b5172" frameborder="0" allowfullscreen></iframe>



## 🚀 Features
- **🔒 User Authentication**:
  - 🎉 **Registration**: New users can create an account by providing a username and password.
  - 🚪 **Login/Logout**: Users can securely log in to access their tasks and log out when done.
  - 🔐 **Password Security**: Passwords are hashed before being stored, ensuring user data security.
- **✅ Task Management**:
  - ➕ **Add Tasks**: Users can quickly add new tasks to their list.
  - ✅ **Task Status**: Each task can be marked as complete or incomplete with a simple click.
  - ❌ **Delete Tasks**: Users can remove tasks they no longer need.
  - 🌳 **Hierarchical Task Organization**: Users can create tasks with subtasks and subsubtasks, enabling them to organize their tasks hierarchically. Additionally, users can move top-level tasks under other top-level tasks, allowing for flexible task organization.
- **📱 Responsive UI**:
  - 🎨 Built with the Semantic UI framework, the application offers a clean, intuitive, and mobile-responsive user interface.


## 🏗️ Code Structure
- **app.py**: The heart of the application.
  - 🛠️ **Flask Configuration**: Sets up the Flask app, database connection, and other configurations.
  - 🗃️ **Database Models**: Defines the User and Todo models for SQLAlchemy.
  - 🚦 **Routes**: Handles the application's logic, from user registration and authentication to task management.
- **templates folder**: Houses the HTML templates.
  - 📄 **login.html**: Renders the login page.
  - 📝 **signup.html**: Displays the user registration form.
  - 🏠 **base.html**: The core template where users interact with their tasks.
