from datetime import date, timedelta


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

def test_weekly_summary_invalid_week_format_returns_400(client):
    r = client.get("/analytics/weekly-summary?week=banana")
    assert r.status_code == 400


def test_weekly_summary_invalid_week_number_returns_400(client):
    # ISO weeks don't go to 99
    y = date.today().year
    r = client.get(f"/analytics/weekly-summary?week={y}-99")
    assert r.status_code == 400


def test_delete_missing_log_returns_404(client):
    r = client.post("/habits", json={"name": "Walk", "description": "", "frequency": "daily"})
    habit_id = r.json()["id"]

    # log_id that doesn't exist
    resp = client.delete(f"/habits/{habit_id}/logs/999999")
    assert resp.status_code == 404


def test_create_log_for_missing_habit_returns_404(client):
    payload = {"date": str(date.today()), "notes": "done"}
    resp = client.post("/habits/999999/logs", json=payload)
    assert resp.status_code == 404

def test_weekly_summary_missing_week_param_returns_422(client):
    r = client.get("/analytics/weekly-summary")
    assert r.status_code == 422