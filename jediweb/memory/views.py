import numpy as np
from django.contrib.auth import authenticate, login
# Create your views here.
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from rest_framework.authtoken.models import Token

from .forms import UserForm
from .models import MemoryImages, MemoryTest


def register(request):
  if request.POST:
    form = UserForm(request.POST)

    # Validate the form: the captcha field will automatically
    # check the input
    if form.is_valid():
      human = True

      user = User()
      user.first_name = form.cleaned_data['name']
      user.last_name = form.cleaned_data['affiliation']
      user.email = form.cleaned_data['email']
      user.username = form.cleaned_data['email']
      user.save()

      token, created = Token.objects.get_or_create(user=user)


      # Save the details.

  else:
    form = UserForm()

  data = {}
  data['form'] = form
  return render(request, 'memory/index.html', data)


def home(request, token):
  # Login/ Authenticate user using a token.

  user = authenticate(token)
  if user is not None:
    login(request, user)
    print('User successfully logged in.')
    return redirect('memory_start')
  else:
    return render(request, 'common/error.html')


def start(request):
  print(request.user)
  data = {}
  data['show_memory_nav'] = True
  return render(request, 'memory/start.html', data)


def images(request, n_img=2):
  data = {}
  data['n_img'] = n_img;
  data['show_memory_nav'] = True
  return render(request, 'memory/images.html', data)


def images_test(request):
  data = {}
  data['show_memory_nav'] = True
  return render(request, 'memory/images_test.html', data)


def get_images(request, n_img=2):
  n_imgs = 80
  img_idx = []
  images = []
  for i in range(int(n_img)):
    rand_int = np.random.random_integers(0, n_imgs, 1)[0]
    while rand_int in img_idx:
      rand_int = np.random.random_integers(0, n_imgs, 1)[0]

    img_idx.append(int(rand_int))
    img = MemoryImages.objects.get(id=rand_int)
    images.append(img.file_name)

  # Save the images to session.
  request.session['ORDER_IMGS'] = img_idx
  request.session['ORDER_IMG_NAMES'] = images

  data = {}
  data['images'] = images

  return JsonResponse(data)


def get_images_test(request):
  imgs = request.session['ORDER_IMGS']
  np.random.shuffle(imgs)
  images = []
  for i in imgs:
    img = MemoryImages.objects.get(id=i)
    images.append(img.file_name)

  data = {}
  data['images'] = images

  return JsonResponse(data)


def check_order(request):
  imgs = request.session['ORDER_IMG_NAMES']
  provided_order = request.POST.getlist('items[]')

  data = {}
  n_imgs = len(imgs)

  if (imgs == provided_order):
    if n_imgs <= 10:
      n_imgs = len(imgs) + 1
      data['redirect_url'] = reverse('memory_images', kwargs={'n_img': '%d' % (n_imgs)})
  else:

    memoryTest = MemoryTest()
    memoryTest.user = request.user
    memoryTest.score = n_imgs
    memoryTest.save()

    request.session['USER_MEMORY'] = n_imgs
    data['redirect_url'] = reverse('memory_completed')

  return JsonResponse(data)


def completed(request):
  data = {}
  data['show_memory_nav'] = True

  memoryTest = MemoryTest.objects.filter(user=request.user).all()
  trials = len(memoryTest)

  data['trials'] = trials

  if trials < 3:
    next_url = '/memory/images/2'
  else:
    next_url = '/memory/score'

  data['next_url'] = next_url

  return render(request, 'memory/completed.html',data)


def score(request):


  memoryTest = MemoryTest.objects.filter(user=request.user).all()

  score = 0
  for mem in memoryTest:
    score += mem.score

  score = score/3.0

  data = {}
  data['score'] = "%0.2f"%score


  return render(request, 'memory/score.html',data)