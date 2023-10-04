from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blogs.models import Blog


class BlogCreateView(CreateView):
    """Представление для создания нового блога."""

    model = Blog  # Используемая модель
    fields = ('title', 'content', 'created_at',)  # Поля, отображаемые в форме
    success_url = reverse_lazy('blogs:list')  # URL, куда перенаправлять после успешного создания блога

    def form_valid(self, form):
        """Обработка данных формы в случае их корректности."""

        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """Представление для обновления существующего блога."""

    model = Blog  # Используемая модель
    fields = ('title', 'content', 'created_at',)  # Поля, отображаемые в форме

    def form_valid(self, form):
        """Обработка данных формы в случае их корректности."""

        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Получение URL для перенаправления после успешного обновления блога."""

        return reverse('blogs:view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    """Представление для отображения списка блогов."""

    model = Blog  # Используемая модель

    def get_queryset(self, *args, **kwargs):
        """Получение queryset блогов, отфильтрованных по признаку публикации."""

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """Представление для отображения детальной информации о блоге."""

    model = Blog  # Используемая модель

    def get_object(self, queryset=None):
        """Получение объекта блога и обновление счетчика просмотров."""

        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    """Представление для удаления существующего блога."""

    model = Blog  # Используемая модель
    success_url = reverse_lazy('blogs:list')  # URL, куда перенаправлять после успешного удаления блога

