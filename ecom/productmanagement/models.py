from django.db import models
from categorymanagement.models import Brand
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps


class Product(models.Model):
    CATEGORY_CHOICES = [("men", "Men"), ("women", "Women"), ("all", "ALL")]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="all")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    image1 = models.ImageField(upload_to="media/images/", blank=True)
    is_listed = models.BooleanField(default=True)
    discount_percentage = models.DecimalField(
        max_digits=3, decimal_places=0, default=0, null=True, blank=True
    )

    def offer_price(self):
        # from coupon.models import ProductOffer,BrandOffer
        # import models using apps to avoid circular dependency
        BrandOffer = apps.get_model("coupon", "BrandOffer")
        ProductOffer = apps.get_model("coupon", "ProductOffer")
        product_offers = ProductOffer.objects.filter(product=self, is_active=True)
        brand_offers = BrandOffer.objects.filter(brand=self.brand, is_active=True)

        if product_offers.exists() and brand_offers.exists():
            max_prod_offer = max(offer.offer_percentage for offer in product_offers)
            max_brand_offer = max(offer.offer_percentage for offer in brand_offers)
            max_offer = max(max_brand_offer, max_prod_offer)
        elif product_offers.exists():
            max_offer = max(offer.offer_percentage for offer in product_offers)
        elif brand_offers.exists():
            max_offer = max(offer.offer_percentage for offer in brand_offers)
        else:
            discount_percentage = round(
                (
                    (int(self.original_price) - int(self.selling_price))
                    / float(self.original_price)
                )
                * 100
            )
            return self.selling_price, discount_percentage

        offer_price = round(int(self.selling_price) * (1 - max_offer / 100), 2)
        discount_percentage = round(
            ((int(self.original_price) - offer_price) / float(self.original_price))
            * 100
        )
        return offer_price, discount_percentage

    def __str__(self) -> str:
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    images = models.ImageField(upload_to="media/images/")
    image_number = models.PositiveIntegerField(blank=True)

    def __str__(self) -> str:
        return f"{self.product.name}'s Image-{self.image_number}"

@receiver(pre_save, sender=Product)
def calc_discount_percentage(sender, instance, **kwargs):
    if not instance.discount_percentage:
        og = float(instance.original_price)
        sp = float(instance.selling_price)
        instance.discount_percentage = round(((og - sp) / og) * 100)


class ProductVariant(models.Model):
    SIZE_CHOICES = [(7, "7"), (8, "8"), (9, "9"), (10, "10")]
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(
        max_length=5, choices=SIZE_CHOICES, null=True, blank=True, default="7"
    )
    stock = models.PositiveIntegerField(default=0, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True, default="white")

    def __str__(self) -> str:
        return f" {self.product_id.brand.brand_name}  {self.product_id.name}-({self.size}) " 