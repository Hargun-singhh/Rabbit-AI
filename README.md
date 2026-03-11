# AI Data Analysis and Reporting System

This is a full-stack, cloud-native application that allows users to upload structured data files (CSV, XLSX), analyzes the data on the backend, generates an AI-powered summary using Google Gemini, and emails the final report.

It demonstrates production-grade architecture, microservices containerization with Docker, and CI/CD pipelines via GitHub Actions.

## Project Structure
- `frontend/`: Next.js 14 Web Application (React, TailwindCSS)
- `backend/`: FastAPI Python Application (Pandas, yagmail, GenerativeAI)
- `docker-compose.yml`: For running the entire stack locally.
- `.github/workflows/`: Automated CI testing and continuous deployment to Vercel and Render.

---

## 🚀 How to Run Locally with Docker

Prerequisites: [Docker](https://docs.docker.com/get-docker/) installed.

1. **Clone the repository.**
2. **Create the environment file**
   Copy the example environment into a `.env` file at the root or within the backend directory.
   ```bash
   cp backend/.env.example backend/.env
   ```
   Fill in your `GEMINI_API_KEY` and Email credentials if you want to test AI & Email functionality locally.

3. **Start the containers**
   Run the following command in the root of the repository:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - **Frontend UI:** [http://localhost:3000](http://localhost:3000)
   - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Backend Health Check:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 🛳 Deployment Documentation

Both services are configured to deploy automatically via GitHub Actions whenever code is merged to the `main` branch.

### 1. Deploying the Backend to Render
1. Go to [Render.com](https://render.com) and create an account.
2. Click **New +** and select **Web Service**.
3. Choose **Build and deploy from a Git repository** and connect this GitHub repo.
4. Set the following configurations:
   - **Name:** e.g., `ai-data-analysis-api`
   - **Root Directory:** `backend`
   - **Environment:** `Docker` (Render automatically detects your Dockerfile)
5. Under **Environment Variables**, add:
   - `GEMINI_API_KEY` = your_gemini_api_key
   - `ENABLE_AI_SUMMARY` = true
   - `EMAIL_SENDER` = your_email@gmail.com
   - `EMAIL_PASSWORD` = your_app_password
   - `CORS_ORIGINS` = `["https://your-vercel-frontend-url.vercel.app"]`
6. Click **Create Web Service**.
7. **CI/CD Hook:** Copy the "Deploy Hook" URL from Render Settings -> Deploy Hook, and add it to your GitHub Repository Secrets as `RENDER_DEPLOY_HOOK`. The GitHub action will trigger this hook upon successful tests.

### 2. Deploying the Frontend to Vercel
1. Go to [Vercel.com](https://vercel.com) and create an account.
2. Click **Add New Project** and import this GitHub repository.
3. The framework preset should auto-detect **Next.js**.
4. Set the **Root Directory** to `frontend`.
5. Open **Environment Variables** and add:
   - `NEXT_PUBLIC_API_URL`: `<your-render-backend-url>/api/v1`
6. Click **Deploy**. Vercel handles the build and deployment automatically. 
7. **Note:** Ensure your Vercel URL is added to the `CORS_ORIGINS` in your Render backend environment variables to allow API access.

---

## 🛡 Security Practices Implemented
- **Input Validation:** Files are strictly validated by MIME type and extension (`.csv`, `.xlsx`). Pydantic enforces schema validation.
- **Upload Limits:** Enforced via environment variables (default 10MB) to prevent memory exhaustion and DoS.
- **Secrets Management:** No API keys are in source code; all pass through `pydantic-settings` via dot-env.
- **Data Privacy:** Only high-level mathematical aggregations and column names are sent to the AI API; raw row data never leaves the server.
- **CORS Mitigation:** FastAPi CORS middleware restrict origins.

## 📡 API Documentation
The API documentation is interactive and available via Swagger UI. Once deployed locally or on Render, visit `/docs`.

**Key Endpoints:**
- `GET /api/v1/health`: Checks service status.
- `POST /api/v1/analyze`: Expects `multipart/form-data` with `file` (CSV/XLSX) and an optional `email` field. Returns a structured JSON summary and dispatches email.
