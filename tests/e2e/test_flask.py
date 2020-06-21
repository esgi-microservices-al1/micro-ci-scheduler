import json
from datetime import datetime
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.testing = True
    with app.test_client() as client:
        yield client


testSchedule = dict(
    name="scheduleTest",
    project="projectTest",
    branch="master",
    interval=dict(unity='DAY', frequency=1),
    startDate=str(datetime.now())
)
updatedSchedule = dict(
    name="updatedScheduleTest",
    project="projectTest",
    branch="master",
    interval=dict(unity='DAY', frequency=1),
    startDate=str(datetime.now())
)


class TestAPI:
    def test_get_root(self):
        app.testing = True
        with app.test_client() as client:
            res = client.get('/')
            assert res.status_code == 200

    def test_post_get_schedule(self):
        app.testing = True
        with app.test_client() as client:
            post = client.post('/schedule', data=json.dumps(testSchedule), follow_redirects=True,
                               headers={'Content-Type': 'application/json'})
            assert post.status_code == 201
            res = client.get('/schedule')
            assert res.status_code == 200
            assert b'"name": "scheduleTest' in res.data

    def test_post_delete_schedule(self):
        app.testing = True
        with app.test_client() as client:
            post = client.post('/schedule', data=json.dumps(testSchedule), follow_redirects=True,
                               headers={'Content-Type': 'application/json'})
            data = json.loads(post.data)
            assert post.status_code == 201
            res = client.delete("/schedule/" + data['id'])
            assert res.status_code == 200

    def test_post_put_schedule(self):
        app.testing = True
        with app.test_client() as client:
            post = client.post('/schedule', data=json.dumps(testSchedule), follow_redirects=True,
                               headers={'Content-Type': 'application/json'})
            data = json.loads(post.data)
            assert post.status_code == 201
            res = client.put("/schedule/" + data['id'], data=json.dumps(updatedSchedule),
                             follow_redirects=True,
                             headers={'Content-Type': 'application/json'})
            assert res.status_code == 200

    def test_post_get_put_delete(self):
        app.testing = True
        with app.test_client() as client:
            post = client.post('/schedule', data=json.dumps(testSchedule), follow_redirects=True,
                               headers={'Content-Type': 'application/json'})
            data = json.loads(post.data)
            assert post.status_code == 201
            res = client.get('/schedule/' + data['id'])
            assert res.status_code == 200
            assert b'"name": "scheduleTest' in res.data
            res = client.put("/schedule/" + data['id'], data=json.dumps(updatedSchedule),
                             follow_redirects=True,
                             headers={'Content-Type': 'application/json'})
            assert res.status_code == 200
            res = client.delete("/schedule/" + data['id'])
            assert res.status_code == 200
