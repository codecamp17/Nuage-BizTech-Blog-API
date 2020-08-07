# Nuapp Biz technologies
Nuapp Biz technologies Internship Assignment 

Used Postman as mock server for testing API response

# How to run the project
## Install dependencies
```python
pip install -r requirements.txt
```
## Start MongoDB Server
To start MongoDB Server in Windows, start Mongo Daemon (mongod.exe)
```cmd
C:\> "C:\Program Files\MongoDB\Server\4.2\bin\mongod.exe"
```
## Config the application
Change the `Database Name` in the `config.py` file according to the database name you are using.
Change the `blogData.py` line no.14 and 16 and give respective `Database name` and `collection name`

## Start the application
```cmd
python run-app.py
```

Once the application is started, go to [localhost](http://localhost:5000/)
on Postman and explore the APIs.

# Following Endpoints are supported
1. http://127.0.0.1:5000/api/blog - POST - To create a new blog
2. http://127.0.0.1:5000//api/blog/{id} - GET - To get the details of a blog
3. http://127.0.0.1:5000//api/blog/api/blog?{Query} - GET - To list the blogd according to the query
4. http://127.0.0.1:5000//api/blog/{id} - PUT - To update the details of a blog (use $set parameter Example:
```JSON
{
	"$set": {
		"name": "This is my blog"
	}
}
``` 
5. http://127.0.0.1:5000//api/blog/{id} - DELETE - To delete the blog
