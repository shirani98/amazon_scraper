from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

    def fetch_data(self, product_id):
        pass

    def get_cache_data(self, product_id):
        pass

    def get_database_data(self, product_id):
        pass

    def scrape_amazon(self, product_id):
        pass