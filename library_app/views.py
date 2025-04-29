from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .decorators import role_required
from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserEditForm, BookForm
from .models import Book, CustomUser


def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')


#Аутентификация
def custom_login_view(request):
    form = CustomLoginForm()
    error = False
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('role_redirect')
            else:
                error = True
    return render(request, 'authentication.html', {
        'form': form,
        'error': error
    })

#Аккаунт библиотекаря
@role_required(['LIBRARIAN'])
def librarian_account(request):
    user_sort = request.GET.get('user_sort')
    book_sort = request.GET.get('book_sort')
    username = request.GET.get('username')

    if user_sort not in ['full_name', 'id', 'username',]:
        user_sort = 'full_name'

    if book_sort not in ['name', 'id', 'printing_year', 'author', 'language', 'end_date', 'is_taken', 'reader']:
        book_sort = 'name'

    users = CustomUser.objects.filter(role='READER').order_by(user_sort)
    books = Book.objects.all()

    if username:
        try:
            user = CustomUser.objects.get(username=username)
            books = books.filter(reader=user)
        except CustomUser.DoesNotExist:
            books = Book.objects.none()

    books = books.order_by(book_sort, 'end_date')

    return render(request, 'librarian_account.html', {
        'users': users,
        'books': books,
        'now': datetime.now().date(),
        'user_sort': user_sort,
        'book_sort': book_sort,
        'username': username,
        'current_user': request.user,
    })


@role_required(['READER'])
def reader_account(request):
    books = Book.objects.filter(reader=request.user.id)

    errors = request.session.pop('errors', None)
    message = request.session.pop('message', None)

    return render(request, 'reader_account.html', {
        'books': books,
        'now': datetime.now().date(),
        'current_user': request.user,
        'errors': errors,
        'message': message,
    })

@role_required(['READER'])
def add_reservation(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    errors = []

    active_reservations = Book.objects.filter(reader=request.user, is_taken=False).count()

    if active_reservations >= 5:
        errors.append("Вы не можете забронировать больше 5 книг одновременно")
    elif book.reader is not None:
        errors.append("Эта книга уже забронирована или выдана")
    else:
        book.reader = request.user
        book.end_date = datetime.now().date() + timedelta(days=7)
        book.save()
        request.session['message'] = "Книга успешно забронирована"

    if errors:
        request.session['errors'] = errors

    return redirect('reservation')

@role_required(['READER'])
def cancel_reservation(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    errors = []
    if book.reader != request.user:
        errors.append("Вы не можете отменить бронь на эту книгу")
    elif book.is_taken:
        errors.append("Нельзя отменить бронь: книга уже выдана")
    else:
        book.reader = None
        book.end_date = None
        book.save()
        request.session['message'] = "Бронь успешно отменена"

    if errors:
        request.session['errors'] = errors

    return redirect('reader_account')



@role_required(['READER'])
def reservation(request):
    errors = request.session.pop('errors', None)
    message = request.session.pop('message', None)

    book_sort = request.GET.get('book_sort')


    if book_sort not in ['name', 'author', 'printing_year', 'language']:
        book_sort = 'name'

    books = Book.objects.filter(end_date=None, is_taken=False).order_by(book_sort)
    return render(request, 'reservation.html', {
        'books': books,
        'book_sort': book_sort,
        'errors': errors,
        'message': message
    })




#Распределение по ролям
def role_redirect_view(request):
    user = request.user
    if user.role == 'ADMIN':
        return redirect(reverse('admin:index'))
    elif user.role == 'LIBRARIAN':
        return redirect('librarian_account')
    elif user.role == 'READER':
        return redirect('reader_account')
    return redirect('home')








# def register_reader(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'READER'
#             user.save()
#             messages.success(request, "Пользователь успешно зарегистрирован!")
#             login(request, user)  # Авторизуем пользователя сразу после регистрации
#             return redirect('home')
#         else:
#             messages.error(request, "Ошибка при регистрации")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration.html', {'form': form})
def register_reader(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'READER'
            user.save()
            messages.success(request, "Пользователь успешно зарегистрирован!")
            login(request, user)
            return redirect('register_reader')
        else:
            # Передаём ошибки вручную
            return render(request, 'registration.html', {
                'form': form,
                'errors': sum(form.errors.values(), []),  # Собираем все ошибки в один список
            })
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})




# --- LIBRARIAN FUNCTIONS ---
@role_required(['LIBRARIAN'])
def edit_reader(request, pk):

    errors = []
    user_obj = get_object_or_404(CustomUser, pk=pk)

    if user_obj.role != 'READER':
        return redirect('home')

    form = CustomUserEditForm(request.POST or None, instance=user_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Читатель изменён")
            return redirect('librarian_account')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    errors.append(error)

    return render(request, 'forms/reader_form.html', {'form': form,
                                                      'errors': errors,
                                                      'title': 'Редактировать читателя'})

@role_required(['LIBRARIAN'])
def delete_reader(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)

    # Проверка, чтобы librarian мог удалять только READER
    if user_obj.role != 'READER':
        return redirect('home')


    user_obj.delete()
    messages.success(request, "Читатель удалён")
    return redirect('librarian_account')










# --- BOOKS ---
@role_required(['ADMIN', 'LIBRARIAN'])
def create_book(request):
    errors = []
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Книга добавлена")
            return redirect('librarian_account' if request.user.role == 'LIBRARIAN' else 'admin')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    errors.append(error)
    else:
        form = BookForm()
    return render(request, 'forms/book_form.html', {'form': form, 'errors': errors, 'title': 'Добавить книгу'})

@role_required(['ADMIN', 'LIBRARIAN'])
def edit_book(request, pk):
    errors = []
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Книга изменена")
        return redirect('librarian_account' if request.user.role == 'LIBRARIAN' else 'admin')
    else:
        for field_errors in form.errors.values():
            for error in field_errors:
                errors.append(error)
    return render(request, 'forms/book_form.html', {'form': form, 'errors': errors, 'title': 'Редактировать книгу'})

@role_required(['ADMIN', 'LIBRARIAN'])
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    book.delete()
    return redirect('librarian_account' if request.user.role == 'LIBRARIAN' else 'admin')








# --- ADMIN FUNCTIONS (только API, так как есть админ панель Django) ---
@role_required(['ADMIN'])
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь создан")
            return redirect('admin_account')
    else:
        form = CustomUserCreationForm()
    return render(request, 'form.html', {'form': form, 'title': 'Создать пользователя'})

@role_required(['ADMIN'])
def edit_user(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)

    if request.user.role == 'READER':
        return redirect('home')

    # Librarian может только reader'ов
    if request.user.role == 'LIBRARIAN' and user_obj.role != 'READER':
        return redirect('home')

    # Librarian не может редактировать себя или других librarian/admin
    if request.user.role == 'LIBRARIAN' and user_obj.pk == request.user.pk:
        return redirect('home')

    form = CustomUserCreationForm(request.POST or None, instance=user_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_account' if request.user.role == 'ADMIN' else 'librarian_account')

    return render(request, 'form.html', {'form': form, 'title': 'Редактировать пользователя'})


@role_required(['ADMIN'])
def delete_user(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if request.user.role == 'LIBRARIAN' and user_obj.role != 'READER':
        return redirect('home')

    if request.user.role == 'READER':
        return redirect('home')

    user_obj.delete()
    return redirect('admin' if request.user.role == 'ADMIN' else 'librarian_account')











#Страницы ошибок
def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'errors/403csrf.html', status=403)


def server_error(request):
    return render(request, 'errors/500.html', status=500)