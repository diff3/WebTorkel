from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import random
import re
import sys
import time

from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "mysql+pymysql://root:pwd@192.168.11.81:3306/webtorkel"
LOG_PATH = Path(__file__).with_name("webtorkel_log.txt")

TABLE_COUNT = 226
OPTIONS_PER_TABLE = 6
PROP_COLUMNS = 38

Base = declarative_base()


class TableText(Base):
    __tablename__ = "table_text"

    table_id = Column(Integer, primary_key=True)
    label = Column(Text)
    title = Column(Text)
    option_1 = Column(Text)
    option_2 = Column(Text)
    option_3 = Column(Text)
    option_4 = Column(Text)
    option_5 = Column(Text)
    option_6 = Column(Text)


class TableOptionProperties(Base):
    __tablename__ = "table_option_properties"

    table_id = Column(Integer, primary_key=True)
    option_index = Column(Integer, primary_key=True)

    c0 = Column(Integer)
    c1 = Column(Integer)
    c2 = Column(Integer)
    c3 = Column(Integer)
    c4 = Column(Integer)
    c5 = Column(Integer)
    c6 = Column(Integer)
    c7 = Column(Integer)
    c8 = Column(Integer)
    c9 = Column(Integer)
    c10 = Column(Integer)
    c11 = Column(Integer)
    c12 = Column(Integer)
    c13 = Column(Integer)
    c14 = Column(Integer)
    c15 = Column(Integer)
    c16 = Column(Integer)
    c17 = Column(Integer)
    c18 = Column(Integer)
    c19 = Column(Integer)
    c20 = Column(Integer)
    c21 = Column(Integer)
    c22 = Column(Integer)
    c23 = Column(Integer)
    c24 = Column(Integer)
    c25 = Column(Integer)
    c26 = Column(Integer)
    c27 = Column(Integer)
    c28 = Column(Integer)
    c29 = Column(Integer)
    c30 = Column(Integer)
    c31 = Column(Integer)
    c32 = Column(Integer)
    c33 = Column(Integer)
    c34 = Column(Integer)
    c35 = Column(Integer)
    c36 = Column(Integer)
    c37 = Column(Integer)


class Opponent(Base):
    __tablename__ = "opponents"

    opponent_id = Column(Integer, primary_key=True)
    correction = Column(Integer)
    xp = Column(Integer)


class CombatText(Base):
    __tablename__ = "combat_texts"

    combat_id = Column(Integer, primary_key=True)
    text = Column(Text)


class InfoLine(Base):
    __tablename__ = "info_lines"

    line_index = Column(Integer, primary_key=True)
    text = Column(Text)


class Transcript:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._handle = path.open("w", encoding="utf-8")
        self._color_enabled = sys.stdout.isatty()

    def write_color(
        self,
        text: str,
        color: str,
        end: str = "\n",
        to_stdout: bool = True,
        to_file: bool = True,
    ) -> None:
        if to_stdout:
            if self._color_enabled:
                sys.stdout.write(f"{color}{text}\x1b[0m{end}")
            else:
                sys.stdout.write(text + end)
            sys.stdout.flush()
        if to_file:
            self._handle.write(text + end)
            self._handle.flush()

    def write(self, text: str, end: str = "\n", to_stdout: bool = True, to_file: bool = True) -> None:
        if to_stdout:
            sys.stdout.write(text + end)
            sys.stdout.flush()
        if to_file:
            self._handle.write(text + end)
            self._handle.flush()

    def close(self) -> None:
        self._handle.close()


@dataclass
class TableEntry:
    table_id: int
    label: str
    title: str
    options: List[str]


@dataclass
class TableView:
    table_id: int
    title: str
    display_title: str
    options: List[str]
    image_id: int
    is_random: bool
    missing: bool


@dataclass
class PlayerStatus:
    name: str
    xp: int
    gold: int
    form: str
    companions: int
    items: str


@dataclass
class RollOutcome:
    table_id: int
    title: str
    option: int
    choice_raw: str
    choice_log: str
    choice_image_id: int
    table_image_id: int
    combat_text: str
    status: PlayerStatus
    game_over: bool
    is_random: bool
    special: bool


class DataStore:
    def __init__(self, session):
        self.tables: Dict[int, TableEntry] = {}
        self.option_props: Dict[Tuple[int, int], List[int]] = {}
        self.opponents: Dict[int, Tuple[int, int]] = {}
        self.combat_texts: Dict[int, str] = {}
        self.info_lines: List[str] = []
        self._load(session)

    def _load(self, session) -> None:
        for row in session.query(TableText).order_by(TableText.table_id):
            options = [
                row.option_1 or "",
                row.option_2 or "",
                row.option_3 or "",
                row.option_4 or "",
                row.option_5 or "",
                row.option_6 or "",
            ]
            self.tables[row.table_id] = TableEntry(
                table_id=row.table_id,
                label=row.label or "",
                title=row.title or "",
                options=options,
            )

        for row in session.query(TableOptionProperties):
            self.option_props[(row.table_id, row.option_index)] = [
                row.c0,
                row.c1,
                row.c2,
                row.c3,
                row.c4,
                row.c5,
                row.c6,
                row.c7,
                row.c8,
                row.c9,
                row.c10,
                row.c11,
                row.c12,
                row.c13,
                row.c14,
                row.c15,
                row.c16,
                row.c17,
                row.c18,
                row.c19,
                row.c20,
                row.c21,
                row.c22,
                row.c23,
                row.c24,
                row.c25,
                row.c26,
                row.c27,
                row.c28,
                row.c29,
                row.c30,
                row.c31,
                row.c32,
                row.c33,
                row.c34,
                row.c35,
                row.c36,
                row.c37,
            ]

        for row in session.query(Opponent).order_by(Opponent.opponent_id):
            self.opponents[row.opponent_id] = (row.correction, row.xp)

        for row in session.query(CombatText).order_by(CombatText.combat_id):
            self.combat_texts[row.combat_id] = row.text or ""

        for row in session.query(InfoLine).order_by(InfoLine.line_index):
            self.info_lines.append(row.text or "")

    def get_table(self, table_id: int) -> Optional[TableEntry]:
        return self.tables.get(table_id)

    def get_props(self, table_id: int, option_index: int) -> List[int]:
        props = self.option_props.get((table_id, option_index))
        if props is None:
            return [0] * PROP_COLUMNS
        return props

    def set_prop(self, table_id: int, option_index: int, column: int, value: int) -> None:
        key = (table_id, option_index)
        if key not in self.option_props:
            self.option_props[key] = [0] * PROP_COLUMNS
        self.option_props[key][column] = value

    def set_option_text(self, table_id: int, option_index: int, text: str) -> None:
        entry = self.tables.get(table_id)
        if entry is None:
            return
        if 1 <= option_index <= OPTIONS_PER_TABLE:
            entry.options[option_index - 1] = text

    def clone(self) -> "DataStore":
        clone = object.__new__(DataStore)
        clone.tables = {
            key: TableEntry(
                table_id=value.table_id,
                label=value.label,
                title=value.title,
                options=list(value.options),
            )
            for key, value in self.tables.items()
        }
        clone.option_props = {key: list(values) for key, values in self.option_props.items()}
        clone.opponents = dict(self.opponents)
        clone.combat_texts = dict(self.combat_texts)
        clone.info_lines = list(self.info_lines)
        return clone


class Dice:
    def roll(self, count: int) -> int:
        sign = -1 if count < 0 else 1
        count = abs(count)
        total = 0
        for _ in range(count):
            total += random.randint(1, 6)
        return total * sign


@dataclass
class Player:
    xp: int = 0
    gold: int = 0
    form: int = 5
    gender: int = 1
    gurgle: int = 0
    weapon: int = 0
    weapon_pending: int = 0
    dead: bool = False
    item: int = 0
    item_pending: int = 0
    items_collected: str = ""
    companions: int = 0
    pirate_treasure: int = 0
    grandma_available: bool = True
    ak4: bool = False
    kingdom: int = 0
    name: str = "Torkel"
    last_joy: int = 0

    def kill(self) -> None:
        self.dead = True


FORM_NAMES = {
    1: "Blomma",
    2: "Groda",
    3: "Kobold",
    4: "Skelett",
    5: "Barbar",
    6: "Vampyr",
    7: "Varulv",
    8: "Alv",
}

FALLBACK_IMAGES = [image_id for image_id in range(2, 58) if image_id != 6]

RANDOM_ENCOUNTERS = {
    3: "F\u00e5r en grip i skallen! J\u00e4vlar! J\u00e4vlar! J\u00e4vlar!",
    4: "En\u00f6gd man.",
    5: "1d6 banditer.",
    6: "Flicka med godtyckligt utseende.",
    7: "1d6 svartalver.",
    8: "Kobolder.",
    9: "Person med spetsiga \u00f6ron.",
    10: "Flygande f\u00f6rem\u00e5l.",
    11: "1d6 \u00e4ventyrare.",
    12: "1d6 orcher.",
    13: "Vis man.",
    14: "Drake.",
    15: "Svart riddare.",
    16: "Beholder.",
    17: "Munter man i r\u00f6da kl\u00e4der.",
    18: "Balrog.",
}


class GameEngine:
    def __init__(self, data: DataStore):
        self.data = data
        self.dice = Dice()
        self.player = Player()

        self.current_table = 1
        self.star_table = 1
        self.next_table = 0
        self.next_next_table = 0
        self.previous_table = 0
        self.previous_option = 0

        self.modifier = 0
        self.glass_pin = False
        self.extra_life = False
        self.boyfriend = 0

        self.result_text = ""
        self.in_combat = False
        self.current_table_image_id = 1
        self.next_table_image_id = 0
        self.next_option_image_id = 0
        self.last_choice_image_id = 1
        self.round = 0
        self.required_tables = set(self.data.tables.keys())
        self.required_tables.add(226)
        self.visited_tables = set()
        self._mark_table_visited(self.current_table)

    def set_player_name(self, name: str) -> None:
        if name:
            self.player.name = name

    def get_intro_lines(self) -> List[str]:
        return list(self.data.info_lines)

    def is_dead(self) -> bool:
        return self.player.dead

    def get_round(self) -> int:
        return self.round

    def all_tables_visited(self) -> bool:
        return self.visited_tables.issuperset(self.required_tables)

    def get_table_view(self) -> TableView:
        if self.current_table == 226:
            options = [
                f"{key}. {RANDOM_ENCOUNTERS[key]}"
                for key in sorted(RANDOM_ENCOUNTERS.keys())
            ]
            return TableView(
                table_id=226,
                title="Random Encounter",
                display_title="Random Encounter",
                options=options,
                image_id=self.current_table_image_id,
                is_random=True,
                missing=False,
            )

        entry = self.data.get_table(self.current_table)
        if entry is None:
            title = f"Table {self.current_table} (missing)"
            return TableView(
                table_id=self.current_table,
                title=title,
                display_title=title,
                options=[],
                image_id=self.current_table_image_id,
                is_random=False,
                missing=True,
            )

        label = f"{entry.label} " if entry.label else ""
        return TableView(
            table_id=entry.table_id,
            title=entry.title,
            display_title=f"{label}{entry.title}",
            options=list(entry.options),
            image_id=self.current_table_image_id,
            is_random=False,
            missing=False,
        )

    def roll(self) -> RollOutcome:
        table_view = self.get_table_view()
        self.round += 1
        option = self._roll_option()
        self.previous_option = option
        choice_raw, choice_log, special = self._choice_text(table_view, option)
        self._apply_events(option)
        choice_image_id = self._consume_choice_image()
        combat_text = self.result_text if self.in_combat else ""
        self.in_combat = False
        self._advance_table()
        status = self.get_status()
        return RollOutcome(
            table_id=table_view.table_id,
            title=table_view.title,
            option=option,
            choice_raw=choice_raw,
            choice_log=choice_log,
            choice_image_id=choice_image_id,
            table_image_id=table_view.image_id,
            combat_text=combat_text,
            status=status,
            game_over=self.player.dead,
            is_random=table_view.is_random,
            special=special,
        )

    def get_status(self) -> PlayerStatus:
        form = FORM_NAMES.get(self.player.form, "Unknown")
        return PlayerStatus(
            name=self.player.name,
            xp=self.player.xp,
            gold=self.player.gold,
            form=form,
            companions=self.player.companions,
            items=self.player.items_collected,
        )

    def _consume_choice_image(self) -> int:
        if self.next_option_image_id != 0:
            image_id = self.next_option_image_id
            self.next_option_image_id = 0
            if image_id <= 0:
                image_id = 1
        else:
            image_id = self._random_fallback_image()
        self.last_choice_image_id = image_id
        return image_id

    def _choice_text(self, table_view: TableView, option: int) -> Tuple[str, str, bool]:
        if table_view.is_random:
            text = RANDOM_ENCOUNTERS.get(option, "Unknown encounter")
            return text, text, False
        if table_view.missing:
            raw = f"{option} (missing)"
            return raw, raw, True
        if 1 <= option <= OPTIONS_PER_TABLE:
            raw = table_view.options[option - 1]
            return raw, self._strip_option_prefix(raw), False
        return f"{option} (special)", "special", True

    def _roll_option(self) -> int:
        if self.current_table == 226:
            return self.dice.roll(3)

        option = self.dice.roll(1) + self.modifier
        if option < 1:
            option = 1
        if option > OPTIONS_PER_TABLE:
            option = OPTIONS_PER_TABLE
        if self.glass_pin and option == OPTIONS_PER_TABLE:
            self.player.xp += 88
        self.glass_pin = False
        return option

    def _strip_option_prefix(self, text: str) -> str:
        return re.sub(r"^\s*\d+\.\s*", "", text)

    def _apply_events(self, option: int) -> None:
        self.result_text = ""

        if self.current_table == 226:
            self._random_encounter(option)
            return

        if option == 8:
            self.player.gold += self.dice.roll(1) * 100
            self.next_table = 88
            self.star_table = 85
            self.modifier = 0
            return

        props = self.data.get_props(self.current_table, option)

        self._fix_next_table(props)
        self._fix_xp(props)
        self._fix_gold(props)

        if props[10] != 0:
            self.player.weapon_pending = props[10]
        if props[11] != 0:
            self._apply_weapon()

        if props[12] != 0:
            self.player.item_pending = props[12]
        if props[13] != 0:
            self._apply_item()

        if props[16] != 0 and self.previous_table == 7:
            self.player.xp += 1

        if props[17] != 0 and self.player.companions == 0:
            self._apply_companions(props[17])

        if props[19] != 0:
            self._change_gender()

        if props[20] != 0:
            self.player.pirate_treasure = self.dice.roll(2) * 100

        if props[21] != 0:
            self.next_table = 0
            self.next_next_table = 0
            self.star_table = 1

        if props[22] != 0:
            if self.previous_table in (58, 59, 219):
                self.next_table = -1

        if props[23] != 0:
            self._change_form(props[23])

        if props[24] != 0:
            if self.player.grandma_available:
                self.next_table = 0
            else:
                self.next_table = -1
            self.player.grandma_available = False

        if props[25] != 0 and self.player.item == 2:
            self.modifier = 1

        if props[26] != 0:
            self.glass_pin = True

        if props[27] != 0:
            if props[27] >= 0:
                self.next_table_image_id = props[27]
            else:
                self.next_option_image_id = -props[27]

        if props[28] != 0:
            self.player.ak4 = True

        if props[29] != 0:
            self.player.kingdom += 1
            if self.player.kingdom >= 2:
                self.player.name = "Kung Torkel"

        if props[30] != 0:
            self.player.xp += (self.dice.roll(1) + 6) * 6

        if props[31] != 0 and self.player.kingdom <= 1:
            self.player.name = "Sir Torkel"

        if props[32] != 0 and self.boyfriend == 161:
            self.player.name = "Josef"

        if props[33] != 0:
            self.boyfriend = props[33]

        if props[34] != 0:
            self.extra_life = True

        if props[35] != 0:
            self.player.last_joy = props[35]

        if props[36] != 0:
            self._pay_joy()

        if props[37] != 0:
            self.player.gurgle += 1

        if props[14] != 0:
            self._torkel_fights(props)

    def _fix_next_table(self, props: List[int]) -> None:
        if props[0] != 0:
            self.next_table = 226 if props[0] == 226 else props[0]
        else:
            self.next_table = 0

        if props[1] != 0:
            self.next_next_table = props[1]

        if props[2] != 0:
            self.star_table = props[2]

    def _fix_xp(self, props: List[int]) -> None:
        if props[3] != 0:
            if props[4] != 0:
                roll = self.dice.roll(props[3])
                result = roll + props[4]
                self.player.xp += result * props[5]
            else:
                roll = self.dice.roll(props[3])
                self.player.xp += roll * props[5]

        if props[4] != 0 and props[3] == 0:
            self.player.xp += props[4]

        if props[6] != 0:
            if props[6] == 1:
                self.player.xp //= 2
            if props[6] == 2:
                self.player.xp = 0

    def _fix_gold(self, props: List[int]) -> None:
        if props[7] != 0:
            roll = self.dice.roll(props[7])
            self.player.gold += roll * props[8]

        if props[8] != 0 and props[7] == 0:
            self.player.gold += props[8]

        if props[9] != 0:
            self.player.gold = 0

    def _apply_weapon(self) -> None:
        weapon = self.player.weapon_pending
        self.player.weapon = weapon
        self.player.weapon_pending = 0

        if weapon == 1:
            self.player.gold += 5
        elif weapon == 2:
            self.player.gold += 500
        elif weapon == 3:
            self.player.gold += 100
        elif weapon == 4:
            self.player.gold += 2000

    def _apply_item(self) -> None:
        item = self.player.item_pending
        self.player.item = item
        self.player.item_pending = 0

        items = {
            1: "Katapult, ",
            2: "Skattkarta, ",
            3: "Sv\u00e4rd med hack i eggen, ",
            4: "Sv\u00e4rd som nytt, ",
            5: "Guldpl\u00e4tterad champagnevisp, ",
            6: "Rockring i sk\u00e4r plast, ",
            7: "Guldring, ",
            8: "Teleporteringsring, ",
            9: "K\u00f6nsbytarring, ",
            10: "Tand, ",
            11: "",
            12: "B\u00e4rnsten, ",
            13: "P\u00e4rla, ",
            14: "Diamant, ",
            15: "Juvelbesatt guld\u00e4gg, ",
            16: "Tr\u00e4h\u00e4st, ",
            17: "Korg, ",
            18: "Rutig hatt, f\u00f6rstorningsglas, fiol, pipa, ",
            19: "Flaggst\u00e5ng, ",
            20: "Tv\u00e5l, ",
            21: "Galjonsfigur, ",
            22: "Nordpolen, ",
        }

        if item == 1:
            self.player.gold += 100
        if item == 3:
            self.player.gold += 5
        if item == 4:
            self.player.gold += 10
        if item == 5:
            self.player.gold += 100
        if item == 7:
            self.player.gold += self.dice.roll(2) * 100
        if item == 10:
            self.player.gold += 1
        if item == 11:
            stones = self.dice.roll(1)
            self.player.items_collected += f"{stones} st stenar, "
        if item == 12:
            self.player.gold += self.dice.roll(1) * 10
        if item == 13:
            self.player.gold += self.dice.roll(1) * 100
        if item == 14:
            self.player.gold += self.dice.roll(1) * 1000
        if item == 15:
            self.player.gold += 200

        if item in items and items[item]:
            self.player.items_collected += items[item]

    def _apply_companions(self, mode: int) -> None:
        if mode == 1:
            self.player.companions = self.dice.roll(1)
        elif mode == 2:
            self.player.companions = self.dice.roll(1) + 2

    def _change_gender(self) -> None:
        if self.player.gender in (1, 3, 5):
            self.data.set_prop(44, 6, 0, 6)
            self.data.set_option_text(44, 6, "Tycker att Gandalf har charmigt sk\u00e4gg.")

            self.data.set_prop(57, 1, 0, 6)
            self.data.set_prop(57, 1, 14, 0)
            self.data.set_option_text(57, 1, "Tr\u00e4ffar Sankte Per, f\u00f6rf\u00f6risk.")

            self.data.set_prop(69, 6, 0, 166)
            self.data.set_prop(69, 6, 4, -69)
            self.data.set_option_text(69, 6, "Hade f\u00f6r br\u00e5ttom att skydda sig.")

            self.data.set_prop(91, 6, 0, 0)
            self.data.set_option_text(91, 6, "Vomerar.")

            self.data.set_prop(108, 6, 0, -1)
            self.data.set_prop(108, 6, 4, 69)

            self.data.set_prop(169, 6, 0, 0)
            self.data.set_option_text(169, 6, "Skarvar i smyg p\u00e5 sin livstr\u00e5d.")

            self.data.set_prop(186, 5, 0, 0)
            self.data.set_prop(186, 5, 4, 60)
            self.data.set_option_text(186, 5, "F\u00e5r en silikoningjutning.")

            self.data.set_option_text(219, 6, "Tr\u00e4ffar incubus.")

            self.player.name = "Torkla"

            self.data.set_prop(4, 6, 33, 34)
            self.data.set_prop(25, 6, 33, 98)
            self.data.set_prop(44, 6, 33, 41)
            self.data.set_prop(219, 6, 33, 131)

            self.player.gender += 1
            return

        if self.player.gender in (2, 4, 6):
            self.data.set_prop(44, 6, 0, 23)
            self.data.set_option_text(44, 6, "St\u00f6ter ihop med Galadriel.")

            self.data.set_prop(57, 1, 0, 0)
            self.data.set_prop(57, 1, 14, 93)
            self.data.set_option_text(57, 1, "Tr\u00e4ffar Sankte Per, p\u00e5stridig.")

            self.data.set_prop(69, 6, 0, 69)
            self.data.set_prop(69, 6, 4, 69)
            self.data.set_option_text(69, 6, "Filckan salig, om igen.")

            self.data.set_prop(91, 6, 0, 130)
            self.data.set_option_text(91, 6, "Spyr. Urrrk...")

            self.data.set_prop(108, 6, 0, 26)
            self.data.set_prop(108, 6, 4, 0)

            self.data.set_prop(169, 6, 0, 69)
            self.data.set_option_text(169, 6, "Mutar till sig ett l\u00e4ngre liv.")

            self.data.set_prop(186, 5, 0, -1)
            self.data.set_prop(186, 5, 4, 0)
            self.data.set_option_text(186, 5, "Kastreras.")

            self.data.set_option_text(219, 6, "Tr\u00e4ffar succusbus.")

            self.player.name = "Torkel"

            self.data.set_prop(4, 6, 33, 98)
            self.data.set_prop(25, 6, 33, 140)
            self.data.set_prop(44, 6, 33, 0)
            self.data.set_prop(219, 6, 33, 58)

            self.player.gender += 1

    def _change_form(self, form: int) -> None:
        self.player.form = form

    def _pay_joy(self) -> None:
        if self.player.last_joy == 1:
            self.player.gold -= self.dice.roll(1)
        if self.player.last_joy == 2:
            self.player.gold -= self.dice.roll(3)
        if self.player.last_joy == 3:
            self.player.gold -= self.dice.roll(6)
        if self.player.last_joy == 4:
            self.player.gold -= self.dice.roll(2) * 10
        if self.player.last_joy == 5:
            self.player.gold -= self.dice.roll(3) * 20

    def _torkel_fights(self, props: List[int]) -> None:
        enemy = props[14]
        if props[15] == 0:
            count = 1
        else:
            count = self.dice.roll(props[15]) + props[18]
        self._combat_roll(count, enemy, self.player.form)

    def _combat_roll(self, enemy_count: int, enemy_id: int, form: int) -> None:
        if enemy_id == 160:
            enemy_id = self.boyfriend

        correction, xp_reward = self.data.opponents.get(enemy_id, (0, 0))

        count_mod = 0
        if enemy_count == 1:
            count_mod = 0
        elif 2 <= enemy_count <= 3:
            count_mod = -1
        elif 4 <= enemy_count <= 5:
            count_mod = -2
        elif 6 <= enemy_count <= 10:
            count_mod = -3
        elif 11 <= enemy_count <= 19:
            count_mod = -4
        elif enemy_count >= 20:
            count_mod = -5

        form_mod = 0
        if form == 8:
            form_mod = 0
        elif form == 1:
            form_mod = -9
        elif form == 2:
            form_mod = -7
        elif form == 3:
            form_mod = -2
        elif form == 4:
            form_mod = -1
        elif form == 5:
            form_mod = 0
        elif form == 6:
            form_mod = 3
        elif form == 7:
            form_mod = 1

        result = self.dice.roll(1) + count_mod + form_mod + correction
        if self.player.ak4 and enemy_id != 130:
            result = 2

        self._combat_result(result, enemy_id, enemy_count, xp_reward)

    def _combat_result(self, result: int, enemy_id: int, count: int, xp_reward: int) -> None:
        if result <= -10:
            self.player.kill()
            self.result_text = self.data.combat_texts.get(0, "")
        elif result == -9:
            self.player.kill()
            self.result_text = self.data.combat_texts.get(1, "")
        elif result == -8:
            self.next_table = 0
            self.star_table = 1
            self.result_text = self.data.combat_texts.get(2, "")
        elif result == -7:
            self.next_table = 0
            self.star_table = 221
            self.result_text = self.data.combat_texts.get(3, "")
        elif result == -6:
            self.next_table = 0
            self.next_next_table = 0
            self.star_table = 59
            self.result_text = self.data.combat_texts.get(4, "")
        elif result == -5:
            self.player.kill()
            self.result_text = self.data.combat_texts.get(5, "")
        elif result == -4:
            self.next_table = 111
            self.result_text = self.data.combat_texts.get(6, "")
        elif result == -3:
            self.next_table = 51
            self.result_text = self.data.combat_texts.get(7, "")
        elif result == -2:
            self.player.xp += -20
            self.next_table = 0
            self.star_table = 101
            self.result_text = self.data.combat_texts.get(8, "")
        elif result == -1:
            new_count = count - 1
            self.player.xp += xp_reward
            if count > 0:
                self._combat_roll(new_count, enemy_id, self.player.form)
            else:
                self.next_table = 0
            self.result_text = self.data.combat_texts.get(9, "")
        elif result == 0:
            self.next_table = 51
            self.result_text = self.data.combat_texts.get(10, "")
        elif result == 1:
            self.next_table = 224
            self.result_text = self.data.combat_texts.get(11, "")
        elif result == 2:
            self.next_table = 0
            self.player.xp += xp_reward
            self.result_text = self.data.combat_texts.get(12, "")
        elif result == 3:
            self.next_table = 0
            self.next_next_table = 13
            self.result_text = self.data.combat_texts.get(13, "")
        elif result == 4:
            self.next_table = 0
            self.player.xp += xp_reward
            self.result_text = self.data.combat_texts.get(14, "")
        elif result == 5:
            prize = xp_reward * 2
            self.player.xp += prize
            self.next_table = 0
            self.result_text = self.data.combat_texts.get(15, "")
        elif result == 6:
            prize = xp_reward // 2
            self.player.xp += prize
            self.next_table = 0
            self.result_text = self.data.combat_texts.get(16, "")
        elif result == 7:
            self.next_table = 0
            self.player.xp += xp_reward
            self.result_text = self.data.combat_texts.get(17, "")
        elif result == 8:
            self.next_table = 91
            self.player.xp += xp_reward
            self.result_text = self.data.combat_texts.get(18, "")
        elif result == 9:
            self.result_text = self.data.combat_texts.get(19, "")
            self._combat_roll(count, enemy_id, self.player.form)
        elif result >= 10:
            self.next_table = 0
            self.result_text = self.data.combat_texts.get(20, "")

        if result in (2, 4, 5, 6, 7, 8) or result >= 10:
            if self.player.pirate_treasure != 0:
                self.player.gold += self.player.pirate_treasure

        self.player.pirate_treasure = 0
        self.in_combat = True

    def _random_encounter(self, option: int) -> None:
        if option == 3:
            self.next_table = -1
        elif option == 4:
            self.next_table = 119
        elif option == 5:
            count = self.dice.roll(1)
            self._combat_roll(count, 8, self.player.form)
        elif option == 6:
            self.next_table = 6
        elif option == 7:
            count = self.dice.roll(1)
            self._combat_roll(count, 2, self.player.form)
        elif option == 8:
            self.next_table = 218
        elif option == 9:
            self.next_table = 20
        elif option == 10:
            self.next_table = 27
        elif option == 11:
            self.next_table = 9
        elif option == 12:
            count = self.dice.roll(1)
            self._combat_roll(count, 87, self.player.form)
        elif option == 13:
            self.next_table = 43
        elif option == 14:
            self.next_table = 35
        elif option == 15:
            self.next_table = 120
            self.next_table_image_id = 32
        elif option == 16:
            self.next_table = 31
            self.next_table_image_id = 10
        elif option == 17:
            self.next_table = 162
        elif option == 18:
            self._combat_roll(1, 7, self.player.form)

    def _advance_table(self) -> None:
        self.previous_table = self.current_table

        if self.extra_life and self.next_table == -1:
            self.next_table = 0
            self.extra_life = False

        if self.next_table != 0:
            self.current_table = self.next_table
        elif self.next_table == 0 and self.next_next_table == 0:
            self.current_table = self.star_table
        elif self.next_table == 0 and self.next_next_table != 0:
            self.current_table = self.next_next_table
            self.next_next_table = 0

        if self.next_table == -1:
            self.player.kill()

        self._update_table_image()
        self._mark_table_visited(self.current_table)
        self.next_table = 0

    def _update_table_image(self) -> None:
        image_id = self.next_table_image_id if self.next_table_image_id != 0 else 1
        if self.current_table == 0 and self.star_table == 50:
            image_id = 14
        if self.current_table == 0 and self.star_table == 86:
            image_id = 23
        if image_id <= 0:
            image_id = 1
        if image_id == 1:
            image_id = self._random_fallback_image()
        self.current_table_image_id = image_id
        self.next_table_image_id = 0

    def _random_fallback_image(self) -> int:
        if FALLBACK_IMAGES and random.random() < 0.33:
            return random.choice(FALLBACK_IMAGES)
        return 1

    def _mark_table_visited(self, table_id: int) -> None:
        if table_id >= 0:
            self.visited_tables.add(table_id)

class GameCLI:
    def __init__(self, engine: GameEngine, io: Transcript) -> None:
        self.engine = engine
        self.io = io

    def play(self) -> None:
        self._print_intro()
        name = self._prompt_line("Name [Torkel]: ").strip()
        self.engine.set_player_name(name)

        last_status: Optional[PlayerStatus] = self.engine.get_status()
        completion_message: Optional[str] = None

        while not self.engine.is_dead():
            view = self.engine.get_table_view()
            round_number = self.engine.get_round() + 1
            self.io.write(f"Round {round_number}", to_file=False)
            self._render_table(view)
            if not self._prompt_continue():
                self.io.write("Goodbye.", to_file=False)
                return

            outcome = self.engine.roll()
            self._render_choice(outcome)
            self._log_outcome(outcome)
            if last_status is not None:
                self._log_status_if_changed(last_status, outcome.status)
            self._finish_log_entry()

            if outcome.combat_text:
                self.io.write(f"Combat: {outcome.combat_text}", to_file=False)

            self._render_status(outcome.status)
            last_status = outcome.status
            if outcome.game_over:
                break
            if self.engine.all_tables_visited():
                completion_message = "All tables visited."
                break
            time.sleep(2)

        if last_status is None:
            last_status = self.engine.get_status()
        self._show_game_over(last_status, completion_message)

    def simulate(self, max_rounds: int = 10000) -> None:
        self.io.write("Simulating...", to_file=False)
        last_status = self.engine.get_status()
        completion_message: Optional[str] = None

        while (
            not self.engine.is_dead()
            and not self.engine.all_tables_visited()
            and self.engine.get_round() < max_rounds
        ):
            outcome = self.engine.roll()
            self._log_outcome(outcome)
            self._log_status_if_changed(last_status, outcome.status)
            self._finish_log_entry()
            last_status = outcome.status
            if outcome.game_over:
                break

        if self.engine.all_tables_visited():
            completion_message = "All tables visited."
        elif self.engine.get_round() >= max_rounds:
            completion_message = f"Max rounds reached ({max_rounds})."

        self._show_game_over(last_status, completion_message)

    def _print_intro(self) -> None:
        self.io.write("WebTorkel (text-only)", to_file=False)
        self.io.write("", to_file=False)
        for line in self.engine.get_intro_lines():
            if line.strip():
                self.io.write(line, to_file=False)
        self.io.write("", to_file=False)

    def _prompt_line(self, message: str) -> str:
        self.io.write(message, end="", to_file=False)
        reply = sys.stdin.readline()
        if not reply:
            return ""
        reply = reply.rstrip("\r\n")
        self.io.write(reply, to_stdout=False, to_file=False)
        return reply

    def _prompt_continue(self) -> bool:
        reply = self._prompt_line("Press Enter to roll, or 'q' to quit: ").strip().lower()
        self.io.write("", to_file=False)
        return reply != "q"

    def _render_table(self, view: TableView) -> None:
        self.io.write("", to_file=False)
        if view.missing:
            self.io.write_color(view.display_title, "\x1b[36m", to_file=False)
            return

        self.io.write_color(view.display_title, "\x1b[36m", to_file=False)
        for option in view.options:
            self.io.write(option, to_file=False)

    def _render_choice(self, outcome: RollOutcome) -> None:
        if outcome.is_random:
            self.io.write(f"Rolled {outcome.option}: ", end="", to_file=False)
        else:
            self.io.write("Rolled: ", end="", to_file=False)
        self.io.write_color(outcome.choice_raw, "\x1b[33m", to_file=False)

    def _log_outcome(self, outcome: RollOutcome) -> None:
        self.io.write_color(
            f"{outcome.table_id} {outcome.title}",
            "\x1b[36m",
            to_stdout=False,
            to_file=True,
        )
        if outcome.choice_log:
            self.io.write_color(
                outcome.choice_log,
                "\x1b[33m",
                to_stdout=False,
                to_file=True,
            )

    def _log_status_if_changed(self, previous: PlayerStatus, current: PlayerStatus) -> None:
        if (
            previous.xp == current.xp
            and previous.gold == current.gold
            and previous.form == current.form
            and previous.companions == current.companions
        ):
            return
        line = (
            f"Status: name={current.name} xp={current.xp} gold={current.gold} "
            f"form={current.form} companions={current.companions}"
        )
        self.io.write(line, to_stdout=False, to_file=True)

    def _finish_log_entry(self) -> None:
        self.io.write("", to_stdout=False, to_file=True)

    def _render_status(self, status: PlayerStatus) -> None:
        line = (
            f"Status: name={status.name} xp={status.xp} gold={status.gold} "
            f"form={status.form} companions={status.companions}"
        )
        self.io.write(line, to_file=False)
        if status.items:
            self.io.write(f"Items: {status.items}", to_file=False)

    def _show_game_over(self, status: PlayerStatus, reason: Optional[str]) -> None:
        self.io.write("", to_file=False)
        if reason:
            self.io.write(reason, to_file=False)
        self.io.write("Game over.", to_file=False)
        self.io.write(f"Final XP: {status.xp}", to_file=False)
        self.io.write(f"Final gold: {status.gold}", to_file=False)
        self.io.write(
            f"Status: name={status.name} xp={status.xp} gold={status.gold} "
            f"form={status.form} companions={status.companions}",
            to_stdout=False,
            to_file=True,
        )
        self.io.write("", to_stdout=False, to_file=True)
        self.io.write("Game over.", to_stdout=False, to_file=True)
        self.io.write(f"Final XP: {status.xp}", to_stdout=False, to_file=True)
        self.io.write(f"Final gold: {status.gold}", to_stdout=False, to_file=True)


def main() -> None:
    transcript = Transcript(LOG_PATH)
    try:
        engine = create_engine(DB_URL, future=True)
        Session = sessionmaker(bind=engine, future=True)
    except Exception as exc:
        transcript.write(f"Failed to configure database: {exc}", to_file=False)
        transcript.close()
        return

    try:
        with Session() as session:
            data = DataStore(session)
    except Exception as exc:
        transcript.write(f"Failed to load data: {exc}", to_file=False)
        transcript.close()
        return

    engine_instance = GameEngine(data)
    cli = GameCLI(engine_instance, transcript)
    try:
        simulate = "--simulate" in sys.argv
        max_rounds = 10000
        for arg_index, arg in enumerate(sys.argv[1:], start=1):
            if arg.startswith("--max-rounds="):
                value = arg.split("=", 1)[1]
                if value.isdigit():
                    max_rounds = int(value)
            elif arg == "--max-rounds" and arg_index + 1 < len(sys.argv):
                value = sys.argv[arg_index + 1]
                if value.isdigit():
                    max_rounds = int(value)

        if simulate:
            cli.simulate(max_rounds=max_rounds)
        else:
            cli.play()
    finally:
        transcript.close()


if __name__ == "__main__":
    main()
