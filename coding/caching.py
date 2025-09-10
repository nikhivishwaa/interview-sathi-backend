from coding.models import CodingQuestion, TestCase, Submission, SubmissionLog, CodingSolution, Language
from coding.serializers import CodingQuestionSerializer, TestCaseSerializer
from django.core.cache import cache
import json

# fetch testcases with cache
def get_testcases(question_id, include_hidden=False):
    cache_key = f"testcases:{question_id}:{'all' if include_hidden else 'visible'}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    if not include_hidden:
        queryset = TestCase.objects.filter(question_id=question_id, is_hidden=False)
    else:
        queryset = TestCase.objects.filter(question_id=question_id)

    testcases = TestCaseSerializer(queryset, many=True).data
    cache.set(cache_key, json.dumps(testcases), 1000)
    return testcases

def get_languages(language_id=None):
    cache_key = f"languages:{language_id or 'all'}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    if language_id:
        _lang = Language.objects.get(pk=language_id)
        languages = dict()
        languages["name"] = _lang.name
        languages["id"] = _lang.id
        cache.set(cache_key, json.dumps(languages), 1800)

    else:
        languages = Language.objects.all().values('id', 'name')
        cache.set(cache_key, json.dumps(list(languages)), 1800)
    return languages