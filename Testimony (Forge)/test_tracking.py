import pytest

from tracking_fixed import (
    load_events, events_between, gate_openings, 
    zone_access, sensor_alerts, batch_movements, alarm_enabled_at
)

@pytest.fixture(scope="module")
def events_list():
    return load_events("hub_log.txt")

# 1. Тест events_between

def test_module_can_find_events_across_midnight(events_list):
    """
    Перевіримо, чи вміє модуль шукати події, 
    якщо проміжок часу захоплює перехід через 00:00.
    Візьмемо час з 23:00 13-го жовтня до 01:00 14-го жовтня.
    """
    events_found = events_between(events_list, "2026-10-13T23:00:00", "2026-10-14T01:00:00")
    
    # Якщо модуль працює правильно, він має повернути не порожній список.
    assert len(events_found) > 0, "ПОМИЛКА: Модуль не бачить подій після опівночі!"

# 2. Перевірка свідчень

def test_dispatcher_testimony(events_list):
    """Диспетчер: «Партію 4-А відвантажили через ворота 1 о 22:10, за графіком.»"""
    movements_list = batch_movements(events_list, "4-А")
    
    assert len(movements_list) == 1
    assert movements_list[0].fields.get("gate") == "1"
    
    # чи це взагалі відбулося в діапазоні 22-ї години, якщо так то це підтверджує слова диспетчера
    assert "2026-10-13T22:" in movements_list[0].ts 

def test_guard_testimony(events_list):
    """
    Охоронець: «Після 23:00 у сектор С ніхто не заходив.»
    Очікуємо 0 проходів.
    """
    access_events_list = zone_access(events_list, "C", "2026-10-13T23:00:00", "2026-10-14T05:00:00")
    
    # Якщо він каже правду, список має бути порожнім
    assert len(access_events_list) == 0, f"Охоронець збрехав! Знайдено проходи: {access_events_list}"

def test_engineer_testimony(events_list):
    """Інженер: «Датчик диму в секторі С спрацював о 02:47.»"""
    alerts_list = sensor_alerts(events_list, "C", "smoke", "2026-10-14T02:47:00", "2026-10-14T02:48:00")
    
    assert len(alerts_list) == 1


# 3. Перевірка стану сигналізації у момент пожежі

@pytest.mark.parametrize("target_moment, expected_state", [
    ("2026-10-13T20:00:00", True),
    ("2026-10-14T02:47:00", False)
])
def test_alarm_status_at_fire(events_list, target_moment, expected_state):
    """Перевірка, чи працювала сигналізація в момент пожежі."""
    assert alarm_enabled_at(events_list, target_moment) == expected_state