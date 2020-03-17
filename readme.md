<h1>Capstone Project: Casting Agency</h1>

<h2>Motivation</h2>

<p>This project was an effort to combine all the skills I learned throughout the course of the Full Stack Developer Nanodegree, including:</p>
<ul>
    <li>SQL and Data Modeling for the Web</li>
    <li>API Development and Documentation</li>
    <li>Identity and Access Management</li>
    <li>Server Deployment, Containerization and Testing</li>
</ul>

<h2>Project Dependencies</h2>

<h3>### Python 3.7.4</h3>
<p>
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/windows.html?highlight=installing%20latest%20version%20python)
</p>

<h3>### PIP Dependencies</h3>
<p>
```bash
pip install -r requirements.txt
```
This will install all of the required packages for this project.
</p>

<h3>### Running the server</h3>
<p>
From within the root directory, each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.
</p>

<h2>Tasks</h2>

<h3>### Setup Auth0</h3>
<ol>
    <li>Create a new Auth0 Account</li>
    <li>Select a unique tenant domain</li>
    <li>Create a new, single page web application</li>
    <li>Create a new API
        - in API Settings:
            <ul>
                <li>Enable RBAC</li>
                <li>Enable Add Permissions in the Access Token</li>
            </ul>
    </li>
    <li>Create new API permissions:
        <ul>
            <li>get:actors</li>
            <li>get:movies</li>
            <li>post:actor</li>
            <li>post:movie</li>
            <li>patch:actor</li>
            <li>patch:movie</li>
            <li>delete:actor</li>
            <li>delete:movie</li>
        </ul>
    </li>
    <li>Create new roles for:
        <ul>
            <li>Casting Assistant
                - can get:actors and get: movies
            </li>
            <li>Casting Director
                - can perform all actions of Casting Assistant
                - can post:actor and delete:actor
                - can patch:actor and patch:movie
            </li>
            <li>Executive Producer
                - can perform all actions
            </li>
        </ul>
    </li>
</ol>