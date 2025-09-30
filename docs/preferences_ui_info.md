# 🎨 Интерфейс "Мои предпочтения"

Страница позволяет пользователю явно указать свои предпочтения по категориям (`aisle`).  

---

## 📂 Структура

1. `preferences/forms.py`  
   - форма `UserPreferencesForm`
   - использует `ModelMultipleChoiceField` для отображения всех `Aisle` как списка чекбоксов.  


2. `preferences/views.py`  
   Представление `UserPreferencesView(LoginRequiredMixin, FormView)`:  
   - `GET`: отображает форму с уже выбранными ранее значениями  
   - `POST`: сохраняет выбор в `UserPreference` и `UserInteraction`  


3. `preferences/urls.py`  
   Маршрут для страницы:  
   ```python
   path("my/", UserPreferencesView.as_view(), name="user_preferences_page")


4. `preferences/templates/preferences/user_preferences.html`  
    Шаблон на Bootstrap:
   - список чекбоксов для товарных категорий (aisles) в прокручиваемом блоке (scroll)
   - кнопка "Сохранить мои предпочтения"

---

## 🚀 Поведение

- При первом заходе форма пустая (ничего не выбрано).
- При сохранении:
  - старые записи UserPreference и UserInteraction (с типом preference) удаляются
  - новые предпочтения сохраняются в обе модели
- При повторном заходе уже выбранные значения автоматически отмечены.
