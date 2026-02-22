from datetime import date


def test_duplicate_log_returns_409(client):
    r = client.post("/habits", json={"name": "Study", "description": "", "frequency": "daily"})
    habit_id = r.json()["id"]

    payload = {"date": str(date.today()), "notes": "done"}
    r1 = client.post(f"/habits/{habit_id}/logs", json=payload)
    assert r1.status_code == 201

    r2 = client.post(f"/habits/{habit_id}/logs", json=payload)
    assert r2.status_code == 409


def test_streak_and_weekly_summary(client):
    r = client.post("/habits", json={"name": "Read", "description": "", "frequency": "daily"})
    habit_id = r.json()["id"]

    client.post(f"/habits/{habit_id}/logs", json={"date": str(date.today()), "notes": "done"})

    s = client.get(f"/habits/{habit_id}/streak")
    assert s.status_code == 200
    data = s.json()
    assert data["habit_id"] == habit_id

    # Use current ISO week
    y, w, _ = date.today().isocalendar()
    ws = client.get(f"/analytics/weekly-summary?week={y}-{w:02d}")
    assert ws.status_code == 200
