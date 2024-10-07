import pytest
from model_bakery import baker

from students.models import Course


@pytest.mark.django_db
def test_course_retrieve(client, course_factory):
    course = course_factory(_quantity=1)
    responce = client.get(f'/api/v1/courses/{course[0].id}/')
    assert responce.status_code == 200
    data = responce.json()
    assert data['name'] == course[0].name
    
@pytest.mark.django_db
def test_course_list(client, course_factory):
    course = course_factory(_quantity=3)
    responce = client.get(f'/api/v1/courses/')
    assert responce.status_code == 200
    data = responce.json()
    assert len(data) == len(course)
    for i, c in enumerate(data):
        assert c['name'] == course[i].name
        
@pytest.mark.django_db
def test_course_filter_id(client, course_factory):
    course = course_factory(_quantity=3)
    responce = client.get(f'/api/v1/courses/', data={'id': course[0].id})
    assert responce.status_code == 200
    data = responce.json()
    assert data[0]['name'] == course[0].name

@pytest.mark.django_db
def test_course_filter_name(client, course_factory):
    course = course_factory(_quantity=3)
    responce = client.get(f'/api/v1/courses/', data={'name': course[0].name})
    assert responce.status_code == 200
    data = responce.json()
    for i, c in enumerate(data):
        assert c['name'] == course[0].name
        
@pytest.mark.django_db
def test_course_create(client):
    course_name = 'test_course_1'
    responce = client.post(f'/api/v1/courses/', data={'name': course_name}, format='json')
    assert responce.status_code == 201
    data = responce.json()
    assert course_name == data['name']
    
@pytest.mark.django_db
def test_course_update(client, course_factory):
    course = course_factory(_quantity=1)
    update_name = 'test_course_update'
    response = client.put(f'/api/v1/courses/{course[0].id}/', data={'name': update_name}, format='json')
    assert response.status_code == 200
    data = response.json()
    assert update_name == data['name']

@pytest.mark.django_db
def test_course_delete(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{course[0].id}/', format='json')
    assert response.status_code == 204
    assert Course.objects.filter(id=course[0].id).count() == 0