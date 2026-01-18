# CLI Notes Manager

A **command-line application** that helps users **organize notes and tasks locally** using a clean structure of **workspaces, notebooks, notes, and tasks**.

All data is stored on your system using the filesystem — no internet, no database, no external services.

---

## What is this app?

It allows you to:
- create an account
- log in securely
- organize your notes and tasks in a structured way
- access everything from the command line

---

## What can users do?

### Authentication
- Sign up with a username and password
- Log in to access personal data
- Each user has isolated data storage

---

### Workspaces
Workspaces help separate different areas of your life.

Examples:
- `Personal`
- `College`
- `Work`
- `Projects`

Users can:
- create a workspace
- list existing workspaces
- select a workspace to work in
- delete a workspace

---

### Notebooks
Inside a workspace, notebooks help group related notes.

Examples:
- `Python`
- `Math`
- `Meeting Notes`

Users can:
- create notebooks
- list notebooks
- delete notebooks

---

### Notes
Notes are simple text files where users store information.

Users can:
- create notes
- edit notes
- view notes
- search notes
- delete notes

Notes can exist:
- directly inside a workspace
- or inside a notebook

---

### Tasks
Tasks help track to-do items.

Users can:
- add tasks
- list tasks
- update task status
- delete tasks

Tasks are stored alongside notes within a workspace or a notebook.

## How the application flows

1. User starts the app
2. User logs in or signs up
3. A session is created for the logged-in user
4. User selects or creates a workspace
5. Inside the workspace, the user can:
   - manage notebooks
   - create and manage notes
   - create and manage tasks
6. All changes are saved automatically to local storage
7. User exits the app safely

---

## Session Handling 

- The app maintains a single active session
- The session remembers:
  - which user is logged in
  - which workspace is currently active
- This ensures user data is always kept separate and safe

---

## Data Storage

- All data is stored locally under a `user_data/` directory
- Each user has their own folder
- Workspaces, notebooks, notes, and tasks are saved as files and folders
- No internet connection is required

---

## Logging

- The app keeps logs of important actions
- Logs help debug issues if something goes wrong
- Sensitive data like passwords is never logged

---

## How to run the app

### Requirements
- Python 3.8 or higher

### Run
```bash
python -m src.notes.app
```

