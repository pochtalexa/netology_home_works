from collections import Counter

from django.shortcuts import render
from django.http import Http404

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')

    if from_landing == 'original':
        counter_click['original'] += 1
    elif from_landing == 'test':
        counter_click['test'] += 1
    else:
        counter_click['errors'] += 1

    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    ab_test_arg = request.GET.get('ab-test-arg')

    if not ab_test_arg:
        raise Http404('no arg "ab-test-arg"')

    if ab_test_arg == 'original':
        counter_show['original'] += 1
        return render(request, 'landing.html')
    elif ab_test_arg == 'test':
        counter_show['test'] += 1
        return render(request, 'landing_alternate.html')
    else:
        raise Http404('"ab-test-arg" value error')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    contexts = {
        'test_conversion': round(counter_click['test'] / counter_show['test'], 2),
        'original_conversion': round(counter_click['original'] / counter_show['original'], 2)
    }

    return render(request, 'stats.html', context=contexts)
