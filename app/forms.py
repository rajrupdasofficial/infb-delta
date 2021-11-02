from django import forms
from .models import BlogPost,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



choices=Category.objects.all().values_list('name','name')
choice_list=[]
for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields=('author','intro','category','thumbnail','content')
        widgets={
            'author':forms.TextInput(attrs={'class':"from-control",'value':'','id':'max','type':'hidden'}),
            #'category':forms.Select(choices=choice_list,attrs={'class':"form-control"}),
            'category':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
            'intro':forms.TextInput(attrs={'class':'form-control'}),
        }
class SignUpForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget.attrs.update({
            'class':"input",
            'placeholder':''
        })
        self.fields["email"].widget.attrs.update({
            'class':"input",
            'placeholder':""
        })
    #email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    #first_name=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':"form-control"}))
    #last_name=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':"form-control"}))
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')
    #def __init__(self,*args,**kwargs):
        #super(SignUpForm,self).__init__(*args,**kwargs)
        #self.fields['username'].widget.attrs['class']='form-control'
        #self.fields['password1'].widget.attrs['class']='form-control'
        #self.fields['password2'].widget.attrs['class']='form-control' 
