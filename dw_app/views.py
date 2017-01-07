from django.core.exceptions import ValidationError
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import RequestContext
from .forms import *
from .helpers.dwlib import api_conn, date_convertor
from datetime import datetime


def index(request):
    if request.user.is_authenticated():
        email = request.user.email
        psw = request.user.api_pass

        conn = api_conn(email, psw)

        info_data = conn.get_client_info()

        return render(request, "home.html", {'info': info_data})

    return render(request, "home.html")

@login_required(login_url='/login/')
def general_indicators(request):
        email = request.user.email
        psw = request.user.api_pass

        conn = api_conn(email, psw)

        info_data = conn.get_client_info()

        initial_start = info_data['date_from'].strftime("%m.%d.%Y")
        initial_end = info_data['date_to'].strftime("%m.%d.%Y")

        if request.method == "POST":

            date_range_raw = request.POST.get('info', None)
            if date_range_raw:
                start_date, end_date, period = date_convertor(date_range_raw)

                df = conn.get_products_sale(
                              date_from = start_date,
                              date_to = end_date,
                              interval = period,
                              view_type = 'raw',
                              by = ['turnover', 'qty', 'receipts_qty', 'profit'])

                if not df.empty:
                    df.sort_values(['date'], inplace=True)
                    df.set_index(['date'], inplace=True)

                    result = df.groupby([df.index]).aggregate('sum')
                    result['turnover_diff'] = result['turnover'].diff()

                    format = lambda x: "{0:.2f}".format(x)
                    result = result.applymap(format)

                    json_dt = result.reset_index().to_json(orient='records')

                    return HttpResponse(json_dt, content_type='application/json')
                    # return JsonResponse(json_dt)

                return JsonResponse({'empty': True})

        else:
            daterange_form = DateRangeForm(required=True, initial_start_date=initial_start,
                                           initial_end_date=initial_end)

            context = {'daterange_form': daterange_form}

            return render(request, 'general.html', context)


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'],
                                            api_pass=form.cleaned_data['api_pass'])

            return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()
    # variables = RequestContext(request, {'form': form})

    return render(request, 'register.html', {'form': form})