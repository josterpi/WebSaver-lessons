from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .forms import URLForm
from .models import UserContent
from .qr_code import generate_qr_code


@login_required
def add_url(request: HttpRequest) -> HttpResponse:
    libraryform = URLForm()
    if request.method == 'POST':
        libraryform = URLForm(request.POST)
        if libraryform.is_valid():
            url_entry = libraryform.save(commit=False)
            url_entry.user = request.user
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
@login_required
def url_library(request: HttpRequest) -> HttpResponse:
    library = UserContent.objects.all()
    libraryform = URLForm()
    return render(request, 'library.html', {
        'library': library,
        'libraryform': libraryform
    })


# send to personal view
@login_required
def myurls_library(request: HttpRequest) -> HttpResponse:
    library = UserContent.objects.filter(user=request.user)

    edit_mode = False
    edit_id = request.GET.get('edit')
    libraryform = URLForm()

    if edit_id:
        try:
            saved_url = UserContent.objects.get(id=edit_id, user=request.user)
            libraryform = URLForm(instance=saved_url)
            edit_mode = True
        except UserContent.DoesNotExist:
            pass

    return render(request, 'library.html', {
        'library': library,
        'libraryform': libraryform,
        'edit_mode': edit_mode,
        'edit_id': edit_id,
    })


# Update view
@login_required
def update_url(request: HttpRequest, pk: int) -> HttpResponse:
    saved_url = get_object_or_404(UserContent, id=pk)

    if saved_url.user != request.user:  # only the user that created the url can edit it
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

    library = UserContent.objects.filter(user=request.user)

    return render(request, 'library.html', {
        'libraryform': libraryform,
        'library': library,
        'edit_mode': True,
        'edit_id': pk,
    })


# delete view
@login_required
def delete_url(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != 'POST':
        return redirect('myurls_library')
    saved_url = get_object_or_404(UserContent, id=pk)

    if saved_url.user != request.user:  # only the user that created the url can delete it
        return redirect('url_library')
    saved_url.delete()
    return redirect('myurls_library')


# about page view
def about_view(request: HttpRequest) -> HttpResponse:
    return render(request, "how_it_works.html")
