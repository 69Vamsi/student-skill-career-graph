# Student Skill & Career Graph — Backend

FastAPI backend for the Student Skill & Career Graph. This phase sets up the API foundation only. CognoDB is **not** connected yet.

## Requirements

- Python 3.11

## 1. Create and activate the virtual environment

From the `backend` directory:

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

After activation, your prompt should show `(.venv)`.

## 2. Install dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

## 3. Environment variables

Copy the example file and edit it if needed:

```bash
copy .env.example .env
```

On macOS / Linux:

```bash
cp .env.example .env
```

Leave `COGNODB_*` values empty for now. Do not put real passwords in git.

## 4. Start the FastAPI server

From the `backend` directory, with `.venv` activated:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

## 5. Test the health endpoint

In a new terminal:

```bash
curl http://127.0.0.1:8000/health
```

**Windows PowerShell**

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected JSON:

```json
{
  "status": "ok",
  "message": "API is running"
}
```

You can also open http://127.0.0.1:8000/health in a browser.

## Project layout

```text
backend/
  app/
    main.py          # FastAPI entry point
    config.py        # Environment-variable settings
    errors.py        # JSON error handlers
    routers/
      health.py      # GET /health
  requirements.txt
  .env.example
```
