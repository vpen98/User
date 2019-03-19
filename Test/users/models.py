from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # 用户信息于用户一对一关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('住址', max_length=128, blank=True)
    telephone = models.CharField('手机号码', max_length=50, blank=True)
    mod_date = models.DateTimeField("last modified", auto_now=True)

    class Meta:
        # 数据库表的名字
        db_table = "UserProfile"
        # 后台表的名称
        verbose_name = 'User Profile'
    
    def __str__(self):
        return "{}".format(self.user.__str__())