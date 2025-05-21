from rest_framework import serializers
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption

# 적금
# Saving 데이터 불러오기
class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'
        read_only_fields = ('interest_user',)

# Saving 옵션 데이터
class SavingOptionSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        # 사용자가 옵션을 임의로 바꾸면 안되니까
        read_only_fields = ('saving_product',)

# Saving 리스트 출력
class SavingListSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionSerialzier(many=True, read_only=True)
    class Meta:
        model = SavingProduct
        fields = '__all__'
        read_only_fields = ('interest_user',)


# 예금
# Deposit 데이터 불러오기(상품의 전체 정보)
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'
        # 클라이언트가 이 필드를 수정하지 못하도록, 찜하기 버튼 클릭 시에만 가능
        read_only_fields = ('interest_user',)


# Deposit 옵션 데이터(개별 옵션 -> 기간, 금리 등 옵션 자체의 정보만 반환)
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'

# Deposit 리스트 출력(상품 정보의 모든 정보와 옵션 함께 포함)
class DepositListSerializer(serializers.ModelSerializer):
    # 상품 하나에 여러 개의 옵션 연결(일대다 관계)
    # DepositOption 모델이 외래키로 DepositProduct 참조하고 있기 때문에 이렇게 작성
    depositoption_set = DepositOptionSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProduct
        fields = '__all__'
        read_only_fields = ('interest_user',)


