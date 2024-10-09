from django.shortcuts import render

def profile_view(request):
    # Add your view logic here
    return render(request, 'profiles/profile.html')

