from rest_framework import serializers
from onlineapp.models import College, Student, MockTest1


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('id', 'name', 'acronym', 'location', 'contact')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'db_folder', 'dropped_out') #, 'college')


class MockTest1Serializer(serializers.ModelSerializer):
    class Meta:
        model = MockTest1
        fields = ('problem1', 'problem2', 'problem3', 'problem4', 'total') #, 'student')


class StudentDetailsSerializer(serializers.ModelSerializer):
    mocktest1 = MockTest1Serializer(many=False, read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'dob', 'db_folder', 'dropped_out', 'mocktest1')

    # def create(self, validated_data):
    #     pass
    #
    # def update(self, student, validated_data):
    #     pass
