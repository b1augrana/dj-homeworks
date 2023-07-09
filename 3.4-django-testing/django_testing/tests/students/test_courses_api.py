import pytest
from django.contrib.auth.models import User
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
    course = courses_factory(name = 'TestCourse')
    response = api_client.get(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name
    
    
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
    courses = courses_factory(_quantity=10)
    response = api_client.get('/api/v1/courses/', {'id': courses[2].id})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == 3        
    
    
@pytest.mark.django_db
def test_filter_courses_by_name(api_client, courses_factory):
    courses = courses_factory(_quantity=10)
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
def test_course_update(api_client,courses_factory,students_factory):
    students_factory(id=1,name='TestStudent')
    courses_factory(id=1,name='TestCourse')
    data = {'name': 'UpdateCourse', 'students': [1]}
    response = api_client.patch('/api/v1/courses/1/',data=data,format='json')
    assert response.status_code == 200
    assert Course.objects.get(id=1).name == 'UpdateCourse'
    assert Course.objects.get(id=1).students.all().count() == 1
    assert list(Course.objects.get(id=1).students.all()) == [Student.objects.get(id=1)]
    
    
@pytest.mark.django_db
def test_course_delete(api_client,courses_factory):
    courses_factory(id=1,name='TestCourse')
    response = api_client.delete('/api/v1/courses/1/')
    assert response.status_code == 204
    assert len(Course.objects.all()) == 0
    
    
