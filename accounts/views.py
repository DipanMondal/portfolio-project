from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from portfolio.models import PortfolioImage
from portfolio.forms import UploadFileForm
from portfolio_project import mongo


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('account_manager')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def account_manager(request):
    images = PortfolioImage.objects.all()
    feedback_list = mongo.get_all_feedback()
    json_data = mongo.get_analysis()
    print(json_data)
    analysis = [json_data['positive'], json_data['negative'], json_data['neutral']]
    for feedback in feedback_list:
        feedback['id'] = str(feedback['_id'])  # Convert ObjectId to string for use in templates
        del feedback['_id']
    print(feedback_list)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = PortfolioImage(image=request.FILES["file"])
            instance.save()
            return redirect('account_manager')
    else:
        form = UploadFileForm()
    return render(request, "account_manager.html", {"form": form, "images": images, "feedback_list": feedback_list, "analysis": analysis})


@login_required
def delete_image(request, image_id):
    PortfolioImage.objects.filter(id=image_id).delete()
    return redirect('account_manager')


@login_required
def delete_feedback(request, id):
    mongo.delete_feedback(id)
    return redirect(account_manager)

