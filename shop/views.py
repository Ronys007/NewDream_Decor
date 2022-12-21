from multiprocessing import context
from os import remove
from django.views.generic import View
from unicodedata import category
from django.http import HttpResponse, JsonResponse
from .models import Product, Order, OrderItem, ContactForm
from .models import Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .cart import Cart
from .forms import CartAddProductForm
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
import random
from django.db.models import Min, Max
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

def home(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
        
    #return render(request, 'home.html', {'cart': cart})
    if bedding:
        products = Product.objects.filter(category=4)
        return render(request, 'home.html', {'product': products, 'category': 4, 'cart': cart})


def bedroom(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    if bedroom: 
        products = Product.objects.filter(category=1)
        return render(request, 'bedroom.html', {'product': products, 'category': 1, 'cart': cart})
  
    
        


def livingroom(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    if livingroom:
        products = Product.objects.filter(category=2)
        return render(request, 'livingroom.html', {'product': products, 'category': 2, 'cart': cart})


def diningroom(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    if diningroom:
        products = Product.objects.filter(category=3)
        return render(request, 'diningroom.html', {'product': products, 'category': 3, 'cart': cart})


def bedding(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    if bedding:
        products = Product.objects.filter(category=4)
        return render(request, 'bedding.html', {'product': products, 'category': 4, 'cart': cart})


def youth(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    if youth:
        products = Product.objects.filter(category=5)
        return render(request, 'youth.html', {'product': products, 'category': 5, 'cart': cart})


def newarrival(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    products = Product.objects.all().order_by('-pub_date')
    return render(request, 'newarrival.html', {'product': products, 'cart': cart})


def login(request):
    return render(request, 'login.html')


def signup(request):

    if request.method == "POST":
        # Get the Post Parameter
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("signup")
            else:
                # Create User
                user = User.objects.create_user(username=username,
                                                first_name=first_name, last_name=last_name, email=email, password=password1)
                user.save()
                
                subject = 'Welcome to Dream Decor'
                message = f'Hi {user.username}, thank you for registering in Dream Decor.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return redirect("login")

        else:
            messages.info(request, "Password not matching")
            return redirect("signup")

    else:
        return render(request, 'signup.html')
    


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect("home")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("login")

    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("home")


def product(request, id):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    products = Product.objects.filter(id=id)
    cart_product_form = CartAddProductForm()
    return render(request, 'product.html', {'product': products, 'cart_product_form': cart_product_form, 'cart': cart})


@require_POST
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart_detail')


def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        neworder = Order()
        current_user = request.user
        neworder.user = User.objects.get(id=current_user.id)
        neworder.name = request.POST.get('name')
        neworder.address = request.POST.get('address')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.zip_code = request.POST.get('zip_code')

        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart(request)
        cart.get_total_price=0
        for item in cart:
            cart.get_total_price = cart.get_total_price + item['price']*item['quantity']

            neworder.total_price = cart.get_total_price
            trackingno = 'DreamDecor_' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackingno) is None:
                trackingno = 'DreamDecor_' + \
                    str(random.randint(1111111, 9999999))

            neworder.tracking_no = trackingno
            neworder.save()
            neworderitems = Cart(request)
            for item in neworderitems:
                OrderItem.objects.create(order=neworder,
                                         product=item['product'],
                                         price=item['total_price'],
                                         quantity=item['quantity'])

            cart.clear()
            template = get_template('cart/invoice.html')
            data = {
                        'order_id': str(neworder.id),
                        'user_email': neworder.email,
                        'date': str(neworder.created_at),
                        'name': neworder.name,
                        'order': neworder,
                        'amount': neworder.total_price,
                    }
            html  = template.render(data)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
            pdf = result.getvalue()
            filename = 'Invoice_' + data['order_id'] + '.pdf'

            mail_subject = 'Recent Order Details'
                    # message = render_to_string('firstapp/payment/emailinvoice.html', {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # })
            context_dict = {
                        'user': neworder.user,
                        'order': neworder
                    }
            template = get_template('cart/email.html')
            message  = template.render(context_dict)
            to_email = neworder.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
            email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email],['gauravbdevil@gmail.com']
                    )
            email.attach_alternative(message, "text/html")
            email.attach(filename, pdf, 'application/pdf')
            email.send(fail_silently=False)
            
        messages.info(request, "Your Order has been successfully placed.")
        return redirect('/cart_detail')


@csrf_exempt
def payment_done(request):
    return render(request, 'paypal/payment_done.html')


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'paypal/payment_cancelled.html')


def payment_process(request):
    return render(request, 'paypal/payment_process.html')


def order(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'cart/order.html', context)


def orderview(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(
        user=request.user).first()
    orderitem = OrderItem.objects.filter(order=order)
    context = {'order': order, 'orderitem': orderitem}
    return render(request, 'cart/orderview.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        newcontact = ContactForm()
        current_user = request.user
        newcontact.user = User.objects.get(id=current_user.id)
        newcontact.name = request.POST.get('name')
        newcontact.phone = request.POST.get('phone')
        newcontact.email = request.POST.get('email')
        newcontact.phone = request.POST.get('phone')
        newcontact.subject = request.POST.get('subject')
        newcontact.message = request.POST.get('message')
        newcontact.save()

        messages.success(request, "Thank You for contacting us.")
    return render(request, 'contact.html')

def warranty(request):
    return render(request, 'warranty.html')

def shippingpolicy(request):
    return render(request, 'shippingpolicy.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def termsandpolicy(request):
    return render(request, 'termsandpolicy.html')

def tracking(request):
    return render(request, 'tracking.html')


# for generating pdf invoice
def fetch_resources(uri):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class GenerateInvoice(View):
    def get(self, request, id, *args, **kwargs):
        try:
            order_db = Order.objects.get(id = id, user = request.user)     #you can filter using order_id as well
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.id,
            'transaction_id': order_db.payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.updated_at),
            'name': order_db.name,
            'order': order_db,
            'amount': order_db.total_price,
        }
        pdf = render_to_pdf('cart/invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

