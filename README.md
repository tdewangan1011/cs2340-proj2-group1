
## Local Setup

Clone the repository:

```bash
git clone REPOSITORY_URL
cd jobplatform
```

Create a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
.\venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up the database:

```bash
python manage.py migrate
```

Run the application:

```bash
python manage.py runserver
```

The application will be available at:

http://127.0.0.1:8000/

## Django Admin

To create an administrator account:

```bash
python manage.py createsuperuser
```

The Django administrator page is available at:

http://127.0.0.1:8000/admin/

## Database Changes

If you modify a Django model, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

Migration files should be committed to Git.

Do not commit `db.sqlite3`.

After pulling somebody else's model changes, run:

```bash
python manage.py migrate
```


