from django.contrib import admin
from django import forms
from django.db import models
from .models import PriceData
import pandas as pd
from django.utils.translation import gettext_lazy as _

# Register your models here.

class PriceDataImportForm(forms.Form):
    file = forms.FileField(label=_("엑셀 파일 선택"))

@admin.register(PriceData)
class PriceDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'asset_type', 'price')
    list_filter = ('asset_type',)
    search_fields = ('date',)
    ordering = ('-date',)
    change_list_template = 'admin/price_import.html'
    
    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            form = PriceDataImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    df = pd.read_excel(request.FILES['file'])
                    column_map = {
                        'date': ['Date', '날짜', 'date'],
                        'asset_type': ['Asset', '자산종류', 'asset_type'],
                        'price': ['Price', '가격', 'price']
                    }
                    
                    actual_columns = {}
                    for field, possible_names in column_map.items():
                        for name in possible_names:
                            if name in df.columns:
                                actual_columns[field] = name
                                break
                        else:
                            self.message_user(request, 
                                _("'{field}' 컬럼을 찾을 수 없습니다.").format(field=field), 
                                level='error'
                            )
                            return super().changelist_view(request, extra_context)
                    
                    error_log = []
                    for index, row in df.iterrows():
                        try:
                            date = pd.to_datetime(row[actual_columns['date']]).date()
                            asset_type = str(row[actual_columns['asset_type']]).upper()
                            price_str = str(row[actual_columns['price']]).replace(',','').replace('$','').strip()
                            price = float(price_str)
                            
                            PriceData.objects.update_or_create(
                                date=date,
                                asset_type=asset_type,
                                defaults={'price': price}
                            )
                        except Exception as e:
                            error_log.append(_("{row}행 오류: {error}").format(row=index+2, error=str(e)))
                    
                    if error_log:
                        self.message_user(request, "\n".join(error_log[:10]), level='error')
                    else:
                        self.message_user(request, _("성공적으로 {count}건 데이터를 임포트했습니다.").format(count=len(df)))
                        
                except Exception as e:
                    self.message_user(request, _("파일 처리 오류: {error}").format(error=str(e)), level='error')
                    
        return super().changelist_view(request, extra_context)
