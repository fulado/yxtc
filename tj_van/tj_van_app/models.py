from django.db import models

# Create your models here.


# 部门表
class Dept(models.Model):
    dept_name = models.CharField(max_length=50, null=True, blank=True)       # 部门名称


# 用户表
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)                     # 帐号
    password = models.CharField(max_length=50)                                  # 密码
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)  # 所属部门
    authority = models.IntegerField(default=1, null=True, blank=True)  # 权限: 0-超级管理员, 1-安监处, 2-支队


# 车辆表
class Vehicle(models.Model):
    number = models.CharField(max_length=20)  # 号牌号码
    brand = models.CharField(max_length=50, null=True, blank=True)  # 车辆品牌
    v_type = models.CharField(max_length=20, null=True, blank=True)   # 车辆类型
    vin = models.CharField(max_length=50, null=True, blank=True)  # 车辆识别代号
    owner = models.CharField(max_length=50, null=True, blank=True)  # 所有人
    p_id = models.CharField(max_length=50, null=True, blank=True)  # 身份证明号码
    address = models.CharField(max_length=100, null=True, blank=True)  # 住所详细地址
    phone = models.CharField(max_length=20, null=True, blank=True)  # 联系电话
    mobile = models.CharField(max_length=20, null=True, blank=True)  # 手机号
    driver = models.CharField(max_length=20, null=True, blank=True)  # 驾驶员
    d_phone = models.CharField(max_length=20, null=True, blank=True)  # 驾驶员电话
    discovery = models.IntegerField(default=0, null=True, blank=True)  # 排查状态: 0-未排查, 1-路面排查, 2-源头排查
    d_time = models.DateTimeField(null=True, blank=True)  # 排查时间
    d_dept_id = models.IntegerField(default=0, null=True, blank=True)  # 排查人员所属支队id
    is_card = models.BooleanField(default=False)  # 是否已发卡
    is_archive = models.BooleanField(default=False)  # 是否已建档
    c_time = models.DateTimeField(null=True, blank=True)  # 发卡时间
    a_time = models.DateTimeField(null=True, blank=True)  # 建档时间
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)  # 所属支队
    status = models.IntegerField(default=1, null=True, blank=True)  # 车辆状态: 1-未排查, 2-任务办理中, 3-已排查, 4-任务完成
    secure = models.CharField(max_length=200, null=True, blank=True)  # 隐患内容
    is_secure = models.BooleanField(default=False)  # 是否存在安全隐患


# 安全隐患表
class Security(models.Model):
    content = models.CharField(max_length=200, null=True, blank=True)  # 隐患内容
    is_fixed = models.BooleanField(default=False)  # 是否已整改
    f_time = models.DateTimeField(null=True, blank=True)  # 整改时间
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)  # 对应车辆
