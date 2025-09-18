# 🌤️ Deploy Weather Agent – Flask + Gemini (LangChain) Google Cloud S

A simple **Flask web app** powered by **LangChain** + **Google Gemini API**.  
It includes a basic weather tool and uses Gemini (`gemini-2.5-flash`) to answer natural language queries.

---

## ✨ Features
- Web UI (Flask) to ask weather-related questions.  
- Integrated with **Google Gemini** via `langchain-google-genai`.  
- Deployable on:
  - ✅ Render (free tier)  
  - ✅ Google Cloud Run (scalable, serverless)

---

## 📂 Project Structure
```
weather-agent/
│── app.py          # Flask app
│── agent.py        # LangChain agent (Gemini + tools)
│── requirements.txt
│── render.yaml     # Render deployment config
```

---

## 🖥️ Local Development

1. Clone repo and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create `.env` file:
   ```ini
   GOOGLE_API_KEY=your_gemini_api_key
   GOOGLE_CLOUD_PROJECT=<PRJECT_ID>
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

3. Run locally:
   ```bash
   python app.py
   ```
   Open [http://localhost:8080](http://localhost:8080).

---

## 🚀 Deploy to Render

1. Push code to GitHub.  
2. Create new **Web Service** in Render.  
3. Use `render.yaml` for config.  
4. Set `GOOGLE_API_KEY` in **Render Dashboard → Environment Variables**.  
5. Deploy 🎉

---

<img src="./images/Screenshot from 2025-09-19 02-12-04.png" alt="Weather Agent" width="400"/>



## 🚀 Deploy to Google Cloud Run

### 1. Setup
```bash
gcloud auth login
gcloud config set project <PRJECT_ID>
gcloud services enable run.googleapis.com secretmanager.googleapis.com
```

### 2. Deploy with API key directly
```bash
gcloud run deploy weather-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="your_gemini_api_key"
```

### 3. Deploy with Secret Manager (secure option)
```bash
echo -n "your_gemini_api_key" | gcloud secrets create gemini_api_key --data-file=-
gcloud projects add-iam-policy-binding <PRJECT_ID> \
  --member="serviceAccount:$(gcloud projects describe <PRJECT_ID> --format='value(projectNumber)')-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud run deploy weather-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets GOOGLE_API_KEY=gemini_api_key:latest
```

---

## 🚀 Deploy to Google Cloud Run (Docker)

### 1. Create Artifact Registry repo
```bash
gcloud artifacts repositories create weather-docker \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repo for weather agent"
```

### 2. Authenticate Docker
```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 3. Build & Push
```bash
docker build -t us-central1-docker.pkg.dev/<PRJECT_ID>/weather-docker/weather-agent .
docker push us-central1-docker.pkg.dev/<PRJECT_ID>/weather-docker/weather-agent
```

### 4. Verify image exists
```bash
gcloud artifacts docker images list us-central1-docker.pkg.dev/<PRJECT_ID>/weather-docker
```

### 5. Deploy Cloud Run with Docker image
```bash
gcloud run deploy weather-agent \
  --image us-central1-docker.pkg.dev/<PRJECT_ID>/weather-docker/weather-agent \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets GOOGLE_API_KEY=gemini_api_key:latest
```

---

## 📜 Logs & Monitoring

### View logs
```bash
gcloud run services logs read weather-agent --region=us-central1
```

### Stream logs
```bash
gcloud run services logs tail weather-agent --region=us-central1
```

<img src="./images/Screenshot from 2025-09-19 02-12-56.png" alt="Weather Agent" width="400"/>

### Metrics
Go to **Google Cloud Console → Cloud Run → weather-agent → Metrics**  
See:
- Request count
- Latency
- Scaling activity
- Errors

---

## ⚡ Scaling

Cloud Run scales automatically:
- **Idle → 0 instances (no cost)**  
- **Load → multiple instances**  
- Control concurrency & max instances:

```bash
gcloud run deploy weather-agent \
  --image us-central1-docker.pkg.dev/<PRJECT_ID>/weather-docker/weather-agent \
  --region us-central1 \
  --allow-unauthenticated \
  --concurrency=20 \
  --max-instances=50 \
  --set-secrets GOOGLE_API_KEY=gemini_api_key:latest
```

---

✅ You now have a **scalable AI weather agent** deployed both on **Render** and **Google Cloud Run (Docker or Buildpacks)**.  
