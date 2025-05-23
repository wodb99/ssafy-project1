from django.core.management.base import BaseCommand
from golds.models import PriceData
import pandas as pd

class Command(BaseCommand):
    help = '엑셀 파일에서 가격 데이터 가져오기 (금/은 따로)'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='엑셀 파일 경로')
        parser.add_argument('asset_type', type=str, help='자산 종류(GOLD/SILVER)')

    def handle(self, *args, **options):
        file_path = options['file_path']
        asset_type = options['asset_type'].upper()
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            date = row['Date']
            price_str = str(row['Close/Last']).replace(',', '').replace('$', '').strip()
            try:
                price = float(price_str)
            except ValueError:
                continue
            PriceData.objects.update_or_create(
                date=date,
                asset_type=asset_type,
                defaults={'price': price}
            )
        self.stdout.write(self.style.SUCCESS(f'{asset_type} 데이터 임포트 완료!'))
