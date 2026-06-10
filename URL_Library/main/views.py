from django.shortcuts import render, redirect
from .forms import URLForm
from sign_up.models import UserContent, User
from .qr_code import generate_qr_code


def add_url(request):
    libraryform = URLForm()
    if request.method == 'POST':
        libraryform = URLForm(request.POST)
        if libraryform.is_valid():
            url_entry = libraryform.save(commit=False)
            user_id = request.session.get("user_id")  # using session to get the current user_id
            if user_id:
                url_entry.user = User.objects.get(id=int(user_id))

            url = url_entry.url
            name = url_entry.name
            url_entry.image_path = generate_qr_code(url, name)
            url_entry.save()
            return redirect('myurls_library')
    else:
        libraryform = URLForm()

    library = UserContent.objects.all()
    return render(request, 'library.html', {
        'libraryform': libraryform,
        'library': library,
    })


#Emmanuel says we dont need this anymore i am not sure why we dont i will ask him tonight
def url_library(request):
    # BUG This doesn't check for a logged in user. It just shows all the links.
    library = UserContent.objects.all()
    libraryform = URLForm()
    return render(request, 'library.html', {
        'library': library,
        'libraryform': libraryform
    })


# send to personal view
def myurls_library(request):
    user_id = request.session.get('user_id')
    library = UserContent.objects.filter(user=user_id) if user_id else UserContent.objects.none()
    # BUG If the user isn't logged in, redirect to login page instead of showing empty library

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

    return render(request, 'library.html', {
        'library': library,
        'libraryform': libraryform,
        'edit_mode': edit_mode,
        'edit_id': edit_id,
    })


# Update view
def update_url(request, pk):
    saved_url = UserContent.objects.get(id=pk)
    user_id = request.session.get('user_id')

    if not user_id or saved_url.user.id != int(user_id):  # only the user that created the url can edit it
        return redirect('url_library')

    if request.method == 'POST':
        libraryform = URLForm(request.POST, instance=saved_url)  # prefill the form with existing data

        if libraryform.is_valid():
            url_entry = libraryform.save(commit=False)
            url = url_entry.url
            name = url_entry.name
            url_entry.image_path = generate_qr_code(url, name)
            url_entry.save()
            return redirect('myurls_library')
    else:
        libraryform = URLForm(instance=saved_url)

    if user_id:
        library = UserContent.objects.filter(user=int(user_id))  # show only user's URLs
    else:
        library = UserContent.objects.all()  # show all URLs if not logged in

    return render(request, 'library.html', {
        'libraryform': libraryform,
        'library': library,
        'edit_mode': True,
        'edit_id': pk,
    })


# delete view
def delete_url(request, pk):
    saved_url = UserContent.objects.get(id=pk)
    user_id = request.session.get('user_id')

    if not user_id or saved_url.user.id != int(user_id):  # only the user that created the url can delete it
        return redirect('url_library')
    saved_url.delete()
    return redirect('myurls_library')


# about page view
def about_view(request):
    return render(request, "how_it_works.html")
