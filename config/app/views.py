from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.db.models import Q
from .models import UserFile
from .forms import RegisterForm, FileUploadForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('file_list')
    else:
        form = RegisterForm()
    return render(request, 'storage/register.html', {'form': form})

@login_required
def file_list(request):
    files = UserFile.objects.filter(owner=request.user)
    query = request.GET.get('q')
    if query:
        files = files.filter(Q(title__icontains=query) | Q(file__icontains=query))
    file_type = request.GET.get('type')
    if file_type in ('image', 'video', 'document', 'other'):
        files = files.filter(file_type=file_type)
    return render(request, 'storage/file_list.html', {
        'files': files, 'query': query, 'current_type': file_type,
    })

@login_required
def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'storage/upload.html', {'form': form})

@login_required
def file_detail(request, pk):
    file = get_object_or_404(UserFile, pk=pk)
    if file.owner != request.user and not file.is_public:
        raise Http404("Файл не найден")
    return render(request, 'storage/file_detail.html', {'file': file})

@login_required
def file_download(request, pk):
    file = get_object_or_404(UserFile, pk=pk)
    if file.owner != request.user and not file.is_public:
        raise Http404("Файл не найден")
    return FileResponse(
        file.file.open('rb'),
        as_attachment=True,
        filename=file.file.name.split('/')[-1],
    )

@login_required
def file_delete(request, pk):
    file = get_object_or_404(UserFile, pk=pk, owner=request.user)
    if request.method == 'POST':
        file.file.delete(save=False)
        file.delete()
        return redirect('file_list')
    return render(request, 'storage/file_confirm_delete.html', {'file': file})