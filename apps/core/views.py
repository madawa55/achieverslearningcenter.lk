from django.shortcuts import render


def home(request):
    """Homepage view"""
    context = {
        'title': 'Achievers Learning Center - Excellence in Education',
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    context = {
        'title': 'About Us - Achievers Learning Center',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Contact page view"""
    context = {
        'title': 'Contact Us - Achievers Learning Center',
    }
    return render(request, 'core/contact.html', context)
