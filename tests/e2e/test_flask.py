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


class TestAPI():
    # @pytest.fixture
    # def create_app(self):
    #     application = app.create_app()
    #     application.config['TESTING'] = True
    #     application.config['DEBUG'] = False
    #     # application.config['DATABASE'] = tempfile.mkstemp()
    #     application.testing = True

    def test_get_root(self):
        app.testing = True
        with app.test_client() as client:
            res = client.get('/')
            assert res.status_code == 200

    def test_post_get_schedule(self):
        with app.test_client() as client:
            post = client.post('/schedule', data=json.dumps(dict(
                name="scheduleTest",
                project="projectTest",
                branch="master",
                interval=dict(unity='DAY', frequency=1),
                startDate=str(datetime.now())
            )), follow_redirects=True, headers={'Content-Type': 'application/json'})
            print(post.data)
            assert post.status_code == 201
            res = client.get('/schedule/')
            assert res.status_code == 200
            assert b'"name": "scheduleTest' in res.data
