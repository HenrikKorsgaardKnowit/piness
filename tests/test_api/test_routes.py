"""Tests for API routes."""

import pytest
from fastapi.testclient import TestClient

from piness.api.server import create_app
from piness.store import EventBuffer, MessageBuffer


@pytest.fixture
def client():
    app = create_app(
        event_buffer=EventBuffer(maxlen=10),
        message_buffer=MessageBuffer(maxlen=10),
    )
    return TestClient(app)


class TestPostEvents:
    def test_post_event(self, client):
        resp = client.post("/events", json={"value": 42.0, "label": "temp"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "ok"
        assert data["events_count"] == 1

    def test_post_event_minimal(self, client):
        resp = client.post("/events", json={"value": 1.0})
        assert resp.status_code == 201

    def test_post_event_missing_value(self, client):
        resp = client.post("/events", json={"label": "oops"})
        assert resp.status_code == 422

    def test_multiple_events_increment_count(self, client):
        client.post("/events", json={"value": 1.0})
        client.post("/events", json={"value": 2.0})
        resp = client.post("/events", json={"value": 3.0})
        assert resp.json()["events_count"] == 3


class TestPostMessages:
    def test_post_message(self, client):
        resp = client.post("/messages", json={"text": "hello", "source": "test"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "ok"
        assert data["messages_count"] == 1

    def test_post_message_minimal(self, client):
        resp = client.post("/messages", json={"text": "hi"})
        assert resp.status_code == 201

    def test_post_message_missing_text(self, client):
        resp = client.post("/messages", json={"source": "oops"})
        assert resp.status_code == 422


class TestGetStatus:
    def test_status_empty(self, client):
        resp = client.get("/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["events_count"] == 0
        assert data["messages_count"] == 0

    def test_status_after_data(self, client):
        client.post("/events", json={"value": 1.0})
        client.post("/messages", json={"text": "hi"})
        resp = client.get("/status")
        data = resp.json()
        assert data["events_count"] == 1
        assert data["messages_count"] == 1
