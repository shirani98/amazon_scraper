from django.db import models
import redis
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
from decimal import Decimal


class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField(max_length=10)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

    @classmethod
    def fetch_data(cls, product_id):
        cache_data = cls.get_cache_data(product_id)
        if cache_data:
            return cache_data
        db_data = cls.get_database_data(product_id)
        if db_data:
            return db_data
        scrape_data = cls.scrape_data(product_id)
        if scrape_data:
            return scrape_data
        return None

    @classmethod
    def get_cache_data(cls, product_id):
        redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
        cached_data = redis_client.get(f"product_{product_id}")
        if cached_data:
            return json.loads(cached_data)
        return None

    @classmethod
    def get_database_data(cls, product_id):
        try:
            product = cls.objects.get(id=product_id)
            return {
                "id": product_id,
                "name": product.name,
                "price": product.price,
                "rating": product.rating,
                "average_rating": product.average_rating,
            }
        except Exception:
            return None

    @classmethod
    def scrape_data(cls, product_id):
        chrome_driver_path = "/usr/bin/chromedriver"
        product_url = f"https://www.amazon.com/dp/{product_id}"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        driver.get(product_url)
        product_name = driver.find_element(By.ID, "productTitle").text.strip()
        price_element = driver.find_element(By.XPATH, '//*[@class="a-offscreen"]')
        product_price = driver.execute_script(
            "return arguments[0].textContent;", price_element
        )[1:]
        product_rating = driver.find_element(
            By.ID, "acrCustomerReviewText"
        ).text.split()[0]
        product_average_rating = (
            driver.find_element(By.ID, "acrPopover").get_attribute("title").split()[0]
        )
        scraped_data = {
            "id": product_id,
            "name": product_name,
            "price": float(product_price),
            "rating": float(product_rating.replace(",", "")),
            "average_rating": float(product_average_rating),
        }
        cls.objects.create(
            id=product_id,
            name=product_name,
            price=Decimal(product_price),
            rating=int(product_rating.replace(",", "")),
            average_rating=Decimal(product_average_rating),
        )
        redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
        redis_client.set(f"product_{product_id}", json.dumps(scraped_data))
        return scraped_data
