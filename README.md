# TracePesa API.  
## Every cent matters!
A simple budgeting tool to fastrack users expenditure.  
TracePesa aims to log users' expenditures from various payments platforms.  
  
For a start, we're making it possible to trace expenditures logged on Mpesa  
- Lipa na Mpesa options of:
- Till Number & Paybill

Next, we'll look into the various mobile wallets and maybe trace crypto.  
  
![logo](https://i.imgur.com/I3m75vU.png)  



## SETUP  

## RUN  
Create a virtual environment.  
```
$ python -m venv .trace  
```

```
$ pip3 install -r requirements.txt  
```

## RUN  

```
$ API_HOST=0.0.0.0 API_PORT=5000 python app.py  
```

## ROUTES  

- `POST /api/v1/signup`: creates a new user with specified params(email, password, username, name).  
- `POST /api/v1/expense/add`: adds a user expenditure.  
- `DELETE /api/v1/expense/remove/int:expense_id>`: deletes an expenditure.
- `GET /api/v1/expenses/<int:user_id>`: retrieves all expenses for a user.
- `PUT /api/v1/expense/update/<int:expense_id>`: updates an expenditure.
- `PUT /api/v1/reset_password:<int>`: resets user password(params: {email, newpassword})
- `GET /api/v1/users`: retrieves all users in the database
