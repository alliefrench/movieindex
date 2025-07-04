### **Project Plan: Neon Auth Integration and Vercel Deployment**

**Objective:** To integrate the React frontend and FastAPI backend with Neon's built-in authentication for Google Logins. The final application will be deployed on Vercel, with a seamless, secure authentication flow and a serverless database backend.

---

### **Phase 1: Database and Authentication Setup (Neon)**

The foundation of the project. This phase involves configuring the external services that the application will depend on.

- **Task 1.1: Configure Neon Project**

  - [x] Create a new project in Neon.
  - [x] Locate and securely store the PostgreSQL connection string. This will be used as an environment variable.

- **Task 1.2: Enable and Configure Neon Auth**

  - [x] In the Neon project settings, enable the built-in Auth feature.
  - [ ] Configure Google as the social login provider. You will need to provide Google with a **Redirect URI**. For local development, this will be something like `http://localhost:3000/auth/callback`. For production, it will be `https://<your-vercel-domain>/auth/callback`.
  - [ ] From the Neon Auth settings, locate and store the following critical values:
    - **JWKS URI:** The URL where your backend can find the public keys to verify tokens.
    - **Issuer URL:** The `iss` value that will be in the JWTs.
    - **Audience:** The `aud` value for your API.
    - **Client ID:** The public identifier for your application.

- **Task 1.3: Define Database Schema**
  - [x] Connect to the Neon database using a database client.
  - [x] Execute the SQL `CREATE TABLE` statement for the `users` table. This table will store application-specific user data, linked to the Neon Auth identity.
    ```sql
    CREATE TABLE users (
        id TEXT PRIMARY KEY, -- Will store the 'sub' claim from the JWT
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    ```

---

### **Phase 2: Backend Development (FastAPI `api/`)**

Implement the API logic to handle authentication and interact with the database.

- **Task 2.1: Update Dependencies**

  - [ ] Ensure `api/requirements.txt` includes:
    - `fastapi`
    - `uvicorn`
    - `sqlalchemy`
    - `psycopg2-binary`
    - `python-jose[cryptography]`

- **Task 2.2: Implement Database Models and Session**

  - [ ] Create a `database.py` file to manage the SQLAlchemy engine and session logic.
  - [ ] Create a `models.py` file and define the `User` table using SQLAlchemy's ORM, matching the schema from Task 1.3.

- **Task 2.3: Implement Core Authentication Logic**

  - [ ] Create an `auth.py` module.
  - [ ] Implement a function to fetch and cache Neon's public keys from the JWKS URI.
  - [ ] Create a FastAPI "dependency" function (`get_current_user`). This function will:
    1.  Extract the JWT from the `HttpOnly` cookie on incoming requests.
    2.  Decode and validate the JWT using the fetched public keys and the correct `audience` and `issuer` values.
    3.  Extract the user's ID (`sub` claim) from the validated token.
    4.  **Implement JIT Provisioning:** Check if a user with this ID exists in the database. If not, create a new `User` record.
    5.  Return the user object.
  - [ ] Any endpoint that uses this dependency will be protected and have access to the current user's data.

- **Task 2.4: Create Authentication Endpoints**
  - [ ] Create a `POST /api/auth/session` endpoint. This endpoint will receive the JWT from the frontend, and its only job is to set it in a secure, `HttpOnly` cookie.
  - [ ] Create a `POST /api/auth/logout` endpoint that clears this cookie.
  - [ ] Create a test endpoint `GET /api/users/me` that uses the `get_current_user` dependency and returns the current user's details.

---

### **Phase 3: Frontend Development (React `app/`)**

Build the user-facing part of the authentication flow.

- **Task 3.1: Implement Login Flow**

  - [ ] Create a "Login with Google" button.
  - [ ] On click, this button should redirect the user to the Neon Auth URL.

- **Task 3.2: Handle Authentication Callback**

  - [ ] Create a new page/route at `/auth/callback`.
  - [ ] This page's component should be responsible for parsing the JWT returned by Neon from the URL fragment (`#token=...`).
  - [ ] Once the token is parsed, it should immediately call the backend `POST /api/auth/session` endpoint to exchange the token for a secure session cookie.
  - [ ] After the session is established, redirect the user to their profile page or the homepage.

- **Task 3.3: Manage Application State**

  - [ ] Implement a global state management solution (e.g., React Context) to store the user's authentication status and profile information.
  - [ ] Create a "logout" function that calls the backend `POST /api/auth/logout` endpoint and clears the local user state.
  - [ ] Create a "hook" (e.g., `useAuth`) to easily access user data and auth status throughout the app.

- **Task 3.4: Protect Routes**
  - [ ] Implement a component or logic that prevents unauthenticated users from accessing protected pages (e.g., `/profile`, `/settings`).

---

### **Phase 4: Deployment and Finalization (Vercel)**

Configure the project for production deployment.

- **Task 4.1: Configure Vercel Project**

  - [ ] Create a new project on Vercel and connect it to your Git repository.
  - [ ] In the project settings, set the **Root Directory** to `app`.
  - [ ] Configure the build commands:
    - **Build Command:** `npm run build`
    - **Output Directory:** `dist`
    - **Install Command:** `npm install`
  - [ ] Vercel will automatically detect the `api` directory and deploy it as serverless functions.

- **Task 4.2: Configure Environment Variables**

  - [ ] In the Vercel project settings, add all necessary environment variables for the backend:
    - `DATABASE_URL` (from Task 1.1)
    - `NEON_JWKS_URI` (from Task 1.2)
    - `NEON_AUDIENCE` (from Task 1.2)
    - `NEON_ISSUER` (from Task 1.2)

- **Task 4.3: Deploy and Test**
  - [ ] Trigger a deployment on Vercel.
  - [ ] Update the Neon Auth provider settings with the final production Redirect URI (`https://<your-vercel-domain>/auth/callback`).
  - [ ] Perform a full end-to-end test of the login and logout flow on the production URL.

---
