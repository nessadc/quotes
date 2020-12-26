import json


def test_create_quote(test_app_with_db):
    response = test_app_with_db.post(
        "/quotes/", data=json.dumps({"value": "foobar"})
    )

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
                "type": "value_error.missing",
            }
        ]
    }


def test_read_quote(test_app_with_db):
    response = test_app_with_db.post(
        "/quotes/", data=json.dumps({"value": "foobar"})
    )
    quote_id = response.json()["id"]

    response = test_app_with_db.get(f"/quotes/{quote_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == quote_id
    assert response_dict["value"] == "foobar"
    assert response_dict["created_at"]


def test_read_quote_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/quotes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quote not found"

    response = test_app_with_db.get("/quotes/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_read_all_quotes(test_app_with_db):
    response = test_app_with_db.post(
        "/quotes/", data=json.dumps({"value": "foobar"})
    )
    quote_id = response.json()["id"]

    response = test_app_with_db.get("/quotes/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == quote_id, response_list))) == 1


def test_remove_quote(test_app_with_db):
    response = test_app_with_db.post(
        "/quotes/", data=json.dumps({"value": "foobar"})
    )
    quote_id = response.json()["id"]

    response = test_app_with_db.delete(f"/quotes/{quote_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": quote_id, "value": "foobar"}


def test_remove_quote_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/quotes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quote not found"

    response = test_app_with_db.delete("/quotes/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_quote(test_app_with_db):
    response = test_app_with_db.post(
        "/quotes/", data=json.dumps({"value": "foobar"})
    )
    quote_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/quotes/{quote_id}/",
        data=json.dumps({"value": "fizzbuzz"})
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == quote_id
    assert response_dict["value"] == "fizzbuzz"
    assert response_dict["created_at"]


def test_update_quotes_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/quotes/999/",
        data=json.dumps({"value": "foobar", "quote": "updated!"})
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Quote not found"


def test_update_quotes_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
        "/quotes/", data=json.dumps({"value": "foobar"})
    )
    quote_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/quotes/{quote_id}/",
        data=json.dumps({})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "value"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_update_quotes_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(
        "/quotes/", data=json.dumps({"value": "foobar"})
    )
    quote_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/quotes/{quote_id}/",
        data=json.dumps({"vlue": "fizzbuzz"})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "value"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
