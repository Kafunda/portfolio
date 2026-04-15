from django import forms


class ContactForm(forms.Form):
    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Votre nom",
            "class": "w-full p-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-black outline-none"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Votre email",
            "class": "w-full p-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-black outline-none"
        })
    )

    sujet = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Sujet",
            "class": "w-full p-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-black outline-none"
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Votre message",
            "rows": 4,
            "class": "w-full p-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-black outline-none"
        })
    )

    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    def clean_message(self):
        message = self.cleaned_data.get("message")

        if len(message) < 10:
            raise forms.ValidationError("Le message est trop court.")

        return message

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("honeypot"):
            raise forms.ValidationError("Spam détecté.")
        return cleaned_data