# 📊 HH.ru Vacancies in an Analytical Dashboard

**Project structure:**

```
BONUS/
├── frontend/               # Frontend UI
│   ├── Dockerfile          # Nginx container config
│   ├── index.html          # Web interface with charts
│   ├── nginx.conf          # Proxy settings for API
│   └── styles.css          # UI styling
│
├── server/                 # Backend server
│   ├── app.py              # Main Flask API server
│   ├── bonus.py            # HH.ru data scraper
│   ├── data.json           # Cached vacancy data
│   ├── Dockerfile          # Python container config
│   ├── requirements.txt    # Python dependencies
│   └── analyst_stats.png   # Example visualization
│
└── docker-compose.yml      # Container orchestration
```

---

## 🧠 Workflow

### 1. Data Collection (`bonus.py`)
- Parses vacancies via the HH.ru API  
- Filters by the keyword **"Analyst"**  
- Saves structured data to `data.json`  

### 2. Flask API Server (`app.py`)
- REST API available at `/api/stats`  
- CORS enabled for frontend integration  
- Serves normalized skill and job data  

### 3. Dockerization
- `frontend/Dockerfile`: Nginx + static files  
- `server/Dockerfile`: Python + requirements  
- Shared network for container communication  

### 4. User Interface
- Interactive charts using **Chart.js**  
- Responsive layout with live updates  
- Served via local Nginx container  

---

## 🚀 Quickstart

```bash
# 1. Build and run the app
docker-compose up --build

# 2. Stop all containers
docker-compose down

# 3. Open in browser
http://localhost
```
