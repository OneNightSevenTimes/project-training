#_*_coding:utf8_*_
#__Author__:YiChen Wang

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from myauth import UserProfile
from django.contrib.auth import forms as auth_form

import models


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email','token')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    """
    help_text=("Raw passwords are not stored, so there is no way to see "
               "this user's password, but you can change the password "
               "using <a href=\"password/\">this form</a>."))
    """
    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("明文密码没有被保存,这里显示的都是加密过后的密文密码.此处可以更改密码"
                   ",地址: <a href=\"password/\">修改密码</a>."))
    class Meta:
        model = UserProfile
        fields = ('email', 'password','is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','is_admin','is_active','name','department')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password','name')}),
        ('Personal info', {'fields': ('department','tel','mobile','memo')}),
        ('API TOKEN info', {'fields': ('token',)}),
        ('Permissions', {'fields': ('is_active','is_admin')}),
        #(u'可管理的主机组', {'fields': ('host_groups',)}),
        #(u'可管理的主机', {'fields': ('bind_hosts',)}),
        ('账户有效期', {'fields': ('valid_begin_time','valid_end_time')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2','name','is_active','is_admin')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()