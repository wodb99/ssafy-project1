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
class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        # 사용자가 옵션을 임의로 바꾸면 안되니까
        read_only_fields = ('saving_product',)

# Saving 리스트 출력
class SavingListSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionSerializer(many=True, read_only=True)
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


# 프로필 페이지에서 찜한 상품들 보여줄 때 상세 정보와 함께 출력하기 위해
class InterestSavingSerializer(serializers.ModelSerializer):
    depositoption_set = DepositOptionSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProduct
        fields = ('id', 'fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'depositoption_set')

class InterestDepositSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProduct
        fields = ('id', 'fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'savingoption_set')


# 가입 기간이 같은 옵션만 응답으로 포함
class DepositMonthSerializser(serializers.ModelSerializer):
    depositoption_set = DepositOptionSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProduct
        fields = '__all__'
        read_only_fields = ('interest_user',)

    def __init__(self, *args, **kwargs):
        # save_trm 꺼내서 변수에 저장
        self.save_trm = kwargs.pop('save_trm', None)
        # 부모 클래스로 전달
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        # 기본 직렬화 데이터 가져오기
        representation = super().to_representation(instance)
        # depositoption_set 일시 제거, 예금 상품의 기본 정보만 남김
        depositoption_set = representation.pop('depositoption_set')

        # save_trm 조건에 맞는 옵션만 필터링
        filtered_options = [option for option in depositoption_set if option['save_trm'] == self.save_trm]
        representation['depositoption_set'] = filtered_options

        return representation
    
class SavingMonthSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProduct
        fields = '__all__'
        read_only_fields = ('interest_user',)

        def __init__(self, *args, **kwargs):
            self.save_trm = kwargs.pop('save_trm', None)
            super().__init__(*args, **kwargs)

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            savingoption_set = representation.pop('savingoption_set')

            # save_trm 조건에 맞는 옵션만 필터링
            filtered_options = [option for option in savingoption_set if option['save_trm'] == self.save_trm]
            representation['savingoption_set'] = filtered_options

            return representation