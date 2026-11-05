"""Модуль трекінгу транспортного хабу Фарми Інк.

Відновлено з чорної скриньки після пожежі 14.10. Частина коду могла
пошкодитися, гарантій ніхто не дає.

Формат журналу: ISO-час|ТИП|ключ=значення|ключ=значення...
Час завжди у форматі YYYY-MM-DDTHH:MM:SS.
"""
from dataclasses import dataclass, field


@dataclass
class Event:
    ts: str                      # '2026-10-14T00:41:30'
    kind: str                    # 'ACCESS', 'GATE', 'CARGO', ...
    fields: dict = field(default_factory=dict)


def load_events(path):
    """Читає журнал і повертає список подій. Биті рядки пропускає."""
    events = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ts, *rest = line.split("|")
            if len(ts) != 19 or "T" not in ts or not rest:
                continue
            kind, *pairs = rest
            try:
                fields = dict(pair.split("=", 1) for pair in pairs)
            except ValueError:
                continue
            events.append(Event(ts, kind, fields))
    return events


def _clock(ts):
    return ts.split("T")[1]


def events_between(events, start, end):
    """Події від start (включно) до end (не включно).

    start і end у форматі 'YYYY-MM-DDTHH:MM:SS'.
    """
    return [e for e in events if _clock(start) <= _clock(e.ts) < _clock(end)]


def gate_openings(events, gate, start, end):
    """Відкриття воріт gate за проміжок часу."""
    return [
        e for e in events_between(events, start, end)
        if e.kind == "GATE" and e.fields.get("gate") == str(gate)
        and e.fields.get("action") == "open"
    ]


def zone_access(events, zone, start, end):
    """Проходи в зону zone за проміжок часу."""
    return [
        e for e in events_between(events, start, end)
        if e.kind == "ACCESS" and e.fields.get("zone") == zone
    ]


def sensor_alerts(events, zone, sensor_type, start, end):
    """Показники датчика sensor_type у зоні zone за проміжок часу."""
    return [
        e for e in events_between(events, start, end)
        if e.kind == "SENSOR" and e.fields.get("zone") == zone
        and e.fields.get("type") == sensor_type
    ]


def batch_movements(events, batch):
    """Усі переміщення партії batch."""
    return [
        e for e in events
        if e.kind == "CARGO" and e.fields.get("batch") == batch
    ]


def alarm_enabled_at(events, moment):
    """Чи була сигналізація увімкнена в момент moment."""
    enabled = True
    for e in sorted(events, key=lambda e: e.ts):
        if e.ts > moment:
            break
        if e.kind == "ALARM" and e.fields.get("zone") == "all":
            enabled = e.fields.get("action") != "disable"
    return enabled
