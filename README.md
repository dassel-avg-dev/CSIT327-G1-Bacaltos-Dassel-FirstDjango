# CampusConnect

Full name: Dassel E. Bacaltos  
Section: G1

## Run locally

1. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`
5. Open `http://127.0.0.1:8000/`.

For deployment, set `DJANGO_SECRET_KEY` to a strong secret value before starting Django.