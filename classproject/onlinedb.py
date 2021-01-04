import openpyxl
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classproject.settings")
django.setup()
from  onlineapp.models import College, Student, MockTest1

skip = True
wb = openpyxl.load_workbook("students.xlsx")
# ws = wb['Colleges']
# for row in ws.rows:
#     if skip:
#         skip = False
#         continue
#     temp = [cell.value.strip() for cell in row]
#     c = College(name=temp[0], location=temp[2], acronym=temp[1], contact=temp[3])
#     c.save()
#
# skip=True
# ws = wb['Current']
# for row in ws.rows:
#     if skip:
#         skip = False
#         continue
#     temp = [cell.value.strip() for cell in row]
#     c = College.objects.get(acronym=temp[1].lower())
#     s = Student(name=temp[0], email=temp[2], db_folder=temp[3], college=c)
#     s.save()
#
# skip = True
# ws = wb['Deletions']
# for row in ws.rows:
#     if skip:
#         skip = False
#         continue
#     temp = [cell.value.strip() for cell in row]
#     c = College.objects.get(acronym=temp[1].lower())
#     s = Student(name=temp[0], email=temp[2], db_folder=temp[3], college=c, dropped_out=True)
#     s.save()
#
#
# wb = openpyxl.load_workbook("results.xlsx")
# ws = wb['Mock Results']
# skip = True
# for row in ws.rows:
#     if skip:
#         skip = False
#         continue
#     temp = [cell.value for cell in row]
#     s = Student.objects.get(db_folder=temp[0].split('_')[2])
#     m = MockTest1(student=s, problem1=temp[1], problem2=temp[2], problem3=temp[3], problem4=temp[4], total=temp[5])
#     m.save()