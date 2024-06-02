from datacenter.models import (Chastisement, Commendation, Lesson, Mark, Schoolkid)
import random
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_child_by_name(child_name):
    try:
        return Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.DoesNotExist:
        logger.error(f'Произошла ошибка: Ученика с указанным именем не найдено.')
        sys.exit()
    except Schoolkid.MultipleObjectsReturned:
        logger.error(f'Произошла ошибка: Получено несколько учеников с этим именем.')
        sys.exit()


def fix_marks(child_name):
    child = get_child_by_name(child_name)
    bad_marks = Mark.objects.filter(schoolkid=child, points__lt=4)
    if not bad_marks:
        return logger.info('У данного ученика нет плохих оценок')
    bad_marks.update(points=random.randint(4, 5))


def remove_chastisements(child_name):
    child = get_child_by_name(child_name)
    chastisements = Chastisement.objects.filter(schoolkid=child)
    if not chastisements:
        return logger.info('У данного ученика нет замечаний')
    chastisements.delete()



def create_commendation(child_name, lesson_title):
    compliments = ['Молодец', 'Так держать!', 'У тебя всё получается!', 'Успех близко', 'Мне приятно от твоих успехов!']
    child = get_child_by_name(child_name)
    lessons = Lesson.objects.filter(
        year_of_study=child.year_of_study, 
        group_letter=child.group_letter, 
        subject__title=lesson_title
        )
    lesson_of_subject = lessons.order_by('-date').first()
    Commendation.objects.create(
        schoolkid=child, 
        subject=lesson_of_subject.subject, 
        teacher=lesson_of_subject.teacher, 
        text=random.choice(compliments), 
        created=lesson_of_subject.date
    )
