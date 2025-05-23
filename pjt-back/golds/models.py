from django.db import models

# Create your models here.
class PriceData(models.Model):
    ASSET_TYPES = (
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver')
    )
    
    date = models.DateField(verbose_name='날짜')
    asset_type = models.CharField(
        max_length=10, 
        choices=ASSET_TYPES,
        verbose_name='자산 종류'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='가격'
    )

    class Meta:
        indexes = [
            models.Index(fields=['date', 'asset_type'])
        ]
