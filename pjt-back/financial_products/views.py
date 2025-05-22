import requests
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DepositProduct, SavingProduct, DepositOption, SavingOption
from .serializers import DepositSerializer, DepositOptionSerializer, DepositListSerializer, InterestDepositSerializer
from .serializers import SavingSerializer, SavingOptionSerializer, SavingListSerializer, InterestSavingSerializer


# Create your views here.
API_KEY = settings.FIN_API_KEY

# < 초기 데이터 가져오기 >
@api_view(['GET'])
def get_deposit_products(request):
    deposit_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    # JSON 데이터에서 'result'라는 키 값 가져와서, result 딕셔너리의 'baseList'라는 키 값 가져오기
    response = requests.get(deposit_API_URL)
    data = response.json().get('result', {})
    deposit_baselist = data.get('baseList', [])
    deposit_optionlist = data.get('optionList', [])

    # base는 한 개의 예금 상품 데이터
    for base in deposit_baselist:
        # 이미 같은 상품 코드가 DB에 있으면, 실행 안 하고 다음으로 넘어감 
        if DepositProduct.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')):
            continue
        deposit_product = {
            'dcls_month' : base.get('dcls_month'),
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'fin_co_no': base.get('fin_co_no'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'join_way': base.get('join_way'),
            'mtrt_int': base.get('mtrt_int'),
            'spcl_cnd': base.get('spcl_cnd'),
            'join_deny': base.get('join_deny'),
            'join_member': base.get('join_member'),
            'etc_note': base.get('etc_note'),
            'max_limit': base.get('max_limit')
        }
        serializer = DepositSerializer(data=deposit_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option in deposit_optionlist:
        prdt_cd = option.get('fin_prdt_cd')
        products = DepositProduct.objects.filter(fin_prdt_cd=prdt_cd)
        for product in products:
            deposit_option = {
                'intr_rate_type': option.get('intr_rate_type'),
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'save_trm': option.get('save_trm'),
                'intr_rate': option.get('intr_rate'),
                'intr_rate2': option.get('intr_rate2'),
            }
            serializer = DepositOptionSerializer(data=deposit_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit_product=product)
    return Response('Deposit 데이터 가져오기 성공')

@api_view(['GET'])
def get_saving_products(request):
    saving_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    saving_baselist = requests.get(saving_API_URL).json()['result']['baseList']
    saving_optionlist = requests.get(saving_API_URL).json()['result']['optionList']

    for base in saving_baselist:
        if SavingProduct.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')):
            continue
        saving_product = {
            'dcls_month' : base.get('dcls_month'),
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'fin_co_no': base.get('fin_co_no'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'join_way': base.get('join_way'),
            'mtrt_int': base.get('mtrt_int'),
            'spcl_cnd': base.get('spcl_cnd'),
            'join_deny': base.get('join_deny'),
            'join_member': base.get('join_member'),
            'etc_note': base.get('etc_note'),
            'max_limit': base.get('max_limit')
        }
        serializer = SavingSerializer(data=saving_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option in saving_optionlist:
        prdt_cd = option.get('fin_prdt_cd')
        products = SavingProduct.objects.filter(fin_prdt_cd=prdt_cd)
        for product in products:
            saving_option = {
                'intr_rate_type': option.get('intr_rate_type'),
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'rsrv_type': option.get('rsrv_type'),
                'rsrv_type_nm': option.get('rsrv_type_nm'),
                'save_trm': option.get('save_trm'),
                'intr_rate': option.get('intr_rate'),
                'intr_rate2': option.get('intr_rate2'),  
            }
            serializer = SavingOptionSerializer(data=saving_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving_product=product)
    return Response('Saving 데이터 가져오기 성공')


# < 목록 조회 >
@api_view(['GET'])
# 로그인(인증)된 사용자만 접근 가능하도록
@permission_classes([IsAuthenticated])
def deposit_product_list(request):
    if request.method == 'GET':
        # DepositProduct의 모든 데이터 DB에서 조회
        deposit_products = DepositProduct.objects.all()
        # 직렬화, 여러 개의 객체라면 many=True 꼭 필요
        serializer = DepositListSerializer(deposit_products, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_product_list(request):
    if request.method == 'GET':
        saving_products = SavingProduct.objects.all()
        serializer = SavingListSerializer(saving_products, many=True)
        return Response(serializer.data)


# < 상세 정보 조회 >
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_detail(request, deposit_name):
    # 상품명과 예금 상품명이 같은 객체 찾기, 없으면 404 에러 발생
    deposit = get_object_or_404(DepositProduct, fin_prdt_nm=deposit_name)
    if request.method == 'GET':
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_detail(request, saving_name):
    saving = get_object_or_404(SavingProduct, fin_prdt_nm=saving_name)
    if request.method == 'GET':
        serializer = SavingSerializer(saving)
        return Response(serializer.data)
    

# < 옵션 목록 조회 >
# 옵션 리스트(여러 개, 모든 옵션 보기)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_option_list(request, deposit_name):
    deposit = get_object_or_404(DepositProduct, fin_prdt_nm=deposit_name)
    # 예금 상품명이 동일한 옵션 목록 조회
    deposit_options = DepositOption.objects.filter(deposit_product=deposit)

    if request.method == 'GET':
        serializer = DepositOptionSerializer(deposit_options, many=True)
        return Response(serializer.data)

# 옵션 1개의 상세 정보(상품 코드, 옵션 ID로 조회)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_option_detail(request, deposit_code, option_id):
    deposit = get_object_or_404(DepositProduct, fin_prdt_cd=deposit_code)
    option = DepositOption.objects.get(deposit_product=deposit, id=option_id)
    if request.method == 'GET':
        serializer = DepositOptionSerializer(option)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_option_list(request, saving_name):
    saving = get_object_or_404(SavingProduct, fin_prdt_nm=saving_name)
    saving_options = SavingOption.objects.filter(saving_product=saving)

    if request.method == 'GET':
        serializer = SavingOptionSerializer(saving_options, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_option_detail(request, saving_code, option_id):
    saving = get_object_or_404(SavingProduct, fin_prdt_cd=saving_code)
    option = SavingOption.objects.get(saving_product=saving, id=option_id)
    if request.method == 'GET':
        serializer = SavingOptionSerializer(option)
        return Response(serializer.data)
    

# < 특정 은행의 예적금 조회 >
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_deposit(request, bank_name):
    if request.method == 'GET':
        if DepositProduct.objects.filter(kor_co_nm=bank_name).exists():
            deposits = DepositProduct.objects.filter(kor_co_nm=bank_name)
            serializer = DepositListSerializer(deposits, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': '해당 은행의 상품이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_saving(request, bank_name):
    if request.method == 'GET':
        if SavingProduct.objects.filter(kor_co_nm=bank_name).exists():
            savings = SavingProduct.objects.filter(kor_co_nm=bank_name)
            serializer = SavingListSerializer(savings, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': '해당 은행의 상품이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


# < 찜하거나 취소하는 기능 >
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_deposit(request, deposit_code):
    deposit = get_object_or_404(DepositProduct, fin_prdt_cd=deposit_code)
    user = request.user
    if deposit.interest_user.filter(id=user.id).exists(): # 이미 좋아요한 경우 좋아요 취소
        deposit.interest_user.remove(user)  
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    else:
        deposit.interest_user.add(user)  # 좋아요 추가
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_saving(request, saving_code):
    saving = get_object_or_404(SavingProduct, fin_prdt_cd=saving_code)
    user = request.user
    if saving.interest_user.filter(id=user.id).exists():
        saving.interest_user.remove(user)  # 이미 좋아요한 경우 좋아요 취소
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    else:
        saving.interest_user.add(user)  # 좋아요 추가
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)