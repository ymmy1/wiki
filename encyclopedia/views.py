from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from . import util

class NewSearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'search', 'placeholder':"Search Encyclopedia" }))
class NewCreateForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'create_title', 'placeholder':"Title" }))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'create', 'placeholder':"Content" }))
     


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def create(request):
    print("request method is " + request.method)
    if request.method == "POST":
        print("form is POST")
        form = NewCreateForm(request.POST)
        if form.is_valid():
            print("form is Valid")
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            print("ENTRY SAVED")
            return HttpResponseRedirect(f'/wiki/{title}')
    return render(request, "encyclopedia/create.html", {
            "form": NewSearchForm(),
            "form_create": NewCreateForm()
        })


def wiki(request, name):
     return render(request, "encyclopedia/item.html", {
        "entry": util.get_entry(name),
        "form": NewSearchForm()
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



