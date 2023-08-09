from django.shortcuts import render

def index(request):

    return render(
        request,
        'single_pages/post_detail.html',
    )

def landing(request):
    return render(
        request,
        'single_pages/landing.html',
    )


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html',
    )