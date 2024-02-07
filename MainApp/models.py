from django.db import models

class Maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100 , default=None , null=True, blank=True)
    pincode = models.CharField(max_length=20 , default=None , null=True, blank=True)
    city = models.CharField(max_length=50 , default=None , null=True, blank=True)
    state = models.CharField(max_length=50 , default=None , null=True, blank=True)
    pic = models.ImageField(upload_to='images' , default=None , null=True, blank=True)

    def __str__(self):
        return str(self.id)+" - "+self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    maincategory = models.ForeignKey(Maincategory , on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory , on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand , on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE , default=None)
    baseprice = models.IntegerField()
    discount = models.IntegerField()
    finalprice = models.IntegerField()
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.CharField(max_length=20 , default='In Stock')
    pic1 = models.ImageField(upload_to='images')
    pic2 = models.ImageField(upload_to='images', default=None , null=True, blank=True)
    pic3 = models.ImageField(upload_to='images', default=None , null=True, blank=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100 , default=None , null=True, blank=True)
    pincode = models.CharField(max_length=20 , default=None , null=True, blank=True)
    city = models.CharField(max_length=50 , default=None , null=True, blank=True)
    state = models.CharField(max_length=50 , default=None , null=True, blank=True)
    pic = models.ImageField(upload_to='images' , default=None , null=True, blank=True)

    def __str__(self):
        return str(self.id)+" "+self.name