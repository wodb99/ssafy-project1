from django.db import models
from django.conf import settings

# Create your models here.
# 적금 상품 정보
class SavingProduct(models.Model):
    # settings.AUTH_USER_MODEL : 연결할 모델 지정
    # User 인스턴스에서 자신이 관심 등록한 Saving Product 목록 조회 가능(역참조)
    interest_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interest_saving')
    dcls_month = models.TextField()
    fin_prdt_cd = models.TextField()
    fin_co_no = models.TextField()
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    join_way = models.TextField()
    mtrt_int = models.TextField()
    spcl_cnd = models.TextField()
    # 디폴트 값 0 ?
    join_deny = models.IntegerField(default=0)    
    join_member = models.TextField()
    etc_note = models.TextField()
    max_limit = models.IntegerField(blank=True, null=True)

# 적금 상품 세부 옵션
class SavingOption(models.Model):
    # ForeignKey : SavingProduct 모델 참조하고 있음을 의미
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    intr_rate_type = models.CharField(max_length=100)
    intr_rate_type_nm = models.CharField(max_length=100)
    rsrv_type = models.TextField()
    rsrv_type_nm = models.TextField()
    save_trm = models.IntegerField(default=0)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)

# 예금 상품 정보
class DepositProduct(models.Model):
    interest_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interest_saving')
    dcls_month = models.TextField()
    fin_prdt_cd = models.TextField()
    fin_co_no = models.TextField()
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    join_way = models.TextField()
    mtrt_int = models.TextField()
    spcl_cnd = models.TextField()
    join_deny = models.IntegerField(default=0)    
    join_member = models.TextField()
    etc_note = models.TextField()
    max_limit = models.IntegerField(blank=True, null=True)    

# 예금 상품 세부 옵션
class DepositOption(models.Model):
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    intr_rate_type = models.CharField(max_length=100)
    intr_rate_type_nm = models.CharField(max_length=100)
    save_trm = models.IntegerField(default=0)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)



