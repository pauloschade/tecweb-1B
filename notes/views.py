from django.shortcuts import render, redirect
from .models import Note, Tag


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = request.POST.get('tag')
        tags = Tag.objects.filter(name=tag)

        if len(tags) > 0:
            new_tag=tags[0]
        elif tag == "":
            new_tag = None
        else:
            new_tag=Tag(name=tag)
            new_tag.save()

        new_note = Note(title=title, content=content,tag=new_tag)
        new_note.save()
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        all_tags = Tag.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes, 'tags':all_tags})

def update(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        id = request.POST.get('id')
        Note.objects.filter(id=id).update(title=title, content=content)
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        all_tags = Tag.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes, 'tags':all_tags})

def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        tag = request.POST.get('tag')
        Note.objects.filter(id=id).delete()

        if tag is not None:
            tag_exist = Note.objects.filter(tag__name=tag)
            if len(tag_exist) == 0:
                Tag.objects.filter(name=tag).delete()

        return redirect('index')
    else:
        all_notes = Note.objects.all()
        all_tags = Tag.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes, 'tags':all_tags})

def get_tag(request):

    tag=request.POST.get('tag')

    notes=Note.objects.filter(tag__name=tag)

    return render(request, 'notes/tag.html', {'notes': notes, 'tag' : tag})