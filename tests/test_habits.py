def test_create_and_list_habits(client):
    r = client.post("/habits", json={"name": "Gym", "description": "Weights", "frequency": "daily"})
    assert r.status_code == 201
    habit = r.json()
    assert habit["name"] == "Gym"

    r2 = client.get("/habits")
    assert r2.status_code == 200
    habits = r2.json()
    assert any(h["name"] == "Gym" for h in habits)
