Author: Qazi Arsalan Shah
Bechelors in Computer Science (Graduating Year)

Demo Video Link : https://youtu.be/lXdz1RuUpqk

Project Title : Todo Application (Technical Assessment)
Submitted to : CarteBlanche (Recruitment)

    Framework: Flask 
    Front End : HTML, CSS, Bootstrap
    Backend : Python
    Database : SQLITE3 with ORM (SQLAlchemy)

    Database Schema:

    Three Tables,
        - USER
        - TODO
        - TASK
    - One User can only have One TODO
    - Each TODO has 0 - many TASKS associated
    
    Created Three Models, 
        - User (id, username, email, password)
        - Todo (id, user_id[fk], backref[user])
        - Task (id, title, label, priority, todo_id[fk], backref[todo])

    To Use This Application,
        - Create Virtual Environment (Python 3.8.5)
        - Install the required packages/Libraries in requirement.txt file
        - python app.run

    Login Page Route : ...address/login
    Signup Page Route : ...address/signup
    Logout Page Route : ...address/logout
    Index Page Route : ...address/index

    etc....


    - app.py (is the main file)
    - static (contains static content) 
    - templates (contains all HTML files)
    - helpers (Contains few helper functions)


    - Developed this Project in a hurry, it Needs Refactoring :)

