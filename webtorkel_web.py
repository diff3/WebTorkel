from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import os
import uuid

from flask import Flask, redirect, render_template, request, session, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from webtorkel import DB_URL, DataStore, GameEngine, PlayerStatus, RollOutcome

APP_ROOT = Path(__file__).resolve().parent
IMAGE_DIR = APP_ROOT / "static" / "images"

AVAILABLE_IMAGES = {
    int(path.stem)
    for path in IMAGE_DIR.glob("*.jpg")
    if path.stem.isdigit()
}

BASE_DATA: Optional[DataStore] = None
DATA_ERROR: Optional[str] = None
DB_SESSION = None

GAMES: Dict[str, GameEngine] = {}
LAST_OUTCOME: Dict[str, RollOutcome] = {}
GAME_LOGS: Dict[str, List[str]] = {}
LAST_STATUS: Dict[str, PlayerStatus] = {}
GAME_OVER_LOGGED: set[str] = set()


def load_base_data() -> Optional[DataStore]:
    global BASE_DATA, DATA_ERROR, DB_SESSION
    if BASE_DATA is not None or DATA_ERROR is not None:
        return BASE_DATA

    try:
        engine = create_engine(DB_URL, future=True, pool_pre_ping=True)
        DB_SESSION = sessionmaker(bind=engine, future=True)
        with DB_SESSION() as session:
            BASE_DATA = DataStore(session)
    except Exception as exc:
        DATA_ERROR = str(exc)
        BASE_DATA = None

    return BASE_DATA


def get_game_id() -> str:
    game_id = session.get("game_id")
    if not game_id:
        game_id = uuid.uuid4().hex
        session["game_id"] = game_id
    return game_id


def get_game() -> Optional[GameEngine]:
    data = load_base_data()
    if data is None:
        return None

    game_id = get_game_id()
    game = GAMES.get(game_id)
    if game is None:
        game = GameEngine(data.clone())
        GAMES[game_id] = game
        GAME_LOGS[game_id] = []
        LAST_STATUS[game_id] = game.get_status()
        GAME_OVER_LOGGED.discard(game_id)
    return game


def _status_line(status) -> str:
    return (
        f"Status: name={status.name} xp={status.xp} gold={status.gold} "
        f"form={status.form} companions={status.companions}"
    )


def _append_log_line(game_id: str, line: str) -> None:
    GAME_LOGS.setdefault(game_id, []).append(line)


def _log_outcome(game_id: str, outcome: RollOutcome) -> None:
    _append_log_line(game_id, f"{outcome.table_id} {outcome.title}")
    choice_text = outcome.choice_log or outcome.choice_raw
    if choice_text:
        _append_log_line(game_id, choice_text)

    previous = LAST_STATUS.get(game_id)
    if previous and (
        previous.xp != outcome.status.xp
        or previous.gold != outcome.status.gold
        or previous.form != outcome.status.form
        or previous.companions != outcome.status.companions
    ):
        _append_log_line(game_id, _status_line(outcome.status))
    LAST_STATUS[game_id] = outcome.status
    _append_log_line(game_id, "")


def _log_game_over(game_id: str, status) -> None:
    if game_id in GAME_OVER_LOGGED:
        return
    _append_log_line(game_id, _status_line(status))
    _append_log_line(game_id, "")
    _append_log_line(game_id, "Game over.")
    _append_log_line(game_id, f"Final XP: {status.xp}")
    _append_log_line(game_id, f"Final gold: {status.gold}")
    GAME_OVER_LOGGED.add(game_id)


def image_url(image_id: int) -> Optional[str]:
    if image_id in AVAILABLE_IMAGES:
        return url_for("static", filename=f"images/{image_id}.jpg")
    if 1 in AVAILABLE_IMAGES:
        return url_for("static", filename="images/1.jpg")
    return None


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("WEBTORKEL_SECRET", "dev-secret")

    @app.route("/")
    def index():
        return redirect(url_for("table"))

    @app.route("/table")
    def table():
        game = get_game()
        if game is None:
            return render_template("error.html", message=DATA_ERROR or "Unknown error")

        if game.is_dead():
            return redirect(url_for("game_over"))

        view = game.get_table_view()
        status = game.get_status()

        intro_lines = None
        if not session.get("intro_shown"):
            intro_lines = game.get_intro_lines()
            session["intro_shown"] = True

        return render_template(
            "table.html",
            view=view,
            status=status,
            intro_lines=intro_lines,
            image_url=image_url(view.image_id),
            name_locked=session.get("name_set", False),
        )

    @app.post("/set-name")
    def set_name():
        game = get_game()
        if game is None:
            return render_template("error.html", message=DATA_ERROR or "Unknown error")

        if not session.get("name_set"):
            name = request.form.get("name", "").strip()
            game.set_player_name(name)
            session["name_set"] = True
        return redirect(url_for("table"))

    @app.post("/roll")
    def roll():
        game = get_game()
        if game is None:
            return render_template("error.html", message=DATA_ERROR or "Unknown error")
        if game.is_dead():
            return redirect(url_for("table"))

        outcome = game.roll()
        game_id = get_game_id()
        LAST_OUTCOME[game_id] = outcome
        _log_outcome(game_id, outcome)
        if outcome.game_over:
            _log_game_over(game_id, outcome.status)
        return redirect(url_for("result"))

    @app.route("/result")
    def result():
        game_id = get_game_id()
        outcome = LAST_OUTCOME.get(game_id)
        if outcome is None:
            return redirect(url_for("table"))
        if outcome.game_over:
            return redirect(url_for("game_over"))

        return render_template(
            "result.html",
            outcome=outcome,
            status=outcome.status,
            image_url=image_url(outcome.choice_image_id),
            choice_text=outcome.choice_log or outcome.choice_raw,
        )

    @app.route("/game-over")
    def game_over():
        game = get_game()
        if game is None:
            return render_template("error.html", message=DATA_ERROR or "Unknown error")
        if not game.is_dead():
            return redirect(url_for("table"))

        game_id = get_game_id()
        outcome = LAST_OUTCOME.get(game_id)
        status = game.get_status()
        _log_game_over(game_id, status)
        log_text = "\n".join(GAME_LOGS.get(game_id, []))
        return render_template(
            "game_over.html",
            status=status,
            outcome=outcome,
            log_text=log_text,
        )

    @app.post("/reset")
    def reset():
        data = load_base_data()
        if data is None:
            return render_template("error.html", message=DATA_ERROR or "Unknown error")

        game_id = get_game_id()
        GAMES[game_id] = GameEngine(data.clone())
        LAST_OUTCOME.pop(game_id, None)
        GAME_LOGS.pop(game_id, None)
        LAST_STATUS.pop(game_id, None)
        GAME_OVER_LOGGED.discard(game_id)
        session.pop("intro_shown", None)
        session.pop("name_set", None)
        return redirect(url_for("table"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
