from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from users.forms import AppUserLoginForm


class UserLoginView(LoginView):
    """Представление для входа пользователя (login.html)."""

    # Явно указываю кастомную форму для входа пользователя, без этого не подтягиваются определенные в
    # форме AppUserLoginForm стили (наверное, потому что по умолчанию LoginView использует стандартную
    # форму Django → AuthenticationForm)
    authentication_form = AppUserLoginForm
    template_name = "users/login.html"

    def get_success_url(self):
        """Метод get_success_url() в LoginView - это предпочтительный для Django способ указания редиректа после
        успешной аутентификации. Если просто указать в контроллере "success_url = reverse_lazy(
        '<какое-то приложение>:main_page', то это не будет работать."""
        return reverse_lazy("preferences:user_preferences_page")

    def form_valid(self, form):
        """Автоматический вход пользователя после успешной аутентификации."""
        login(self.request, form.get_user())
        return super().form_valid(form)
