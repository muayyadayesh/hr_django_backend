from rest_framework import serializers
from ..models import Candidate

# post serializer


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["full_name", "date_of_birth",
                  "experience_years", "department_id", 'resume_file']

# get serializer


class CandidateSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        exclude = ('resume_file', 'registration_date',)
