from django.db import models
from django.db.models.deletion import CASCADE

class ProductList(models.Model):
    completed = models.BooleanField()
    product = models.ForeignKey("Product", 
        on_delete=CASCADE,
        related_name="productlists",
        related_query_name="productlist")
    shopper = models.ForeignKey("Shopper", 
        on_delete=CASCADE,
        related_name="productlists",
        related_query_name="productlist")
    location = models.ForeignKey("Location", 
        on_delete=CASCADE,
        related_name="productlists",
        related_query_name="productlist")

    '''
    Create & Test after URLs and Views are created:

    @property
    def sum_total(self):
        Write a function that loops through each product in the ProductList and adds the price to the next product. A `sum_total` variable with the end total should be returned.
        You will need to import `Product` in and grab all Products that's `id` matches a `product_id` in the ProductList model.
    '''
