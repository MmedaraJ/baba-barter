from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import User, Swappable, SubCategory, Category, UserImage, SwappableImage
import bcrypt
from PIL import Image

def image(request):
    return render(request, 'baba_barter/image_test.html')
  
def process_image(request):
    img = Image.open("apps/baba_barter/static/baba_barter/yofte-assets/images/cupz.png")
    #img = Image.open(request.POST['image'])
    print(img)
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
    print("Successful")
    context = {
        'image': img
    }
    return redirect(reverse('baba:image'))

def intro(request):
    if 'user_id' in request.session:
        return redirect(reverse('baba:home', kwargs={'id':request.session['user_id']}))
    return render(request, 'baba_barter/intro.html')

#TODO implement has paid'
#is_authenticated, is deleted ...
def process_signup(request):
    if request.method == 'POST':
        errors =  User.objects.signup_validations(request.POST)
        if len(errors):
            for k, v in errors.items():
                messages.error(request, v, extra_tags=k)
            return redirect(reverse('baba:signup'))
        else:
            user_password_hash = bcrypt.hashpw(request.POST['signup_password_input'].encode(), bcrypt.gensalt())
            user = User(first_name=request.POST['signup_first_name_input'], last_name=request.POST['signup_last_name_input'], 
                email=request.POST['signup_email_input'], password_hash=user_password_hash, token_count=0, has_paid=True,
                date_of_birth=request.POST['signup_date_of_birth_input'], description=request.POST['signup_description_input'],
                is_authenticated=True
            )
            user.save()
            image_name = f"{request.POST['signup_first_name_input']} {request.POST['signup_last_name_input']}`s Profile Picture"
            image = UserImage(name=image_name, image=request.FILES['signup_image_input'], user=user)
            image.save()
            messages.success(request, f'Successful Sign Up', extra_tags='signup_success')
            request.session['user_id'] = str(user.id)
            return redirect(reverse('baba:home', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:signup'))

def signup(request):
    return render(request, 'baba_barter/signup.html')

def process_signin(request):
    if request.method == 'POST':
        errors =  User.objects.signin_validations(request.POST)
        if len(errors):
            for k, v in errors.items():
                messages.error(request, v, extra_tags=k)
            return redirect(reverse('baba:signin'))
        else:
            user = User.objects.filter(email=request.POST['signin_email_input'])[0]
            request.session['user_id'] = str(user.id)
            print(request.session['user_id'])
            messages.success(request, f'Successful Sign In', extra_tags='signin_success')
            return redirect(reverse('baba:home', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:signin'))

def signin(request):
    return render(request, 'baba_barter/signin.html')

#TODO allow users to view other profiles
#if id=session[id], show edit profle link, else, hide it
def show_user(request, id):
    if 'user_id' in request.session:
        if request.session['user_id'] == id:
            context = {
                'user': User.objects.filter(id=id)[0]
            }
            return render(request, 'baba_barter/user_profile.html', context)
    return redirect(reverse('baba:intro'))

@csrf_protect
def edit_profile(request, id):
    if 'user_id' in request.session:
        if str(request.session['user_id']) == str(id):
            context = {
                'user': User.objects.filter(id=request.session['user_id'])[0]
            }
            return render(request, 'baba_barter/edit_profile.html', context)
        return redirect(reverse('baba:edit_profile', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

#TODO add swappables and (sub)categories 
#TODO change main to true
def swappables(request, id):
    if 'user_id' in request.session:
        if str(id) == str(request.session['user_id']):
            swappables = Swappable.objects.filter(user__id=id)
            swappable_images = SwappableImage.objects.filter(swappable__user__id=id, main=True)
            both = zip(swappables, swappable_images)
            context = {
                'user': User.objects.filter(id=id)[0],
                'user_image': UserImage.objects.filter(user__id=id)[0],
                'both': both
            }
            return render(request, 'baba_barter/swappables.html', context)
        return redirect(reverse('baba:swappables', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

#TODO add security measure like edit_profile
def create_swappable(request, id):
    if 'user_id' in request.session:
        if str(id) == str(request.session['user_id']):
            context = {
                'user': User.objects.filter(id=id)[0]
            }
            return render(request, 'baba_barter/create_swappable.html', context)
        return redirect(reverse('baba:home', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

#TODO implement from is_deleted -- is_banned
def register_swappable(request, id):
    if 'user_id' in request.session:
        if id == request.session['user_id']:
            if request.method == 'POST':
                errors =  Swappable.objects.swappable_validations(request.POST)
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
                    print(request.FILES.getlist('images'))
                    for img in request.FILES.getlist('images'):
                        image_name = f"{request.POST['name']} - {i}"
                        main = True if i==0 else False
                        image = SwappableImage(name=image_name, image=img, swappable=swappable, main=main)
                        image.save()
                        i+=1
                    messages.success(request, f'Swappable created successfully', extra_tags='swappable_creation_sucess')
                    return redirect(reverse('baba:swappables', kwargs={'id':request.session['user_id']}))
        return redirect(reverse('baba:create_swappable', kwargs={'id':request.session['user_id']}))
    return redirect(reverse('baba:intro'))

def show_swappable(request, id):
    if 'user_id' in request.session:
        edit = False
        user = User.objects.filter(id=request.session['user_id'])[0]
        swappable = Swappable.objects.filter(id=id)[0]
        if swappable.user == user:
            edit = True
        context = {
            "swappable": swappable,
            "user": user,
            "edit": edit
        }
        return render(request, 'baba_barter/show_swappable.html', context)
    return redirect(reverse('baba:intro'))

def edit_swappable(request, id):
    if 'user_id' in request.session:
        if len(Swappable.objects.filter(id=id)) > 0:
            swappable = Swappable.objects.filter(id=id)[0]
            user = swappable.user
            if user.id == request.session['user_id']:
                print(swappable.sub_categories)
                swappable_sub_categories = swappable.sub_categories.all().values()
                sub_categories = ""
                for i in range(0, len(swappable_sub_categories)):
                    if i == len(swappable_sub_categories) - 1:
                        sub_categories += swappable_sub_categories[i]['name']
                    else: 
                        sub_categories += swappable_sub_categories[i]['name'] + ', '
                context = {
                    "swappable": swappable,
                    "sub_categories": sub_categories
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
                    swappable = Swappable.objects.filter(id=id)[0]
                    swappable.name = request.POST['name']
                    swappable.type = request.POST['type']
                    category = Category.objects.filter(name=request.POST['category'])[0]
                    swappable.category = category
                    swappable.short_description = request.POST['short_description']
                    swappable.long_description = request.POST['long_description']
                    swappable.notes = request.POST['notes']
                    swappable.value = request.POST['value']
                    swappable.currency = request.POST['currency']
                    swappable.condition = request.POST['condition']
                    swappable.save()
                    messages.success(request, f'Swappable editted successfully', extra_tags='swappable_edit_sucess')
                    return redirect(reverse('baba:show_swappable', kwargs={'id':id}))
    return redirect(reverse('baba:intro'))

def privacy_policy(request):
    return render(request, 'baba_barter/privacy_policy_f.html')

def home(request, id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])[0]
        if str(id) == str(user.id): 
            context = {
                'user': User.objects.filter(id=id)[0]
            }
            return render(request, 'baba_barter/home.html', context)
    return redirect(reverse('baba:intro'))