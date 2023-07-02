from account.models import *
from django.forms import ModelForm, Form, CharField, ImageField, EmailField
from main.classes import *
from account.utils import *

class NewUsernamesForm(ModelForm):
    form_name = "User and Display Name"
    submit_button = "Confirm changes"
    form_disclaimer = "By changing your username, you may break links to your profile, and you may not be able to get your old username back if someone else takes it."


    class Meta:
        model = User
        fields = ["username", "display_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "New username"
        self.fields["display_name"].widget.attrs["placeholder"] = "New display name"

    def is_valid(self):
        return super().is_valid() and is_valid_username(self.cleaned_data["username"])

class BioAndReadmeForm(ModelForm):
    form_name = "Bio and Readme"
    submit_button = "Confirm changes"
    form_disclaimer = "Your bio and readme are public, and can be seen by anyone."
    
    class Meta:
        model = User
        fields = ["bio", "readme"]
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make readme a textarea
        self.fields["readme"].widget.input_type = "textarea"

class AvatarChangeForm(Form):
    form_name = "Avatar"
    submit_button = "Confirm changes"
    form_disclaimer = "Your avatar is public, and can be seen by anyone."
    avatar = ImageField()

    # Only valid if less than 2MB
    def is_valid(self):
        if not super().is_valid():
            return False

        if self.cleaned_data["avatar"].size > 2097152:
            self.add_error("avatar", "The file size must be less than 2MB.")
            return False
        return True

class SendEmailChangeLinkForm(ModelForm):
    class Meta:
        model = User
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Your current email address"
        self.fields["email"].widget.attrs["placeholder"] = "Current email address"
        self.fields["email"].widget.attrs["readonly"] = True

    form_name = "Email"
    submit_button = "Send email change link"
    form_disclaimer = "You will be sent an email with a link to change your email address 📧"


class SendPasswordResetLinkForm(Form):
    form_name = "Password"
    submit_button = "Send password reset link"
    form_disclaimer = "You will be sent an email with a link to reset your password 🔐"

    email = EmailField()

class SendAccountDeletionLinkForm(Form):
    form_name = "Delete Account"
    submit_button = "Send account deletion link"
    form_disclaimer = "You will be sent an email with a link to delete your account 🗑️"

class ChangeEmailForm(ModelForm):
    form_name = "New Email"
    submit_button = "Confirm changes"
    class Meta:
        model = User
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "New email address"
        self.fields["email"].widget.attrs["placeholder"] = "New email address"

class ChangePasswordForm(ModelForm):
    form_name = "New Password"
    submit_button = "Confirm changes"
    form_disclaimer = "You will be logged out from all your sessions after changing your password."
    class Meta:
        model = User
        fields = ["password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].label = "New password"
        self.fields["password"].widget.attrs["placeholder"] = "New password"
        self.fields["password"].widget.attrs["type"] = "password"
        self.fields["password"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password"].widget.attrs["value"] = ""

class DeleteAccountForm(Form):
    form_name = "Confirm Account Deletion"
    submit_button = "Delete account"
    form_disclaimer = "ALL your data will be deleted, and you will not be able to get it back. This action is irreversible."

class ThemeChangeForm(ModelForm):
    form_name = "Theme"
    submit_button = "Apply Theme"
    class Meta:
        model = User
        fields = ["theme"]

class LogoutSessionsForm(Form):
    form_name = "Logout All Sessions"
    submit_button = "Confirm Action"
    form_disclaimer = "You will be logged out from all your devices."
