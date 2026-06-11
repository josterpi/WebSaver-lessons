import qrcode
from django.shortcuts import render,redirect
from .forms import URLForm
from Sign_up.models import UserContent, User
from .QRcode import generate_qr_code
from django.conf import settings
import os

def add_url(request):
    # access form data to generate qr code and save filepath to database
    libraryform = URLForm()
    if request.method == 'POST':
        libraryform = URLForm(request.POST)
        if libraryform.is_valid():
            object = libraryform.save(commit=False)
            user_id = request.session.get("user_id")    #using session to get the current user_id
            if user_id:
                object.user = User.objects.get(id=int(user_id))
                
            url = object.url 
            name = object.name
            object.image_path = generate_qr_code(url, name) #generates qrcode
            object.save()
            return redirect('/my_library')
    else:
        libraryform = URLForm()

    library = UserContent.objects.all() 
    return render(request, 'Library.html', {
        'libraryform':libraryform,
        'library': library,  
    })

#Emmanuel says we dont need this anymore i am not sure why we dont i will ask him tonight
def url_library(request):
    library = UserContent.objects.all()
    libraryform = URLForm()
    return render(request, 'Library.html', {
        'library': library,
        'libraryform': libraryform
    })

# send to personal view
def myurls_library(request):
    user_id = request.session.get('user_id')
    library = UserContent.objects.filter(user=user_id) if user_id else UserContent.objects.none()

    edit_mode = False
    edit_id = request.GET.get('edit')
    libraryform = URLForm()

    if edit_id:
        try:
            saved_url = UserContent.objects.get(id=edit_id, user=user_id)
            libraryform = URLForm(instance=saved_url)
            edit_mode = True
        except UserContent.DoesNotExist:
            pass  # fallback to blank form if object not found or user mismatch

    return render(request, 'Library.html', {
        'library': library,
        'libraryform': libraryform,
        'edit_mode': edit_mode,
        'edit_id': edit_id,
    })


# Update view
def update_url(request, pk):    #uses the primary key that gets made automajically when a new url is added to pull that specific record
    saved_url = UserContent.objects.get(id=pk)
    user_id = request.session.get('user_id')
    
    if not user_id or saved_url.user.id != int(user_id):         #only the user that created the url can edit it
        return redirect('/library')
     
    if request.method == 'POST':
        libraryform = URLForm(request.POST, instance=saved_url)    # this will prefill the form with the existing data from the database
        
        if libraryform.is_valid():
            object = libraryform.save(commit=False)
            url = object.url 
            name = object.name
            object.image_path = generate_qr_code(url, name)
            object.save()
            return redirect('/my_library')
    else:
        libraryform = URLForm(instance=saved_url)

    if user_id:
        library = UserContent.objects.filter(user=int(user_id))  # Show only users URLs
    else:
        library = UserContent.objects.all()  # Show all URLs if not logged in
    
    return render(request, 'Library.html', {
        'libraryform': libraryform,
        'library': library,
        'edit_mode': True,
        'edit_id': pk,
    })


# delete view
def delete_url(request, pk):    #uses the primary key to find the record to delete
    saved_url = UserContent.objects.get(id=pk)
    user_id = request.session.get('user_id')

    if not user_id or saved_url.user.id != int(user_id):         #only the user that created the url can delete it
        return redirect('/library')
    saved_url.delete()
    return redirect('/my_library')

# about page view
def about_view(request):
    return render(request, "how_it_works.html")