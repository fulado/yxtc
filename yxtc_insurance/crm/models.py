from django.db import models

# Create your models here.


# 路路通车辆信息
class VehicleLlt(models.Model):
    number = models.CharField(max_length=20, null=True, blank=True)  # 号牌号码
    type = models.IntegerField(default=2, null=True, blank=True)  # 车辆类型
    phone = models.CharField(max_length=20, null=True, blank=True)  # 联系电话
    is_tsn = models.BooleanField(default=True)  # 是否天津号码


# 原始库车辆信息
class VehicleStd(models.Model):
    number = models.CharField(max_length=20, null=True, blank=True)  # 号牌号码
    type = models.IntegerField(default=2, null=True, blank=True)  # 车辆类型
    e_code = models.CharField(max_length=20, null=True, blank=True)  # 发动机号
    v_code = models.CharField(max_length=20, null=True, blank=True)  # 车架号
    owner = models.CharField(max_length=200, null=True, blank=True)  # 所有人
    id_number = models.CharField(max_length=20, null=True, blank=True)  # 身份证号
    phone = models.CharField(max_length=20, null=True, blank=True)  # 联系电话
    valid_date = models.DateTimeField(null=True, blank=True)  # 验车有效期
    status = models.CharField(max_length=10, null=True, blank=True)  # 状态
    is_tsn = models.BooleanField(default=True)  # 是否天津号码


# 用户表
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    authority = models.IntegerField(default=3)  # 权限等级
    is_delete = models.BooleanField(default=False)
