
# FullStack E-Commerce Platform 

World Cart : World Cart is a comprehensive e-commerce platform designed to facilitate seamless online shopping experiences for users while providing robust management tools for administrators. The platform caters to both consumers looking to purchase a wide range of products and administrators responsible for overseeing the website's operations.



## Visuals of World Cart

For users:

![World Cart](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHA5ZmJuZnZibXcydmd4cWV2YndoMHVobmU5aTFxdWlwNnhpc3BvNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AnPQkilJjnnTuDdWGF/giphy.gif)

For admins:

![World Cart](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTFyODVybmJqY24zYnVvcmNnZG1yd2QyMGt0eWd1Y3FwemFpeDdpbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/x594Fj1TWBygBH6TaB/giphy.gif)
## Key Features
* User Functionality: Customers can easily browse products, add items to their cart, and complete purchases in a secure environment.
* Admin Dashboard: Administrators can manage product listings, including adding, editing, and removing products, as well as monitoring inventory levels.
* Transaction Management: Admins can view and track all transactions, ensuring transparency and accountability in sales.
* User Insights: The platform provides valuable insights into user activity, including total registered users, total sales, and the total number of products available.
## Technology Stack

* Backend: Developed with Flask, a lightweight Python web framework, enabling rapid development and scalability.
* Frontend: Utilizes Tailwind CSS for responsive and aesthetically pleasing design, along with HTML, CSS, and JavaScript for dynamic user interactions.
* Database: SQLAlchemy is employed for database management, providing a powerful ORM (Object-Relational Mapping) layer to interact with the database seamlessly.
* Node Modules: Integrated Node.js modules enhance functionality, allowing for the inclusion of various JavaScript libraries and tools.
## Installation
To set up the project, follow these steps:

1. **Clone the Repository:**
   ```bash
    git clone https://github.com/satyampandey444/World_Cart_FullStack_E-Commerce-Platform.git
    cd World_Cart_Fullstack_E-Commerce-Platform
2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Ensure pipenv is Installed:**
    ```bash
    pipenv install
4. **Install All the Dependencies from requirements.txt:**
     ```bash
     pipenv install -r requirements.txt
5. **Activate the Virtual Environment**
     ```bash
     pipenv shell
6. **Set Up Environment Variables**

     Create a `.env` file for sensitive API keys

7. **Run the Application**
     ```bash
    run app.py# World_Cart_Fullstack_E-Commerce-Platform


## Folder Structure
```
World_Cart_Fullstack_E-Commerce-Platform/
│
├── app/
│   ├── __pycache__/
│   ├── flask_session/
│   ├── static/
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── helping_functions.py
│   │   ├── models.py
│   │   ├── routes_admin.py
│   │   ├── routes_users.py
│   │   └── tailwind.config.js
│
├── instance/
├── node_modules/
├── .env
├── .gitignore
├── app.py
├── COC.txt
├── package-lock.json
├── package.json
├── README.md
├── requirements.txt
└── run_tailwind.sh
```

