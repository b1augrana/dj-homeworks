import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course
from students.models import Student



@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(api_client, courses_factory):
    course = courses_factory(_quantity=1)
    response = api_client.get(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    
    
@pytest.mark.django_db
def test_get_courses_list(api_client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = api_client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['id'] == courses[i].id
        

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, courses_factory):
    courses = courses_factory(_quantity=20)
    response = api_client.get('/api/v1/courses/', {'id': courses[2].id})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == 3        
    
    
@pytest.mark.django_db
def test_filter_courses_by_name(api_client, courses_factory):
    courses = courses_factory(_quantity=20)
    response = api_client.get('/api/v1/courses/', {'name': courses[1].name})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[1].name    
    
    
@pytest.mark.django_db
def test_create_course(api_client):
    count = Course.objects.count()
    response = api_client.post('/api/v1/courses/', data={'name': 'course_1', 'students': []}, format='json')
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    
    
@pytest.mark.django_db
def test_update_course(api_client, courses_factory):
    course = courses_factory(_quantity=1)
    upd_course = 'updcs_course_name'
    result = api_client.get(f'/api/v1/courses/{course[0].id}/')
    assert result.status_code == 200
    assert result.json()['name'] == upd_course
    
    
@pytest.mark.django_db
def test_delete_course(api_client, courses_factory, count=5):
    courses = courses_factory(_quantity=count)
    response = api_client.delete(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1