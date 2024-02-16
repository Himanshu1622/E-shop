from django.shortcuts import render
from django.contrib import messages , auth
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
from .models import *

# Create your views here.
def home(request):
    product = Product.objects.all()
    product = product[::-1]
    context = {"title":"E shop","product": product}
    return render(request, 'home.html',context)


def shop(request,mc,sc,br):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    # Logic for products 
    if(mc=='all' and sc=='all' and br=='all'):
        product = Product.objects.all()
    elif(mc!='all' and sc=='all' and br=='all'):
        product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc))
    elif(mc=='all' and sc!='all' and br=='all'):
        product = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc))
    elif(mc=='all' and sc=='all' and br!='all'):
        product = Product.objects.filter(brand=Brand.objects.get(name=br))
    elif(mc!='all' and sc!='all' and br=='all'):
        product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc))
    elif(mc!='all' and sc=='all' and br!='all'):
        product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br))
    elif(mc=='all' and sc!='all' and br!='all'):
        product = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))
    else:
        product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))
    
    product = product[::-1]
    context = {"title":"Shop","product": product, "Maincategory":maincategory , "Subcategory" : subcategory , "Brand" : brand, "mc":mc, "sc":sc, "br":br}
    return render(request, 'shop.html',context)


def login(request):
    if(request.method=="POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username , password = password)
        if(user is not None):
            # auth is built in module for authenticate purpose which take 2 paramenter one is request and other is user details
            auth.login(request , user)
            if(user.is_superuser):
                return redirect('/admin/')
            else:
                return redirect('/profile/')
        else:
            messages.error(request, "Invalid Credentials")
    context = {"title":"Login"}
    return render(request, 'login.html',context)


def signup(request):
    if(request.method == "POST"):
        actype = request.POST.get('actype')
        if(actype=='seller'):
            # Here u variable is stand for both buyer and seller
            u = Seller()
        else: 
            u = Buyer()
        u.name = request.POST.get('name')
        u.username = request.POST.get('username')
        u.email = request.POST.get('email')
        u.phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if(password == cpassword):
            try:
                # here we user built in method of django (User) here we add minimum 2 parameters and create_user which is built in django for User 
                user = User.objects.create_user(username=u.username , password=password)
                u.save()
                return redirect('/login/')
            except:
                messages.error(request, "Username is already Taken")
        else:
            messages.error(request, "password and confirm password does not match")

    context = {"title":"Signup"}
    return render(request, 'signup.html',context)


@login_required(login_url='/login/')
def profile(request):
    user = User.objects.get(username = request.user)
    if(user.is_superuser):
        return redirect('/admin/')
    else:
       try:
        seller = Seller.objects.get(username = request.user)
        products = Product.objects.filter(seller=seller)
        products = products[::-1]
        return render(request, 'sellerProfile.html', {"user":seller, "product": products , "title": "Seller Profile"})

       except:
        buyer = Buyer.objects.get(username = request.user)
        wishlist = Wishlist.objects.filter(buyer = buyer)
        return render(request, 'buyerProfile.html', {"user":buyer, "wishlist":wishlist, "title": "Buyer Profile"})
        

@login_required(login_url='/login/')
def updateProfile(request):
    user = User.objects.get(username = request.user)
    if(user.is_superuser):
        return redirect('/admin/')
    else:
        try:
            # Here u variable is stand for both buyer and seller
            u = Seller.objects.get(username = request.user)
        except:
            u = Buyer.objects.get(username = request.user)
        if(request.method=='POST'):
            u.name = request.POST.get('name')
            u.email = request.POST.get('email')
            u.phone = request.POST.get('phone')
            u.address = request.POST.get('address')
            u.pincode = request.POST.get('pincode')
            u.city = request.POST.get('city')
            u.state = request.POST.get('state')
            if(request.FILES.get('pic')):
                # os line remove the last image which store in folder where images store
                if(u.pic):
                    os.remove("media/"+str(u.pic))
                u.pic = request.FILES.get('pic')
            u.save()
            return redirect('/profile/')

    return render(request, 'updateProfile.html', {"user" : u , "title" : "Update Profile"})


@login_required(login_url='/login/')
def addProduct(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    context = {"title" : "Add Product", "Maincategory":maincategory , "Subcategory" : subcategory , "Brand" : brand}
    if(request.method=="POST"):
        product = Product()
        product.name = request.POST.get('name')
        product.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
        product.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
        product.brand = Brand.objects.get(name=request.POST.get('brand'))
        product.stock = request.POST.get('stock')
        product.baseprice = int(request.POST.get('baseprice'))
        product.discount = int(request.POST.get('discount'))
        product.finalprice = product.baseprice - product.baseprice*product.discount/100
        color =''
        if (request.POST.get('Red')):
            color = color + 'Red,'
        if (request.POST.get('Green')):
            color = color + 'Green,'
        if (request.POST.get('Yellow')):
            color = color + 'Yellow,'
        if (request.POST.get('Pink')):
            color = color + 'Pink,'
        if (request.POST.get('White')):
            color = color + 'White,'
        if (request.POST.get('Black')):
            color = color + 'Black,'
        if (request.POST.get('Blue')):
            color = color + 'Blue,'
        if (request.POST.get('Brown')):
            color = color + 'Brown,'
        if (request.POST.get('SkyBlue')):
            color = color + 'SkyBlue,'
        if (request.POST.get('Orange')):
            color = color + 'Orange,'
        if (request.POST.get('Navy')):
            color = color + 'Navy,'
        if (request.POST.get('Gray')):
            color = color + 'Gray,'
        product.color = color
        # product.color = request.POST.get('color')
        # product.size = request.POST.get('size')
        size = ''
        if (request.POST.get('S')):
            size = size + 'S'
        if (request.POST.get('SM')):
            size = size + 'SM'
        if (request.POST.get('M')):
            size = size + 'M'
        if (request.POST.get('L')):
            size = size + 'L'
        if (request.POST.get('XL')):
            size = size + 'XL'
        if (request.POST.get('XXL')):
            size = size + 'XXL'
        if (request.POST.get('XXXL')):
            size = size + 'XXXL'
        product.size = size
        product.description = request.POST.get('description')
        product.pic1 = request.FILES.get('pic1')
        product.pic2 = request.FILES.get('pic2')
        product.pic3 = request.FILES.get('pic3')
        try:
            product.seller = Seller.objects.get(username= request.user)
        except:
            return redirect('/profile/')
        product.save()
        return redirect("/profile/")
    return render(request, 'addProducts.html', context)


# here item is use for to get the product you can write anything here like id 
@login_required(login_url='/login/')
def deleteProduct(request, item):
    try:
        product = Product.objects.get(id = item)
        seller = Seller.objects.get(username = request.user)
        if(product.seller == seller):
            product.delete()
        return redirect('/profile/')
    except:
        return redirect('/profile/')
    

@login_required(login_url='/login/')
def UpdateProduct(request, item):
    try:
        product = Product.objects.get(id = item)
        seller = Seller.objects.get(username = request.user)
        # here exclude use cause we dont need that Category agian
        maincategory = Maincategory.objects.exclude(name= product.maincategory)
        subcategory = Subcategory.objects.exclude(name= product.subcategory)
        brand = Brand.objects.exclude(name= product.brand)
        context = {'title':'Update-Product','product':product, "Maincategory":maincategory, "Subcategory":subcategory, "Brand":brand}
        if(request.method == "POST"):
            product.name = request.POST.get('name')
            product.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
            product.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
            product.brand = Brand.objects.get(name=request.POST.get('brand'))
            product.stock = request.POST.get('stock')
            product.baseprice = int(request.POST.get('baseprice'))
            product.discount = int(request.POST.get('discount'))
            product.finalprice = product.baseprice - product.baseprice*product.discount/100
            color =''
            if (request.POST.get('Red')):
                color = color + 'Red,'
            if (request.POST.get('Green')):
                color = color + 'Green,'
            if (request.POST.get('Yellow')):
                color = color + 'Yellow,'
            if (request.POST.get('Pink')):
                color = color + 'Pink,'
            if (request.POST.get('White')):
                color = color + 'White,'
            if (request.POST.get('Black')):
                color = color + 'Black,'
            if (request.POST.get('Blue')):
                color = color + 'Blue,'
            if (request.POST.get('Brown')):
                color = color + 'Brown,'
            if (request.POST.get('SkyBlue')):
                color = color + 'SkyBlue,'
            if (request.POST.get('Orange')):
                color = color + 'Orange,'
            if (request.POST.get('Navy')):
                color = color + 'Navy,'
            if (request.POST.get('Gray')):
                color = color + 'Gray,'
            product.color = color
            # product.color = request.POST.get('color')
            # product.size = request.POST.get('size')
            size = ''
            if (request.POST.get('S')):
                size = size + 'S,'
            if (request.POST.get('SM')):
                size = size + 'SM,'
            if (request.POST.get('M')):
                size = size + 'M,'
            if (request.POST.get('L')):
                size = size + 'L,'
            if (request.POST.get('XL')):
                size = size + 'XL,'
            if (request.POST.get('XXL')):
                size = size + 'XXL,'
            if (request.POST.get('XXXL')):
                size = size + 'XXXL,'
            product.size = size
            # product.color = request.POST.get('color')
            # product.size = request.POST.get('size')
            product.description = request.POST.get('description')
            if(request.FILES.get('pic1')):
                if(product.pic1):
                    os.remove('media/'+str(product.pic1))
                product.pic1 = request.FILES.get('pic1')

            if(request.FILES.get('pic2')):
                if(product.pic2):
                    os.remove('media/'+str(product.pic2))
                product.pic2 = request.FILES.get('pic2')

            if(request.FILES.get('pic3')):
                if(product.pic3):
                    os.remove('media/'+str(product.pic1))
                product.pic3 = request.FILES.get('pic3')
            product.save()
            return redirect('/profile/')
        if(product.seller == seller):
           return render(request, 'productUpdate.html', context)
    except:
        return redirect('/profile/')


def singleProduct(request, id):
    product = Product.objects.get(id = id)
    color = product.color.split(',')
    color = color[:-1]
    size = product.size.split(',')
    size = size[:-1]
    context = {'title': 'Product Page','product': product,"color":color, "size":size}
    return render(request , "singleProduct.html",context)  

def wishList(request , id):
    try:
        buyer = Buyer.objects.get(username = request.user)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        product = Product.objects.get(id = id)
        item = False 
        for i in wishlist:
            if(i.product == product):
                item = True
                break
        if(item == False ):
            wishlist = Wishlist()
            wishlist.buyer = buyer
            wishlist.product = product
            wishlist.save()
        return redirect("/profile/")
    except:
        return redirect("/profile/")


@login_required(login_url='/login/')
def deleteWishlist(request, id):
    try:
        wishlist = Wishlist.objects.get(id = id)
        buyer = Buyer.objects.get(username = request.user)
        if(wishlist.buyer == buyer):
            wishlist.delete()
        return redirect('/profile/')
    except:
        return redirect('/profile/')


def logout(request):
    auth.logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def addToCart(request):
    pid = request.POST.get('pid')
    color = request.POST.get('color')
    size = request.POST.get('size')
    cart = request.session.get("cart",None)
    if(cart):
        if(pid in cart.keys() and color==cart[pid][1] and size==cart[pid][2]):
            pass
        else:
            count = len(cart.keys())
            count=count+1
            cart.setdefault(str(count),[pid,1,color,size])  
    else:
        cart = {"1":[pid,1,color,size]}
    
    request.session['cart']=cart
    return redirect('/cart/')


def Cart(request):
    cart = request.session.get("cart",None)
    total = 0
    shipping = 0
    final = 0
    if(cart):
        for value in cart.values():
            p = Product.objects.get(id=int(value[0]))
            total= total + p.finalprice
        if(len(cart.values()) >=1 and total<1000):
            shipping=150
        final=total+shipping

    return render(request,"cart.html",{'title': 'Cart',"Cart":cart,"Total":total,"Shipping":shipping,"Final":final})