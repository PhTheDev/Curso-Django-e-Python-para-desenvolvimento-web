from typing import Any
from .models import Servico, Funcionario, Recursos
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import ContatoForm

class IndexView(FormView):
    template_name = 'index.html'
    form_class = ContatoForm

    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        servicos = Servico.objects.order_by('?').all()
        funcionarios = Funcionario.objects.order_by('?').all()
        recursos = list(Recursos.objects.order_by('?').all()) # Lista para fazer o split

        # Dividindo os recursos em duas listas
        mid_index = len(recursos) // 2
        recursos_left = recursos[:mid_index]
        recursos_right = recursos[mid_index:]

        context['servicos'] = servicos
        context['funcionarios'] = funcionarios
        context['recursos_left'] = recursos_left
        context['recursos_right'] = recursos_right
        return context

    def form_valid(self, form, *args, **kwargs):
        form.send_email()
        messages.success(self.request, "E-mail enviado com sucesso")
        return super(IndexView, self).form_valid(form, *args, **kwargs)
    
    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        return super(IndexView,self).form_invalid(form, *args, **kwargs)
    