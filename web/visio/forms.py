from django import forms


class CodeInputForm(forms.Form):
    code = forms.CharField(label="Введите код на языке C++:", widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    code_file = forms.FileField(label="Или прикрепите:", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    def is_valid(self):
        code: str = self.data["code"]
        files = self.files
        if len(code.replace(" ", "").replace("\n", "")):
            return True
        if "code_file" in files.keys() and files["code_file"].content_type == "text/plain" \
                and files["code_file"].size < 1048576 and files["code_file"].name.split(".")[1] in ["cpp", "c", "hpp", "h"]:
            return True
        return False
