from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
import secrets
from markdown2 import Markdown
from . import util

class NewSearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={ 'class':'search', 'placeholder':"Search Encyclopedia", "autocomplete":"off"}))

class NewCreateForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'create_title', 'placeholder':"Title" }))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'create_content', 'placeholder':"Content" }))

class NewEditForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'edit_content'}) )




def index(request):
    entries = util.list_entries()
    entries.sort()
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form": NewSearchForm()
    })

def random(request):
    title = secrets.choice(util.list_entries())
    return HttpResponseRedirect(f'/wiki/{title}')


def create(request):
    if request.method == "POST":
        form = NewCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            all_entries = util.list_entries()
            for entrie in all_entries:
                if entrie.lower() == title.lower():
                    return render(request, "encyclopedia/create.html", {
                        "form": NewSearchForm(),
                        "form_create": NewCreateForm(),
                        "error" : "This Title currently exists!"
                    })
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')
    return render(request, "encyclopedia/create.html", {
            "form": NewSearchForm(),
            "form_create": NewCreateForm()
        })

def edit(request, name):
    
    if request.method == "POST":
        print("START POST")
        form = NewEditForm(request.POST)
        if form.is_valid():
            print("START VALID")
            title = name
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            print("START SAVED")
            return HttpResponseRedirect(f'/wiki/{name}')
    
    else:
        page = util.get_entry(name)
        
        context = {
            'form_edit': NewEditForm(initial={'content': page}),
            'title': name
        }

        return render(request, "encyclopedia/edit.html", context)


def wiki(request, name):
    markdowner = Markdown()
    all_entries = util.list_entries()
    entry = None
    for entrie in all_entries:
        if entrie.lower() == name.lower():
            entry = markdowner.convert(util.get_entry(entrie))

    return render(request, "encyclopedia/item.html", {
        "entry": entry,
        "form": NewSearchForm(),
        "title": name
    })

def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["q"].lower()
            entries = util.list_entries()
            entries_list = []
            # converting entries to lower case for simple search
            for entry in entries:
                if search == entry.lower():
                    return HttpResponseRedirect(f'/wiki/{search}')
                # creating list for future not found result
                if search in entry.lower():
                    entries_list.append(entry)

            # If entry not found
            entries_list.sort()
            return render(request, "encyclopedia/search.html", {
                "key" : search,
                "entries": entries_list,
                "form": NewSearchForm()
            })
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
    })



