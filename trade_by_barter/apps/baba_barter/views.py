from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import SwappableAddress, User, Swappable, SubCategory, SwappableFlagImage, \
    Category, UserImage, SwappableImage, UserFlag, UserFlagImage, SwappableFlag
import bcrypt
from PIL import Image

def image(request):
    return render(request, 'baba_barter/image_test.html')
  
def process_image(request):
    img = Image.open("apps/baba_barter/static/baba_barter/yofte-assets/images/cupz.png")
    #img = Image.open(request.POST['image'])
    img = img.convert("RGBA")
  
    datas = img.getdata()
  
    newData = []
  
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
  
    img.putdata(newData)
    img.save("nncupzz.png", "PNG")
    context = {
        'image': img
    }
    return redirect(reverse('baba:image'))

def intro(request):
    if 'user_id' in request.session:
        return redirect(reverse('baba:home', kwargs={'id':request.session['user_id']}))
    return render(request, 'baba_barter/intro.html')

def signup(request):
    return render(request, 'baba_barter/signup.html')

#TODO implement has paid'
#is deleted ...
def process_signup(request):
    if request.method == 'POST':
        errors =  User.objects.signup_validations(request.POST)
        if len(errors):
            for k, v in errors.items():
                messages.error(request, v, extra_tags=k)
            return redirect(reverse('baba:signup'))
        else:
            user_password_hash = bcrypt.hashpw(request.POST['signup_password_input'].encode("utf-8"), bcrypt.gensalt())
            user = User(first_name=request.POST['signup_first_name_input'], last_name=request.POST['signup_last_name_input'], 
                email=request.POST['signup_email_input'], password_hash=user_password_hash, token_count=0, has_paid=True,
                date_of_birth=request.POST['signup_date_of_birth_input'], description=request.POST['signup_description_input']
            )
            user.save()
            image_name = f"{request.POST['signup_first_name_input']} {request.POST['signup_last_name_input']}`s Profile Picture"
            image = UserImage(name=image_name, image=request.FILES['signup_image_input'], user=user)
            image.save()
            mail_subject = "Activate your Baba Barter account."
            html = 'acc_active_email.html'
            send_activation_email(request, user, request.POST['signup_email_input'], html, mail_subject)
            return HttpResponse('Click the link in your email to activate your account')
    return redirect(reverse('baba:signup'))

def send_activation_email(request, user, email_input, html, mail_subject):
    current_site = get_current_site(request)
    mail_subject = mail_subject
    print(urlsafe_base64_encode(force_bytes(user.id)))
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    }
    message = render_to_string(f'baba_barter/{html}', context)
    email = EmailMessage(mail_subject, message, to=[email_input])
    email.send()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_authenticated = True
        user.save()
        messages.success(request, f'Successful Sign Up', extra_tags='signup_success')
        request.session['user_id'] = str(user.id)
        return redirect(reverse('baba:home', kwargs={'id':request.session['user_id']}))
    else:
        return HttpResponse('Activation link is invalid!')

def process_signin(request):
    if request.method == 'POST':
        errors =  User.objects.signin_validations(request.POST)
        if len(errors):
            for k, v in errors.items():
                messages.error(request, v, extra_tags=k)
            return redirect(reverse('baba:signin'))
        else:
            user = User.objects.filter(email=request.POST['signin_email_input'])[0]
            if user.is_authenticated == True:
                request.session['user_id'] = str(user.id)
                messages.success(request, f'Successful Sign In', extra_tags='signin_success')
                return redirect(reverse('baba:home', kwargs={'id':request.session['user_id']}))
            else:
                current_site = get_current_site(request)
                mail_subject = "Activate your Baba Barter account."
                context = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
                    'token': account_activation_token.make_token(user),
                }
                message = render_to_string('baba_barter/acc_active_email.html', context)
                email = EmailMessage(mail_subject, message, to=[request.POST['signin_email_input']])
                email.send()
                return HttpResponse('Click the link in your email to activate your account')
    else:
        return redirect(reverse('baba:signin'))

def signin(request):
    return render(request, 'baba_barter/signin.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect(reverse('baba:intro'))

#TODO allow users to view other profiles
#if id=session[id], show edit profle link, else, hide it
def show_user(request, id):
    if 'user_id' in request.session:
        #Use user information for navbar
        #User's id = session[user_id]
        user = User.objects.filter(id=request.session['user_id'])[0]
        context = {
            'user': User.objects.filter(id=request.session['user_id'])[0],
            'user_image': UserImage.objects.filter(user=user)[0],
            'user_swappable_count': str(Swappable.objects.filter(user__id=request.session['user_id']).count())
        }
        #If user is visiting another user, get information of visited user
        #Visited user's id = id^
        if request.session['user_id'] != id:
            visited_user = User.objects.filter(id=id)
            if len(visited_user) > 0:
                visited_user = visited_user[0]
                context['visited_user'] = visited_user
                context['visited_user_image'] = UserImage.objects.filter(user=visited_user)[0]
                context['visited_user_swappable_count'] = str(Swappable.objects.filter(user__id=id).count())
        return render(request, 'baba_barter/user_profile.html', context)
    return redirect(reverse('baba:intro')) 

@csrf_exempt
def edit_profile(request, id):
    if 'user_id' in request.session:
        if str(request.session['user_id']) == str(id):
            context = {
                'user': User.objects.filter(id=request.session['user_id'])[0]
            }
            return render(request, 'baba_barter/edit_profile.html', context)
        return redirect(reverse('baba:edit_profile', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

def process_edit_profile(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0:
            if request.method == 'POST':
                errors =  User.objects.edit_profile_validations(request.POST, request)
                if len(errors):
                    for k, v in errors.items():
                        messages.error(request, v, extra_tags=k)
                    return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
                else:
                    user = user[0]
                    user.first_name = request.POST['edit_first_name']
                    user.last_name = request.POST['edit_last_name']
                    user.description = request.POST['edit_description']
                    email = user.email
                    user.gender = request.POST['edit_gender']
                    user.password_hash = bcrypt.hashpw(request.POST['edit_new_password'].encode(), bcrypt.gensalt())
                    user.save()
                    if request.POST['edit_email'] != email:
                        user.email = request.POST['edit_email']
                        user.save()
                        current_site = get_current_site(request)
                        mail_subject = "Activate your new Baba Barter email."
                        context = {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
                            'token': account_activation_token.make_token(user),
                        }
                        message = render_to_string('baba_barter/acc_new_email.html', context)
                        email = EmailMessage(mail_subject, message, to=[request.POST['edit_email']])
                        email.send()
                        return HttpResponse('Click the link in your email to confirm your new email address')
                    messages.success(request, f'Profile editted successfully', extra_tags='edit_user_sucess')
                    return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
            return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

def activate_new_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        messages.success(request, f'Profile editted successfully', extra_tags='edit_user_sucess')
        return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
    else:
        return HttpResponse('Activation link is invalid!')

#TODO add swappables and (sub)categories 
#TODO change main to true
def swappables(request, id):
    if 'user_id' in request.session:
        owner = False
        if str(id) == str(request.session['user_id']): owner = True
        swappables = Swappable.objects.filter(user__id=id)
        swappable_images = SwappableImage.objects.filter(swappable__user__id=id, main=True)
        both = zip(swappables, swappable_images)
        user_image = UserImage.objects.filter(user__id=request.session['user_id'])
        user = User.objects.filter(id=request.session['user_id'])
        visited_user = User.objects.filter(id=id)[0]
        value_swappables = swappables.order_by('-value')
        max_value = 0
        if len(value_swappables) > 0:
            max_value = value_swappables[0].value
        else: max_value = 1000
        if len(user_image) > 0 and len(user) > 0:
            context = {
                'user': user[0],
                'user_image': user_image[0],
                'both': both,
                'swappables': Swappable.objects.filter(user__id=id),
                'swappable_images': SwappableImage.objects.filter(swappable__user__id=id, main=True),
                'owner': owner,
                'visited_user': visited_user,
                'max_value': max_value
            }
            return render(request, 'baba_barter/swappables.html', context)
        return redirect(reverse('baba:intro'))
    return redirect(reverse('baba:intro'))

#TODO add security measure like edit_profile
def create_swappable(request, id):
    if 'user_id' in request.session:
        context = {}
        if str(id) == str(request.session['user_id']):
            context['user'] = User.objects.filter(id=id)[0]
        else:
            context['user'] = User.objects.filter(id=request.session['user_id'])[0]
        return render(request, 'baba_barter/create_swappable.html', context)
    return redirect(reverse('baba:intro'))

#TODO implement from is_deleted -- is_banned
#TODO value f"{num:,}"
def register_swappable(request, id):
    if 'user_id' in request.session:
        if id == request.session['user_id']:
            if request.method == 'POST':
                errors =  {**Swappable.objects.swappable_validations(request.POST), **Swappable.objects.validate_images(request.FILES), **SwappableAddress.objects.swappable_address_validations(request.POST)}
                if len(errors):
                    for k, v in errors.items():
                        messages.error(request, v, extra_tags=k)
                    return redirect(reverse('baba:create_swappable', kwargs={'id':request.session['user_id']}))
                else:
                    user = User.objects.filter(id=request.session['user_id'])[0]
                    category = Category.objects.filter(name=request.POST['category'])
                    if len(category) < 1:
                        category = Category(name=request.POST['category'])
                        category.save()
                        category.users.add(user)
                        category.save()
                    else:
                        category = category[0]
                        category.users.add(user)
                        category.save()
                    swappable = Swappable(name=request.POST['name'], type=request.POST['type'], user=user,
                        category=category, short_description=request.POST['short_description'], 
                        long_description=request.POST['long_description'], notes=request.POST['notes'], 
                        value=request.POST['value'], currency=request.POST['currency'], condition=request.POST['condition'])
                    swappable.save()
                    sub_categories = request.POST['sub_categories'].split(",")
                    for s in sub_categories:
                        sub_c = SubCategory(name=s, category=category)
                        sub_c.save()
                        swappable.sub_categories.add(sub_c)
                    swappable.save()
                    i = 0
                    for img in request.FILES.getlist('images'):
                        image_name = f"{request.POST['name']}-{i}"
                        main = True if i==0 else False
                        image = SwappableImage(name=image_name, image=img, swappable=swappable, main=main)
                        image.save()
                        i+=1
                    SwappableAddress.objects.create(swappable=swappable, city=request.POST['city'], 
                        code=request.POST['code'], state=request.POST['state'], country=request.POST['country'])
                    messages.success(request, f'Swappable created successfully', extra_tags='swappable_creation_sucess')
                    return redirect(reverse('baba:swappables', kwargs={'id':request.session['user_id']}))
        return redirect(reverse('baba:create_swappable', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

def show_swappable(request, id):
    if 'user_id' in request.session:
        edit = False
        user = User.objects.filter(id=request.session['user_id'])[0]
        swappable = Swappable.objects.filter(id=id)
        if len(swappable) > 0: 
            swappable = swappable[0]
            swappable_images = SwappableImage.objects.filter(swappable__id=id)
            user_image = UserImage.objects.filter(user__id=user.id)[0]
            if swappable.user == user:
                edit = True
            location = SwappableAddress.objects.filter(swappable=swappable)
            if len(location) > 0:
                location = location[0]
            context = {
                "swappable": swappable,
                "user": user,
                "edit": edit,
                'swappable_images': swappable_images,
                'user_image': user_image,
                'location': location
            }
            return render(request, 'baba_barter/show_swappable.html', context)
    return redirect(reverse('baba:intro'))

def edit_swappable(request, id):
    if 'user_id' in request.session:
        if len(Swappable.objects.filter(id=id)) > 0:
            swappable = Swappable.objects.filter(id=id)[0]
            swappable_images = SwappableImage.objects.filter(swappable__id=id)
            user = swappable.user
            if str(user.id) == request.session['user_id']:
                swappable_sub_categories = swappable.sub_categories.all().values()
                sub_categories = ""
                for i in range(0, len(swappable_sub_categories)):
                    if i == len(swappable_sub_categories) - 1:
                        sub_categories += swappable_sub_categories[i]['name']
                    else: 
                        sub_categories += swappable_sub_categories[i]['name'] + ', '
                swappable_address = SwappableAddress.objects.filter(swappable=swappable)[0]
                context = {
                    "swappable": swappable,
                    "sub_categories": sub_categories,
                    "swappable_images": swappable_images,
                    "swappable_address": swappable_address
                }
                return render(request, 'baba_barter/edit_swappable.html', context)
    return redirect(reverse('baba:intro'))

def update_swappable(request, id):
    if 'user_id' in request.session:
        if request.method == 'POST':
            if len(Swappable.objects.filter(id=id)) > 0:
                errors =  Swappable.objects.swappable_validations(request.POST)
                if len(errors):
                    for k, v in errors.items():
                        messages.error(request, v, extra_tags=k)
                    return redirect(reverse('baba:edit_swappable', kwargs={'id':id}))
                else:
                    swappable = Swappable.objects.filter(id=id)
                    if len(swappable) > 0: swappable = swappable[0]
                    swappable.name = request.POST['name']
                    swappable.type = request.POST['type']
                    category = Category.objects.filter(name=request.POST['category'])
                    if len(category) > 0: swappable.category = category[0]
                    swappable.short_description = request.POST['short_description']
                    swappable.long_description = request.POST['long_description']
                    swappable.notes = request.POST['notes']
                    swappable.value = request.POST['value']
                    swappable.currency = request.POST['currency']
                    swappable.condition = request.POST['condition']
                    swappable.save()
                    #Make sure only one swappable image has main=True
                    no_main_image = False
                    if SwappableImage.objects.filter(swappable__id=id, main=True).count() < 1: no_main_image = True
                    #use i to identify the first new image
                    i = 0
                    #use number_of_swappable_images to keep image naming incremental
                    number_of_swappable_images = SwappableImage.objects.filter(swappable__id=id).count()
                    for img in request.FILES.getlist('images'):
                        number_of_swappable_images+=1
                        image_name = f"{request.POST['name']}-{number_of_swappable_images}"
                        main = False
                        #if there is no main image, make the first of the new images the main one
                        if no_main_image: main = True if i==0 else False
                        image = SwappableImage(name=image_name, image=img, swappable=swappable, main=main)
                        image.save()
                        i+=1
                    messages.success(request, f'Swappable editted successfully', extra_tags='swappable_edit_sucess')
                    return redirect(reverse('baba:show_swappable', kwargs={'id':id}))
    return redirect(reverse('baba:intro'))

def privacy_policy(request):
    return render(request, 'baba_barter/privacy_policy_f.html')

def home(request, id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0:
            user_image = UserImage.objects.filter(user__id=user[0].id)[0]
            if str(id) == str(user[0].id): 
                context = {
                    'user': user[0],
                    'user_image': user_image
                }
                return render(request, 'baba_barter/home.html', context)
    return redirect(reverse('baba:intro'))

@csrf_exempt
def delete_swappable_images(request):
    if request.method == 'POST':
        for k, v in request.POST.items():
            SwappableImage.objects.filter(id=v)[0].delete()
    return HttpResponse(True)

#filter swapables on swappable page and home page
def filter_swappables(request, id):
    if 'user_id' in request.session:
        if request.method == 'POST':
            swappables = Swappable.objects.filter(user__id=id)
            #Name filter
            if len(request.POST['name']) > 0:
                swappables = swappables.filter(name__icontains=request.POST['name'])
            #Category filter
            if request.POST['category_sort'] != '0':
                swappables = swappables.filter(category__name=request.POST['category_sort'])
            #Order filter
            swappables = swappables.order_by(request.POST['order_sort'])
            #Location filter
            if len(SwappableAddress.objects.filter(swappable__user__id=id)) > 0:
                swappables = (
                    swappables.filter(swappable_address__city__icontains=request.POST['location']) | 
                    swappables.filter(swappable_address__state__icontains=request.POST['location']) | 
                    swappables.filter(swappable_address__country__icontains=request.POST['location']) | 
                    swappables.filter(swappable_address__code__icontains=request.POST['location'])
                ).distinct()
            #value filter
            swappables = swappables.filter(value__lte=int(request.POST['value'])+1)
            context = {
                'swappables': swappables
            }
            if len(swappables) < 1:
                context['no_swappable_message'] = "No swappables match your search result"
            return render(request, 'baba_barter/filtered_swappables.html', context)
    return redirect(reverse('baba:intro'))

def delete_swappable(request, id):
    if 'user_id' in request.session:
        swappable = Swappable.objects.filter(id=id)
        if len(swappable) > 0:
            swappable[0].delete()
            return redirect(reverse('baba:swappables', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

@csrf_exempt
def report_user(request, id):
    if 'user_id' in request.session:
        if request.method =='POST':
            context = {
                'user': User.objects.filter(id=id)[0]
            }
            return render(request, 'baba_barter/report_user.html', context)
        return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

def process_report_user(request, id):
    if 'user_id' in request.session:
        flagger_user = User.objects.filter(id=request.session['user_id'])
        if len(flagger_user) > 0:
            flagged_user = User.objects.filter(id=id)
            if len(flagged_user) > 0:
                if request.method =='POST':
                    errors =  UserFlag.objects.user_flag_validations(request.POST)
                    if len(errors):
                        for k, v in errors.items():
                            messages.error(request, v, extra_tags=k)
                        return redirect(reverse('baba:show_user', kwargs={'id':id}))
                    else:
                        user_flag = UserFlag(flagged_user=flagged_user[0], flagger_user=flagger_user[0],
                            message=request.POST['report_user_message'])
                        user_flag.save()
                        i = 0
                        for img in request.FILES.getlist('report_images'):
                            image_name = f"{user_flag.flagger_user.first_name} {user_flag.flagger_user.last_name} reports {user_flag.flagged_user.first_name} {user_flag.flagged_user.last_name} - {i}"
                            image = UserFlagImage(name=image_name, image=img, user_flag=user_flag)
                            image.save()
                            i+=1
                        messages.success(request, f'We have received your report. We are now looking into this issue', extra_tags='report_user_sucess')
                return redirect(reverse('baba:show_user', kwargs={'id':id}))
            return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

@csrf_exempt
def edit_profile_picture(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.filter(id=request.session['user_id'])[0]
        }
        return render(request, 'baba_barter/update_profile_picture.html', context)
    return redirect(reverse('baba:intro'))

def process_edit_profile_picture(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0:
            if request.method == 'POST':
                user = user[0]
                #if len(request.FILES.getlist('edit_user_image')) > 0:
                user_image = UserImage.objects.filter(user=user)[0]
                user_image.image = request.FILES['edit_user_image']
                user_image.save()
                messages.success(request, f'Profile picture updated successfully', extra_tags='profile_picture_update_sucess')
            return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

def compare(request, id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0:
            user = user[0]
            swappable = Swappable.objects.filter(id=id)
            if len(swappable) > 0:
                swappable = swappable[0]
                other_swappables = Swappable.objects.exclude(id=id).exclude(user=user)
                user_image = UserImage.objects.filter(user__id=request.session['user_id'])
                max_value = 0
                value_swappables = other_swappables.order_by('-value')
                if len(value_swappables) > 0:
                    max_value = value_swappables[0].value
                context = {
                    'swappable': swappable,
                    'other_swappables': other_swappables,
                    'user': user,
                    'user_image': user_image[0],
                    'max_value': max_value
                }
                return render(request, 'baba_barter/compare.html', context)
            return redirect(reverse('baba:swappables', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

#filter swapables on swappable page and home page
def filter_other_swappables(request, id):
    if 'user_id' in request.session:
        if request.method == 'POST':
            user = User.objects.filter(id=request.session['user_id'])
            if len(user) > 0:
                user = user[0]
                other_swappables = Swappable.objects.exclude(id=id).exclude(user=user)
                #Name filter
                if len(request.POST['name']) > 0:
                    other_swappables = other_swappables.filter(name__icontains=request.POST['name'])
                #Category filter
                if request.POST['category_sort'] != '0':
                    other_swappables = other_swappables.filter(category__name=request.POST['category_sort'])
                #Order filter
                other_swappables = other_swappables.order_by(request.POST['order_sort'])
                #Location filter
                if len(SwappableAddress.objects.filter(swappable__id=id)) > 0:
                    other_swappables = (
                        other_swappables.filter(swappable_address__city__icontains=request.POST['location']) | 
                        other_swappables.filter(swappable_address__state__icontains=request.POST['location']) | 
                        other_swappables.filter(swappable_address__country__icontains=request.POST['location']) | 
                        other_swappables.filter(swappable_address__code__icontains=request.POST['location'])
                    ).distinct()
                #value filter
                other_swappables = other_swappables.filter(value__lte=int(request.POST['value'])+1)
                context = {
                    'other_swappables': other_swappables
                }
                if len(other_swappables) < 1:
                    context['no_swappable_message'] = "No swappables match your search result"
            return render(request, 'baba_barter/filtered_other_swappables.html', context)
    print("scdsd")
    return redirect(reverse('baba:intro'))

def category(request, id):
    if 'user_id' in request.session:
        swappables = Swappable.objects.filter(category__id=id)
        user_image = UserImage.objects.filter(user__id=request.session['user_id'])
        user = User.objects.filter(id=request.session['user_id'])
        category = swappables[0].category
        max_value = 0
        value_swappables = swappables.order_by('-value')
        if len(value_swappables) > 0:
            max_value = value_swappables[0].value
        else: max_value = 1000
        if len(user_image) > 0 and len(user) > 0:
            context = {
                'user': user[0],
                'user_image': user_image[0],
                'swappables': swappables,
                'max_value': max_value,
                'category': category
            }
            return render(request, 'baba_barter/specific_category_swappables.html', context)
    return redirect(reverse('baba:intro'))

#filter swapables on swappable page and home page
def filter_category(request, id):
    if 'user_id' in request.session:
        if request.method == 'POST':
            swappables = Swappable.objects.filter(category__id=id)
            #Name filter
            if len(request.POST['name']) > 0:
                swappables = swappables.filter(name__icontains=request.POST['name'])
            #Order filter
            swappables = swappables.order_by(request.POST['order_sort'])
            #Location filter
            if len(SwappableAddress.objects.filter(swappable__user__id=id)) > 0:
                swappables = (
                    swappables.filter(swappable_address__city__icontains=request.POST['location']) | 
                    swappables.filter(swappable_address__state__icontains=request.POST['location']) | 
                    swappables.filter(swappable_address__country__icontains=request.POST['location']) | 
                    swappables.filter(swappable_address__code__icontains=request.POST['location'])
                ).distinct()
            #value filter
            swappables = swappables.filter(value__lte=int(request.POST['value'])+1)
            context = {
                'swappables': swappables
            }
            if len(swappables) < 1:
                context['no_swappable_message'] = "No swappables match your search result"
            return render(request, 'baba_barter/filtered_swappables.html', context)
    return redirect(reverse('baba:intro'))

@csrf_exempt
def report_swappable(request, id):
    if 'user_id' in request.session:
        if request.method =='POST':
            context = {
                'swappable': Swappable.objects.filter(id=id)[0]
            }
            return render(request, 'baba_barter/report_swappable.html', context)
        return redirect(reverse('baba:show_swappable', kwargs={'id':id}))
    return redirect(reverse('baba:intro'))

def process_report_swappable(request, id):
    if 'user_id' in request.session:
        flagger_user = User.objects.filter(id=request.session['user_id'])
        if len(flagger_user) > 0:
            flagged_swappable = Swappable.objects.filter(id=id)
            if len(flagged_swappable) > 0:
                if request.method =='POST':
                    errors =  SwappableFlag.objects.swappable_flag_validations(request.POST)
                    if len(errors):
                        for k, v in errors.items():
                            messages.error(request, v, extra_tags=k)
                        return redirect(reverse('baba:show_swappable', kwargs={'id':id}))
                    else:
                        swappable_flag = SwappableFlag(flagged_swappable=flagged_swappable[0], flagger_user=flagger_user[0],
                            message=request.POST['report_swappable_message'])
                        swappable_flag.save()
                        i = 0
                        for img in request.FILES.getlist('report_swappable_images'):
                            image_name = f"{swappable_flag.flagger_user.first_name} {swappable_flag.flagger_user.last_name} reports {swappable_flag.flagged_swappable.user.first_name}'s {swappable_flag.flagged_swappable.name} - {i}"
                            image = SwappableFlagImage(name=image_name, image=img, swappable_flag=swappable_flag)
                            image.save()
                            i+=1
                        messages.success(request, f'We have received your report. We are now looking into this issue', extra_tags='report_swappable_sucess')
                return redirect(reverse('baba:show_swappable', kwargs={'id':id}))
            return redirect(reverse('baba:show_user', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

def chat_room(request):
    context = {
        'user': User.objects.filter(id=request.session['user_id'])[0]
    }
    return render(request, 'baba_barter/chat_room.html', context)

def room(request, room_name):
    return render(request, 'baba_barter/chat.html', {
        'room_name': room_name
    })

def index(request):
    return render(request, 'baba_barter/index.html')