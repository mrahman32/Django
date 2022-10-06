from datetime import datetime, timedelta, date
from email.policy import default
from importlib.resources import path
from pyexpat import model
from secrets import choice
from time import timezone
from django.db import models
from django.utils import timezone

# smart contract imports
import string
from web3 import Web3
import os
from dotenv import load_dotenv
import json

# Create your models here.


class Department(models.Model):
    department_name = models.CharField(max_length=200)
    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.BigIntegerField
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField

    def __str__(self) -> str:
        return self.department_name

    # def was_published_recently(self):
    #     return self.added_date >= timezone.now() - timedelta(days=1)


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50)
    credit_hr = models.IntegerField
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # def __str__(self) -> str:
    #     return self.choice_text


class Semester(models.Model):
    semester_name = models.CharField(max_length=50)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.semester_name


class Student(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    student_roll = models.CharField(max_length=100)
    student_name = models.CharField(max_length=200)
    student_address = models.CharField(max_length=500)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:

        load_dotenv()

        # Open up ABI for calling functions
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_file_path = os.path.join(
            BASE_DIR, "aeibt/contractsjson/student_record_compiled_code.json"
        )
        with open(json_file_path) as file:
            student_json = json.load(file)

        bytecode = student_json["contracts"]["InfoStorage.sol"]["InfoStorage"]["evm"][
            "bytecode"
        ]["object"]
        print(bytecode)

        # get abi
        abi = student_json["contracts"]["InfoStorage.sol"]["InfoStorage"]["abi"]
        print(abi)

        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

        chain_id = 1337
        my_address = os.getenv("MY_ADDRESS")
        private_key = os.getenv("MY_PRIVATE_KEY")
        print(my_address)
        print(private_key)

        w3.eth.default_account = my_address

        student_storage_contract = w3.eth.contract(
            address="0xf528118C6a6bBB61b47Ff92B4431C9b7277E790a",
            abi=abi,
            bytecode=bytecode,
        )

        self.added_date = datetime.now()
        cr_date = self.added_date  # don't use str here
        dateStr = cr_date.strftime("%m/%d/%Y")

        return_after_added = student_storage_contract.functions.add_new_student_record(
            self.student_name,
            self.student_roll,
            self.department.department_name,
            self.semester.semester_name,
            dateStr,
            "",
            "",
            self.student_address,
        ).transact()

        w3.eth.wait_for_transaction_receipt(return_after_added)
        print(return_after_added)

        # results = student_storage_contract.functions.getStudentRecordFiles(
        #     "2009000000032").call()
        # print(results)

        # self.student_name = self.student_name + " (Nick)"
        return super().save(self, *args, **kwargs)


# class TakenCourse(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     added_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)


class StudentDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50)
    document_name = models.CharField(max_length=500)
    block_trans_id = models.CharField(max_length=255)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Teacher(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=200)
    teacher_address = models.CharField(max_length=500)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class SemesterCourse(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)


class SemesterCourseEnroll(models.Model):
    semester_course = models.ForeignKey(SemesterCourse, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)


class CourseClass(models.Model):
    semester_course_enroll = models.ForeignKey(
        SemesterCourseEnroll, on_delete=models.CASCADE
    )
    is_present = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
