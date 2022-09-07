# CS421-FinalProject

## Running the Project
1. `cd` into the th `CS421-FinalProject` directory
2. run `python3 -m venv venv` to create a new python virtual enviroment
3. run `. venv/bin/activate` to launch the virtual enviroment
4. run `pip install -r requirements.txt` to install all needed dependances
5. run `python3 main.py`

Once the server has been launched go to http://127.0.0.1:5000/ for the website. 

admin loggin

**Email:** admin1@gmail.com

**Password:** 1234567 

## Database Structure
The database is Structred in the following way

### User Table

**Columns**

- `id` unique to each user, **primary key**
- `firstname` String
- `lastname` String
- `email` verified email
- `password` encrypted with SHA-256
- `admin_status` boolean

### Book Table
  
**Columns**

- `isbn` unique to each book, **primary key**
- `author` String
- `title` String
- `price` Float
- `stock_quantity` Integer
- `description` String

### Cart Table

**Columns**

- `user_id` related to the `id` in the `User table`
- `isbn` related to the `isbn` in the `Book table`
- `quantity` Integer
