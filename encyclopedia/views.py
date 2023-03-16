from ast import And, Return
from cProfile import label
from logging import PlaceHolder
from tkinter import Widget
from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown import Markdown
from django import forms
import secrets
from . import util


class newEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title",widget=forms.TextInput(attrs={
        "class" : "form-control col-mg-8 col-lg-8",
        "placeholder" : "Your Entry Title",

    }))
    content = forms.CharField(label="Entry Content",widget=forms.Textarea(attrs={
        "class" : "form-control col-mg-8 col-lg-8",
        "placeholder" : "Type your entry content here",
        "rows": 10
    }))
    edit = forms.BooleanField(initial=False , widget=forms.HiddenInput(), required=False)
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request , entry):
    markdown = Markdown()
    givenEntry = util.get_entry(entry)
    if givenEntry is None:
        return render(request, 'encyclopedia/notFound.html',{
            "entryTitle" : entry
        })
    else :
        return render(request, 'encyclopedia/entry.html',
        {
             "entryTitle" : entry,
             "entry" : markdown.convert(givenEntry)
        })   
def search(request):
    i = 0
    value = request.GET.get('q','')
    if (util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entryName:entry",kwargs={"entry":value}))
    else:
        subEntry = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subEntry.append(entry)
                i = 1
        if i == 0:
             return render(request, "encyclopedia/notFound.html",{
                 "entryTitle" : value
            })    

        return render(request,"encyclopedia/index.html",
        {
            "entries" : subEntry,
            "value": value,
            "search":True
        })     
           
def newEntry(request):
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["edit"]is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entryName:entry",kwargs={"entry":title}))
            else :
                return render(request , "encyclopedia/newEntry.html",
                {
                    "form" : form,
                    "existing" : True,
                    "entry" : entry,
                    "entryTitle" : title
                }) 
        else :
             return render(request , "encyclopedia/newEntry.html",
                {
                    "form" : form,
                    "existing" : False,
                    
                })    
    else:
         return render(request , "encyclopedia/newEntry.html",
                {
                    "form" : newEntryForm(),
                    "existing" : False
                    
                })    

def edit(request,entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/notFound.html",
        {
            "entryTitle" : entry
        }) 
    else :
        form = newEntryForm()
        form.fields["title"].initial =entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request , "encyclopedia/newEntry.html" , {
            "entryTitle" : form.fields["title"].initial,
            "form": form,
            "edit":form.fields["edit"].initial

        })

def randomPage(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entryName:entry",kwargs={"entry":randomEntry}))
