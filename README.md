# Project Setup Guide

## Production

1. **Open a New Terminal**: Open a new terminal window or tab.

2. **Navigate to the Backend Directory**: Change to the backend directory from the root of the project.

   ```bash
   cd backend
   ```

3. **Create a Virtual Environment**: Create a Python virtual environment in the current directory.

   ```bash
   python -m venv .venv
   ```

4. **Activate the Virtual Environment**:

   - On Windows:
     ```cmd
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

5. **Install Required Packages**: Install all dependencies listed in `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

6. **Set Environment Variable**: Set the Flask environment variable to production.

   - On Windows:
     ```cmd
     $env:FLASK_ENV="production"
     ```
   - On macOS/Linux:
     ```bash
     export FLASK_ENV=production
     ```

7. **Start flask server**: Run the flask server to serve static files

   ```bash
   flask run
   ```

## Development

### Frontend Setup

1. **Open a New Terminal**: Open a new terminal window or tab.

2. **Navigate to the Frontend Directory**: Change to the frontend directory from the root of the project.

   ```bash
   cd frontend
   ```

3. **Install Dependencies**: Install all required dependencies using npm.

   ```bash
   npm install
   ```

4. **Start the Development Server**: Launch the frontend development server.
   ```bash
   npm run dev
   ```

### Backend Setup

1. **Open a New Terminal**: Open a separate terminal window or tab for the backend setup.

2. **Navigate to the Backend Directory**: Change to the backend directory from the root of the project.

   ```bash
   cd backend
   ```

3. **Create a Virtual Environment**: Create a Python virtual environment in the current directory.

   ```bash
   python -m venv .venv
   ```

4. **Activate the Virtual Environment**:

   - On Windows:
     ```cmd
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

5. **Install Required Packages**: Install all dependencies listed in `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

6. **Set Environment Variable**: Set the Flask environment variable to development

   - On Windows:
     ```cmd
     $env:FLASK_ENV="development"
     ```
   - On macOS/Linux:
     ```bash
     export FLASK_ENV=development
     ```

7. **Start the Backend Server**: Run the backend server with debug mode enabled. This command starts the Flask server.
   ```bash
   flask run --debug
   ```
