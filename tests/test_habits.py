def test_create_and_list_habits(client):
    r = client.post("/api/habits", json={"name": "Gym", "description": "Weights", "frequency": "daily"})
    assert r.status_code == 201
    habit = r.json()
    assert habit["name"] == "Gym"

    r2 = client.get("/api/habits")
    assert r2.status_code == 200
    habits = r2.json()
    assert any(h["name"] == "Gym" for h in habits)

def test_patch_missing_habit_returns_404(client):
    r = client.patch("/api/habits/999999", json={"description": "x"})
    assert r.status_code == 404

def test_delete_habit_then_get_returns_404(client):
    r = client.post("/api/habits", json={"name": "Temp", "description": "", "frequency": "daily"})
    hid = r.json()["id"]

    d = client.delete(f"/api/habits/{hid}")
    assert d.status_code in (204, 200)

    g = client.get(f"/api/habits/{hid}")
    assert g.status_code == 404