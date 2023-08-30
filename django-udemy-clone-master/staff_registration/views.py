from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import StaffRegistrationForm

def register_as_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = StaffRegistrationForm()

    return render(request, 'staff_registration/register.html', {'form': form})

# Create your views here.
