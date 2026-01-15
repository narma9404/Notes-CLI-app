# Notes — CLI Notes Application

Modular command-line notes and task manager.

## Project layout

- `app.py` — CLI entry point  
- `configs/` — configuration containers 
- `src/` — core packages and services  
  - `auth/` — authentication service & validators  
  - `workspace/` — workspace management service  
  - `notebook/` — notebook directory service  
  - `note/` — note file service  
  - `task/` — task file service  
  - `session/` — user session   
  - `utils/` — logging & helpers  


## Configuration

- `NOTES_APP_ROOT` — Root directory for the application
- `NOTES_DATA_DIR` — Directory to store user workspaces and files
- `NOTES_CREDENTIALS_FILE` — Path to user credentials CSV
- `NOTES_LOG_FILE` — Path to log file
- `NOTES_PBKDF2_ITERS` — PBKDF2 hashing iterations for passwords
- `NOTES_SALT_BYTES` — Salt byte size for password hashing

