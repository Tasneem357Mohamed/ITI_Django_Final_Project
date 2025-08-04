from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect , get_object_or_404
from .forms import CreateUserForm, LoginForm , CreateRecordForm , UpdateRecordForm
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField
from .models import Record
from django.db.models.functions import Concat





def index(request):
    return render(request, 'web/index.html')

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'web/register.html', {'form': form})




def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'web/login.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    search_query = request.GET.get('search', '')

    if search_query:
        full_name = Concat('first_name', Value(' '), 'last_name', output_field=CharField())
        records = Record.objects.annotate(full_name=full_name).filter(full_name__icontains=search_query)
        no_results = not records.exists()
    else:
        records = Record.objects.all()
        no_results = False

    return render(request, 'web/dashboard.html', {
        'records': records,
        'search_query': search_query,
        'no_results': no_results
    })








def my_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def create_record(request):
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CreateRecordForm()
    return render(request, 'web/create-record.html', {'form': form})





@login_required(login_url='login')
def view_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    all_records = list(Record.objects.order_by('id'))  # Or another order like '-created_at'

    try:
        record_number = all_records.index(record) + 1
    except ValueError:
        record_number = 'N/A'  # In case it's not found for any reason

    return render(request, 'web/view_record.html', {
        'record': record,
        'record_number': record_number,
    })




@login_required(login_url='login')
def update_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('view-record', record_id=record.id)
    else:
        form = UpdateRecordForm(instance=record)

    return render(request, 'web/update_record.html', {
        'form': form,
        'record': record,
    })



@login_required(login_url='login')
def delete_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard')
    return render(request, 'web/confirm_delete.html', {'record': record})


def custom_404(request, exception):
    return render(request, 'web/404.html', status=404)