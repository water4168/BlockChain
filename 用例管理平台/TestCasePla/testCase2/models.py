from datetime import datetime

from django.db import models


# Create your models here.

class ProjectVersion2(models.Model):
    """
    项目版本信息
    """
    projectVersion = models.CharField(max_length=10, unique=True, verbose_name='project')

    class Meta:
        verbose_name = "MyBitt版本"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.projectVersion


class TestCaseProfile2(models.Model):
    """
    测试用例
    """
    testId = models.IntegerField(null=True, blank=True, verbose_name="序号")
    xuqiu = models.CharField(max_length=50, verbose_name="需求")
    process = models.TextField(max_length=5000, verbose_name="测试用例")
    testMethod = models.CharField(max_length=10, null=True, blank=True, verbose_name="测试方法")
    testDate = models.CharField(max_length=50, null=True, blank=True, verbose_name="测试日期")
    people = models.CharField(max_length=10, null=True, blank=True, verbose_name="测试人员")
    status = models.CharField(max_length=10, null=True, blank=True,  verbose_name="测试状态")
    info = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    addTime = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name="添加时间")
    project = models.ForeignKey(ProjectVersion2, on_delete=models.CASCADE, default="默认项目", blank=True, verbose_name="所属项目")

    class Meta:
        verbose_name = "版本用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.xuqiu



