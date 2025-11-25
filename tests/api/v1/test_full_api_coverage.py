import pytest
from fastapi.testclient import TestClient

# This test file performs comprehensive CRUD + validation + FK-violation tests
# for all API resources. It uses the existing `client` and `db_session` fixtures
# provided by `tests/conftest.py`.


def create_item(client, payload=None):
    payload = payload or {"item_name": "T Water", "unit": "bottle"}
    r = client.post("/api/v1/items/", json=payload)
    return r


def create_special_note(client, payload=None):
    payload = payload or {"notes_content_json": "{\"allergy\": \"none\"}"}
    r = client.post("/api/v1/special_notes/", json=payload)
    return r


def create_member(client, special_notes_id):
    r = client.post("/api/v1/members/", json={"special_notes_id": special_notes_id})
    return r


def create_community(client, member_id, password="TestPass123"):
    r = client.post(
        "/api/v1/communities/",
        json={"name": "C1", "member_id": member_id, "member_count": 5, "password": password},
    )
    return r


def create_request_content(client, items_id):
    r = client.post("/api/v1/request_content/", json={"items_id": items_id, "number": 10})
    return r


def create_shelter_info(client):
    r = client.post("/api/v1/shelter_info/", json={"latitude": 1.23, "longitude": 4.56})
    return r


def create_shelter(client, shelter_info_id, community_id):
    r = client.post("/api/v1/shelter/", json={"shelter_info": shelter_info_id, "community_id": community_id})
    return r


def create_support_request(client, community_id, request_content_id, status="pending"):
    r = client.post(
        "/api/v1/support_requests/",
        json={"community_id": community_id, "request_content_id": request_content_id, "status": status},
    )
    return r


### Items CRUD + validation
def test_items_crud_and_validation(client):
    # create
    r = create_item(client)
    assert r.status_code == 200
    item_id = r.json()["items_id"]

    # read
    r = client.get(f"/api/v1/items/{item_id}")
    assert r.status_code == 200

    # update
    r = client.put(f"/api/v1/items/{item_id}", json={"item_name": "Updated", "unit": "pc"})
    assert r.status_code == 200
    assert r.json()["item_name"] == "Updated"

    # delete
    r = client.delete(f"/api/v1/items/{item_id}")
    assert r.status_code == 200

    # not found
    r = client.get(f"/api/v1/items/{item_id}")
    assert r.status_code == 404

    # validation: missing required 'item_name' -> 422
    r = client.post("/api/v1/items/", json={"unit": "box"})
    assert r.status_code == 422


### SpecialNotes CRUD
def test_special_notes_crud(client):
    r = create_special_note(client)
    assert r.status_code == 200
    sn_id = r.json()["special_notes_id"]

    r = client.get(f"/api/v1/special_notes/{sn_id}")
    assert r.status_code == 200

    r = client.put(f"/api/v1/special_notes/{sn_id}", json={"notes_content_json": "{}"})
    assert r.status_code == 200

    r = client.delete(f"/api/v1/special_notes/{sn_id}")
    assert r.status_code == 200

    r = client.get(f"/api/v1/special_notes/{sn_id}")
    assert r.status_code == 404


### Members (depends on SpecialNotes)
def test_members_crud_and_fk(client, db_session):
    # invalid FK attempt first (isolated) -> expect 409
    r = client.post("/api/v1/members/", json={"special_notes_id": 9999})
    assert r.status_code == 409
    db_session.rollback()

    # then create a special note and a member with valid FK
    sn = create_special_note(client)
    sn_id = sn.json()["special_notes_id"]

    r = create_member(client, sn_id)
    assert r.status_code == 200
    member_id = r.json()["member_id"]

    # read/update/delete
    r = client.get(f"/api/v1/members/{member_id}")
    assert r.status_code == 200

    r = client.put(f"/api/v1/members/{member_id}", json={"special_notes_id": sn_id})
    assert r.status_code == 200

    r = client.delete(f"/api/v1/members/{member_id}")
    assert r.status_code == 200


### Communities (depends on Members)
def test_communities_crud_and_fk(client, db_session):
    # invalid FK first
    r = client.post(
        "/api/v1/communities/",
        json={"name": "X", "member_id": 9999, "password": "Invalid123"},
    )
    assert r.status_code == 409
    db_session.rollback()

    # create member and then create community with valid FK
    sn = create_special_note(client)
    member = create_member(client, sn.json()["special_notes_id"])
    member_id = member.json()["member_id"]

    r = create_community(client, member_id)
    assert r.status_code == 200
    community_id = r.json()["community_id"]

    # read/update/delete
    r = client.get(f"/api/v1/communities/{community_id}")
    assert r.status_code == 200

    r = client.put(f"/api/v1/communities/{community_id}", json={"name": "NewName", "member_id": member_id})
    assert r.status_code == 200

    r = client.delete(f"/api/v1/communities/{community_id}")
    assert r.status_code == 200


### RequestContent (depends on Items)
def test_request_content_crud_and_fk(client, db_session):
    # invalid FK first
    r = client.post("/api/v1/request_content/", json={"items_id": 9999, "number": 1})
    assert r.status_code == 409
    db_session.rollback()

    # then create item and request content with valid FK
    item = create_item(client)
    item_id = item.json()["items_id"]

    r = create_request_content(client, item_id)
    assert r.status_code == 200
    rc_id = r.json()["request_content_id"]

    # read/update/delete
    r = client.get(f"/api/v1/request_content/{rc_id}")
    assert r.status_code == 200

    r = client.put(f"/api/v1/request_content/{rc_id}", json={"items_id": item_id, "number": 5})
    assert r.status_code == 200

    r = client.delete(f"/api/v1/request_content/{rc_id}")
    assert r.status_code == 200


### ShelterInfo CRUD
def test_shelter_info_crud(client):
    r = create_shelter_info(client)
    assert r.status_code == 200
    si_id = r.json()["shelter_info"]

    r = client.get(f"/api/v1/shelter_info/{si_id}")
    assert r.status_code == 200

    r = client.put(f"/api/v1/shelter_info/{si_id}", json={"latitude": 9.9, "longitude": 8.8})
    assert r.status_code == 200

    r = client.delete(f"/api/v1/shelter_info/{si_id}")
    assert r.status_code == 200


### Shelter (depends on ShelterInfo and Communities)
def test_shelter_crud_and_fk(client, db_session):
    # invalid FK first
    r = client.post("/api/v1/shelter/", json={"shelter_info": 9999, "community_id": 9999})
    assert r.status_code == 409
    db_session.rollback()

    # create dependencies and then a valid shelter
    si = create_shelter_info(client)
    sn = create_special_note(client)
    member = create_member(client, sn.json()["special_notes_id"])
    comm = create_community(client, member.json()["member_id"])

    si_id = si.json()["shelter_info"]
    comm_id = comm.json()["community_id"]

    r = create_shelter(client, si_id, comm_id)
    assert r.status_code == 200
    s_id = r.json()["shelter_id"]

    r = client.get(f"/api/v1/shelter/{s_id}")
    assert r.status_code == 200

    r = client.put(f"/api/v1/shelter/{s_id}", json={"shelter_info": si_id, "community_id": comm_id})
    assert r.status_code == 200

    r = client.delete(f"/api/v1/shelter/{s_id}")
    assert r.status_code == 200


### SupportRequest (depends on Communities and RequestContent)
def test_support_request_crud_and_fk(client, db_session):
    # invalid FK first
    r = create_support_request(client, 9999, 9999, status="bad")
    assert r.status_code == 409
    db_session.rollback()

    # build dependencies
    item = create_item(client)
    rc = create_request_content(client, item.json()["items_id"])

    sn = create_special_note(client)
    member = create_member(client, sn.json()["special_notes_id"])
    comm = create_community(client, member.json()["member_id"])

    rc_id = rc.json()["request_content_id"]
    comm_id = comm.json()["community_id"]

    r = create_support_request(client, comm_id, rc_id)
    assert r.status_code == 200
    req_id = r.json()["request_id"]

    r = client.get(f"/api/v1/support_requests/{req_id}")
    assert r.status_code == 200

    r = client.put(f"/api/v1/support_requests/{req_id}", json={"community_id": comm_id, "request_content_id": rc_id, "status": "done"})
    assert r.status_code == 200

    r = client.delete(f"/api/v1/support_requests/{req_id}")
    assert r.status_code == 200
