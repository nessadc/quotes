import json


def test_create_quote(test_app_with_db):
    response = test_app_with_db.post("/quotes/", data=json.dumps({"value": "foobar"}))

    assert response.status_code == 201
    assert response.json()["value"] == "foobar"


def test_create_quotes_invalid_json(test_app):
    response = test_app.post("/quotes/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "value"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_read_quote(test_app_with_db):
    response = test_app_with_db.post("/quotes/", data=json.dumps({"value": "foobar"}))
    quote_id = response.json()["id"]

    response = test_app_with_db.get(f"/quotes/{quote_id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == quote_id
    assert response_dict["value"] == "foobar"
    assert response_dict["created_at"]


def test_read_quote_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/quotes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quote not found"


def test_read_all_quotes(test_app_with_db):
    response = test_app_with_db.post("/quotes/", data=json.dumps({"value": "foobar"}))
    quote_id = response.json()["id"]

    response = test_app_with_db.get("/quotes/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == quote_id, response_list))) == 1
