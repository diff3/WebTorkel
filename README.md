# WebTorkel

Text-only adventure game with a CLI and a Flask web UI. Data is loaded from a
MariaDB database using SQLAlchemy ORM.

## Requirements

- Python 3.10+ recommended
- MariaDB with the `webtorkel` database and tables from `webtorkel_sql/schema.sql`
- Python packages:
  - `flask`
  - `sqlalchemy`
  - `pymysql`

You can install packages with:

```bash
python -m pip install flask sqlalchemy pymysql
```

## Database config

The DB connection is defined in `webtorkel.py`:

```python
DB_URL = "mysql+pymysql://root:pwd@192.168.11.81:3306/webtorkel"
```

Edit that string if your database host, user, or password is different.

## CLI usage

Run the interactive CLI:

```bash
python webtorkel.py
```

Fast simulation (no input, stops when all tables visited or max rounds):

```bash
python webtorkel.py --simulate
python webtorkel.py --simulate --max-rounds 5000
```

The CLI writes a log to `webtorkel_log.txt`.

## Flask web UI

Start the web server:

```bash
python webtorkel_web.py
```

Open: `http://localhost:5000/`

Optional: set a secret key for sessions:

```bash
export WEBTORKEL_SECRET="change-me"
```

### Web flow

- Start screen: enter a name once, then start the game.
- Table page: shows the current table, options, and the scene image.
- Result page: shows the rolled option and the image.
- Game over page: shows final status and totals.

## Project files

- `webtorkel.py` - game engine + CLI
- `webtorkel_web.py` - Flask app
- `templates/` - HTML templates
- `static/` - CSS and images
- `webtorkel_sql/` - schema and import SQL
