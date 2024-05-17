from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import (Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject, Teacher)
import random
import logging

logger = logging.getLogger(__name__)


def fix_marks(schoolkid, child_name):
    child = schoolkid.objects.filter(full_name__contains=child_name)
    bad_marks = Mark.objects.filter(schoolkid=child[0], points__lt=4)
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid, child_name):
    child = schoolkid.objects.filter(full_name__contains=child_name)
    chastisements = Chastisement.objects.filter(schoolkid=child[0])
    chastisements.delete()


def create_commendation(child_name, lesson_title):
    try:
        year_of_study = 6
        group_letter = 'А'
        praises = ['Молодец', 'Так держать!', 'У тебя всё получается!', 'Успех близко', 'Мне приятно от твоих успехов!']

        children = Schoolkid.objects.filter(year_of_study=year_of_study, group_letter=group_letter, full_name__contains=child_name)

        if not children.exists():
            raise ObjectDoesNotExist('Данный пользователь не найден')

        if children.count() > 1:
            raise MultipleObjectsReturned('Возвращено несколько значений')

        subject = Subject.objects.filter(title=lesson_title, year_of_study=year_of_study).first()
        lesson = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter, subject=subject).first()
        teacher = Teacher.objects.filter(full_name=lesson.teacher).first()
        Commendation.objects.create(schoolkid=children[0], subject=subject, teacher=teacher, text=random.choice(praises), created=lesson.date)

    except ObjectDoesNotExist as e:
        logger.warning(f'Произошла ошибка: {e}')
    except MultipleObjectsReturned as e:
        logger.warning(f'Произошла ошибка: {e}')
