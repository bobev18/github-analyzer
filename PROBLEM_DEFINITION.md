# GitHub User Analyzer

In this task, You will have to complete some parts of a web application that:

- Displays GitHub User data, provided in a more user-friendly way. 
- A user should be able to search by 'github_username' and see information about him/her.
- The code is written in Python(back-end) and Angular(front-end).
- To gather the user data, we fetch it from GitHub, using their GitHub REST API.

### Task requirements
Once You start the application and get familiar with it,
You need to add the following information in the UI for a specific user:
- return the number of followers for a user
- return the list of repos of a user
- return the most used language/technology from the list of repos
- return a list of all technologies used in all repos

Additional information:
- return a meaningful message when a user does not exist
- return a meaningful message when a user does not have repos
- return a meaningful message when a user does not have followers

We are providing You with the following code structure and setup steps for the project.


```github-analyzer/
|
 |-----backend/
|    |----main.py
|    |----github_api.py
|    |----github_user.py
|
 |-----frontend/
|    |----app.module.ts
|    |----github.service.ts
|    |----app.component.ts
|    |----app.component.html
|
 |-----requirements.txt
 |-----README.md
 ```

Within the files, You will find the places, which You need to extend/implement. 
Feel free to show your knowledge and creativeness with this task.
If You'd like to extend the task, You can add styles or additional functionalities.


### Setup Steps

You can create a virtualenv for the project.

#### Backend

Run this from the backend folder.

```commandline
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

Run this from the frontend folder. 

```commandline
npm install
ng serve
```


### Notes

The GitHub API is rate-limited -> up to 60 requests per hour, without authentication.

Some repos don't have technologies/languages.
Use OOP for the GithubUser class.
If You have additional questions, You can reach out to us.

Wish you luck and have fun!

