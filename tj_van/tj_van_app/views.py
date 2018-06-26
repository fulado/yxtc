from tj_van import settings
from tj_van.utils import MyPaginator
from .models import User, Vehicle
from .decorator import login_check
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
import random
import io
import hashlib
import time

# Create your views here.


# 显示登录页面
def login(request):
    # session中的user_id不等于空直接跳转到主页
    user_id = request.session.get('user_id', '')
    if user_id != '':
        return HttpResponseRedirect('/main')

    msg = request.GET.get('msg', '')

    context = {'msg': msg}

    return render(request, 'login.html', context)


# 验证码
def check_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bg_color = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25

    # 创建画面对象
    im = Image.new('RGB', (width, height), bg_color)

    # 创建画笔对象
    draw = ImageDraw.Draw(im)

    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    str1 = 'ABCD23EFGHJK456LMNPQRS789TUVWXYZ'

    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 设置字体
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 23)

    # 字体颜色
    font_color = (255, 243, 67)

    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=font_color)
    draw.text((25, 2), rand_str[1], font=font, fill=font_color)
    draw.text((50, 2), rand_str[2], font=font, fill=font_color)
    draw.text((75, 2), rand_str[3], font=font, fill=font_color)

    # 释放画笔
    del draw

    # 存入session，用于做进一步验证
    request.session['check_code'] = rand_str
    request.session.set_expiry(0)  # 浏览器关闭后清除session

    # 内存文件操作
    buf = io.BytesIO()

    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')

    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 登陆服务
def login_handle(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('check_code').upper()

    session_code = request.session.get('check_code')

    if code != session_code:
        msg = '验证码错误'
        return HttpResponseRedirect('/?msg=%s' % msg)

    user_list = User.objects.filter(username=username)
    if len(user_list) == 0:
        msg = '用户不存在'
        return HttpResponseRedirect('/?msg=%s' % msg)

    user = user_list[0]
    if hashlib.sha1(password.encode('utf8')).hexdigest() != user.password:
        msg = '用户名或密码错误'
        return HttpResponseRedirect('/?msg=%s' % msg)

    # 把user.id保存到session中
    request.session.set_expiry(0)  # 浏览器关闭后清除session
    request.session['user_id'] = user.id
    request.session['authority_id'] = user.authority

    return HttpResponseRedirect('/main')


# 退出登录
def logout(request):
    request.session.clear()
    request.session.flush()

    return HttpResponseRedirect('/')


# 显示主页面
@login_check
def main(request):
    user_id = request.session.get('user_id', '')

    if user_id != '':
        user = User.objects.filter(id=user_id)[0]
    # 这里有点问题, user不一定有值, 后面得修改
    context = {'user': user}

    return render(request, 'main.html', context)


# 显示账号管理页面
@login_check
def account(request):
    # 查询企业信息
    user_list = User.objects.all().exclude(id=1).order_by('id')

    # 获取企业搜索信息
    search_name = request.GET.get('search_name', '')
    # 在结果集中搜索包含搜索信息的企业
    if search_name != '':
        user_list = user_list.filter(username__contains=search_name)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(user_list, 10, page_num)

    context = {'mp': mp, 'search_name': search_name}

    # 保存当前页面状态到session
    request.session['search_name'] = search_name
    request.session['page_num'] = page_num

    return render(request, 'account.html', context)


# 显示审核页面
@login_check
def verify(request):
    # 获取session中的user_id,
    user_id = int(request.session.get('user_id', ''))

    # 根据user_id查询用户
    user = User.objects.get(id=user_id)

    # 查询该用户所属支队的所有车辆数据
    if user_id != '' and user_id != 1:
        vehicle_list = Vehicle.objects.filter(dept_id=user.dept_id).order_by('id')
    else:
        vehicle_list = Vehicle.objects.all().order_by('id')

    # 获取用户选择的车辆查询状态, 默认为1, 只查看待处理车辆, 正式运行改成2
    status = int(request.GET.get('status', 2))

    # 根据不同状态过滤车辆
    if status != 0:
        vehicle_list = vehicle_list.filter(status=status)

    # 获取车辆搜索信息
    number = request.GET.get('number', '')

    # 在结果集中搜索包含搜索信息的车辆, 车辆搜索功能不完善, 指数如车牌号,不要输入号牌所在地
    if number != '':
        vehicle_list = vehicle_list.filter(number__contains=number)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp, 'number': number, 'user_id': user_id, 'status': status}

    # 保存页面状态到session
    request.session['number'] = number
    request.session['status'] = status
    request.session['page_num'] = page_num

    return render(request, 'verify.html', context)


# 显示车辆排查页面
@login_check
def vehicle(request):
    # 查询所有车辆数据
    vehicle_list = Vehicle.objects.all().order_by('id')

    # 获取车辆搜索信息
    number = request.GET.get('number', '')
    dept_id = int(request.GET.get('dept', '0'))

    # 在结果集中搜索包含搜索信息的车辆, 车辆搜索功能不完善, 指数如车牌号,不要输入号牌所在地
    if number != '':
        vehicle_list = vehicle_list.filter(number__contains=number)

    if dept_id != 0:
        vehicle_list = vehicle_list.filter(dept_id=dept_id)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp, 'number': number, 'dept': dept_id}

    # 保存页面状态到session
    request.session['number'] = number
    request.session['dept'] = dept_id
    request.session['page_num'] = page_num

    return render(request, 'vehicle.html', context)


# 提交车辆排查信息
def vehicle_modify(request):
    # 获取用户提交的车辆信息
    vehicle_id = request.GET.get('vehicle_id', '')
    driver = request.GET.get('driver', '')
    d_phone = request.GET.get('d_phone', '')
    discovery = request.GET.get('discovery', '0')
    is_card = request.GET.get('is_card', '0')
    is_archive = request.GET.get('is_archive', '0')
    is_secure = request.GET.get('is_secure', '0')
    secure = request.GET.get('secure', '')

    try:
        # 根据id查询车辆
        car = Vehicle.objects.get(id=vehicle_id)
        car.driver = driver
        car.d_phone = d_phone
        car.discovery = discovery
        car.is_card = is_card
        car.is_archive = is_archive
        car.is_secure = is_secure
        car.secure = secure
        car.status = 2
        car.d_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        car.save()
    except Exception as e:
        print(e)

    # 构建返回url
    number = request.session.get('number', '')
    dept = request.session.get('dept', '')
    page_num = request.session.get('page_num', '')
    url = '/vehicle?number=%s&page_num=%s&dept=%s' % (number, page_num, dept)

    return HttpResponseRedirect(url)


# 提交车辆办理信息
def verify_modify(request):
    # 获取用户提交的车辆信息
    vehicle_id = request.GET.get('vehicle_id', '')
    driver = request.GET.get('driver', '')
    d_phone = request.GET.get('d_phone', '')
    discovery = int(request.GET.get('discovery', '0'))
    is_card = int(request.GET.get('is_card', '0'))
    is_archive = int(request.GET.get('is_archive', '0'))
    is_secure = int(request.GET.get('is_secure', '0'))
    secure = request.GET.get('secure', '')

    try:
        # 根据id查询车辆
        car = Vehicle.objects.get(id=vehicle_id)
        car.driver = driver
        car.d_phone = d_phone
        car.discovery = discovery
        car.is_card = is_card
        car.is_archive = is_archive
        car.is_secure = is_secure
        car.secure = secure
        car.status = 3

        if is_card:
            car.c_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        if is_archive:
            car.a_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        car.save()
    except Exception as e:
        print(e)

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 添加用户
def account_add(request):
    # 获取账号信息
    username = request.POST.get('username')                 # 帐号
    password = request.POST.get('password')                 # 密码 不能使用'########'
    dept_id = int(request.POST.get('dept', '1'))   # 部门

    # 创建user
    user = User()
    user.username = username
    user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
    user.dept_id = dept_id
    if dept_id == 1:
        user.authority = 1
    else:
        user.authority = 2

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    # 构建返回url
    search_name = request.session.get('search_name', '')
    page_num = request.session.get('page_num', '')

    url = '/account?search_name=%s&page_num=%s' % (search_name, page_num)

    return HttpResponseRedirect(url)


# 编辑用户
def account_modify(request):
    # 获取账号信息
    user_id = request.POST.get('user_id')
    username = request.POST.get('username')                 # 帐号
    password = request.POST.get('password')                 # 密码 不能使用'########'
    dept_id = int(request.POST.get('dept', '1'))            # 部门
    print(dept_id)
    # 查询用户
    user = User.objects.get(id=user_id)
    user.username = username
    user.dept_id = dept_id

    if dept_id == 1:
        user.authority = 1
    else:
        user.authority = 2

    # 如果密码不是8个'#', 需要修改密码
    if password != r'########':
        user.password = hashlib.sha1(password.encode('utf8')).hexdigest()

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    # 构建返回url
    search_name = request.session.get('search_name', '')
    page_num = request.session.get('page_num', '')

    url = '/account?search_name=%s&page_num=%s' % (search_name, page_num)

    return HttpResponseRedirect(url)


# 判断用户名是否已经存在
def is_user_exist(request):
    username = request.GET.get('username')
    user_id = request.GET.get('id', 0)

    if user_id == 0:
        is_exist = User.objects.filter(username=username).exists()
    else:
        is_exist = User.objects.filter(username=username).exclude(id=user_id).exists()

    return JsonResponse({'is_exist': is_exist})


# 删除用户信息
def account_delete(request):
    # 获取用户id
    user_id = request.POST.get('user_id')  # 用户id

    # 查询user
    user = User.objects.get(id=user_id)

    # 删除user
    try:
        user.delete()
    except Exception as e:
        print(e)

    # 构建返回url
    search_name = request.session.get('search_name', '')
    page_num = request.session.get('page_num', '')
    url = '/account?search_name=%s&page_num=%s' % (search_name, page_num)

    return HttpResponseRedirect(url)
