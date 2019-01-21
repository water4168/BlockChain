from datetime import datetime

from django.db import models


# Create your models here.

class ProjectVersion(models.Model):
    """
    项目版本信息
    """
    projectVersion = models.CharField(max_length=30, verbose_name='项目版本')

    class Meta:
        verbose_name = "UDO版本"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.projectVersion


class TestCaseProfile(models.Model):
    """
    测试用例
    """
    # TEST_STATUS = (
    #     (0, "未执行"),
    #     (1, "通过"),
    #     (2, "不通过"),
    #     (3, "中断")
    # )
    testId = models.IntegerField(null=True, blank=True, verbose_name="序号")
    xuqiu = models.CharField(max_length=50, verbose_name="需求")
    process = models.TextField(max_length=5000, verbose_name="测试用例")
    testMethod = models.CharField(max_length=10, null=True, blank=True, verbose_name="测试方法")
    testDate = models.CharField(max_length=50, null=True, blank=True, verbose_name="测试日期")
    people = models.CharField(max_length=10, null=True, blank=True, verbose_name="测试人员")
    status = models.CharField(max_length=10, null=True, blank=True,  verbose_name="测试状态")
    info = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    addTime = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name="添加时间")
    project = models.ForeignKey(ProjectVersion, on_delete=models.CASCADE, null=True, blank=True, verbose_name="所属项目")

    class Meta:
        verbose_name = "版本用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.xuqiu



