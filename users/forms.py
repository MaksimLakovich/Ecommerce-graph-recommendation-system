from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as translation


class AppUserLoginForm(AuthenticationForm):
    """Форма для входа ранее зарегистрированного пользователя в приложение."""

    def __init__(self, *args, **kwargs):
        """Настройка внешнего вида и поведения полей формы."""
        super().__init__(*args, **kwargs)

        # ШАГ 1: Django использует "username" как ключ, но у нас логин по email поэтому меняю username на email
        # ШАГ 2: Применяю стили - добавляю класс "form-control" для всех полей.
        # ШАГ 3: Устанавливаю placeholder вручную для наших полей формы регистрации.
        self.fields["username"].widget = forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        )
        # ШАГ 4: Убираю help_text из вывода на странице, так как help_text из model.py и дублирует то,
        # что и так уже автоматически создает class AppUser(AbstractUser).
        for field_name, field in self.fields.items():
            field.help_text = None

            # ШАГ 5: Переопределяю label вручную вместо значений на английском
            self.fields["password"].label = "Пароль"

    def clean(self):
        """Переопределяю дефолтное сообщение Django об ошибке.
        БЫЛО: Please enter a correct Почта (username): and password. Note that both fields may be case-sensitive.
        СТАЛО: Пожалуйста, проверьте правильность введённых данных и повторите попытку."""
        try:
            return super().clean()
        except forms.ValidationError:
            raise forms.ValidationError(
                translation("Пожалуйста, проверьте правильность введённых данных и повторите попытку."),
                code="invalid_login"
            )
