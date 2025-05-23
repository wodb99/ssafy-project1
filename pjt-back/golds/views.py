from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from .models import PriceData
from dateutil.parser import parse
import pandas as pd

# Create your views here.
def price_chart(request):
    # 차트 페이지 렌더링
    return render(request, 'golds/chart.html')

def price_api(request):
    asset_type = request.GET.get('asset', 'GOLD').upper()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    try:
        start_date = parse(start_date_str) if start_date_str else None
        end_date = parse(end_date_str) if end_date_str else None
    except Exception:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    queryset = PriceData.objects.filter(asset_type=asset_type)

    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)

    queryset = queryset.order_by('date')

    data = {
        'labels': [item.date.strftime('%Y-%m-%d') for item in queryset],
        'datasets': [{
            'label': f'{asset_type} Price',
            'data': [float(item.price) for item in queryset],
            'borderColor': '#4bc0c0' if asset_type == 'GOLD' else '#ff9f40'
        }]
    }

    return JsonResponse(data)
