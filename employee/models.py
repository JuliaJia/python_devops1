from django.db import models

# Create your models here.

class Employee(models.Model):
    class Gender(models.IntegerChoices):
        MAN = 1,"男"
        FEMALE = 2, "女"
    class Meta:
        db_table = "employee"
        verbose_name = "员工"
    emp_no = models.IntegerField(primary_key=True,verbose_name="工号")
    birth_date = models.DateField(verbose_name="生日")
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gender = models.SmallIntegerField(choices=Gender.choices)
    hire_date = models.DateField(verbose_name="入职时间",default="2022-01-01")




    @property
    def name(self):
        return "".format(self.first_name,self.last_name)
    def __str__(self):
        return "<E {},{}>".format(self.pk,self.name)

    __repr__ = __str__



class Salary(models.Model):
    class Meta:
        db_table = "salaries"
    emp_no = models.ForeignKey(Employee,models.CASCADE,
                               db_column='emp_no',related_name='salaries')
    salary = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()

    @property
    def __str__(self):
        return "<E {},{}>".format(self.pk,self.emp_no,self.salary)

    __repr__ = __str__