Framework used: FastAPI

This backend exposes minimal endpoints to serve IndoBERT predictions and feedback.

Folder: `Backend/fastapi-app`

Windows setup

1) Create and activate venv (optional but recommended)

```powershell
cd "Backend/fastapi-app"
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
pip install -r "..\..\Model IndoBERT\requirements.txt"
```

3) Run server

```powershell
uvicorn app.main:app --reload --port 8000
```

The API will import and reuse code from `Model IndoBERT/src`.

Endpoints

- GET /health → { status: "ok" }
- POST /predict → Predict IndoBERT
	- body: { title?: string, text?: string, body?: string, log_feedback?: boolean, user_label?: 0|1 }
	- resp: { prediction: 0|1, prob_hoax: number, model_version: string }
- GET /feedback?limit=50 → latest feedback rows
- PATCH /feedback/{id} → update user_label
	- body: { user_label: 0|1 }
- GET /model/version → current model version

Notes

- Ensure model files exist at `Model IndoBERT/models/indobert/`.
- Feedback is stored at `Model IndoBERT/data/feedback/feedback.csv` managed by the shared module.