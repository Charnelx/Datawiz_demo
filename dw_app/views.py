from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from .helpers.dwlib import api_conn, date_convertor, get_salary_data, get_dynamic_data
from datetime import datetime
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def index(request):
    context = dict()

    if request.user.is_authenticated():
        email = request.user.email
        psw = request.user.api_pass

        # return datawiz credentials/connection object
        conn = api_conn(email, psw)

        info_data = conn.get_client_info()
        context['info'] = info_data

    return render(request, "home.html", context)

@login_required(login_url='/login/')
def products_diff(request):
    email = request.user.email
    psw = request.user.api_pass

    conn = api_conn(email, psw)

    info_data = conn.get_client_info()

    # get observation interval
    initial_start = info_data['date_from'].strftime("%m.%d.%Y")
    initial_end = info_data['date_to'].strftime("%m.%d.%Y")

    if request.method == "POST":
        # get date range from ajax request
        date_range_raw = request.POST.get('info', None)

        # initial var for response to ajax script
        result_html = ''
        if date_range_raw:
            # convert dates for use with Datawiz API
            start_date, end_date, period = date_convertor(date_range_raw)

            # creates i_hope_unique key to store response data in cache
            h_key = 'dyn_' + str(hash(start_date + end_date))

            # uncomment to use cache
            in_cache = cache.get(h_key, None)
            # in_cache = False

            if in_cache:
                return HttpResponse(in_cache, content_type='text/html')
            else:

                # request to API to get products sales data
                df = conn.get_products_sale(
                    date_from=start_date,
                    date_to=end_date,
                    interval=period,
                    view_type='raw',
                    by=['turnover', 'qty', 'receipts_qty', 'profit'])

                if not df.empty:

                    # get transformed data
                    html_inc, html_dec = get_dynamic_data(df)

                    result_html = '<h2>Positive dynamic</h2>' + html_inc + '<br><br>' + '<h2>Negative dynamic</h2>' + html_dec

                    # uncomment to use cache
                    cache.set(h_key, result_html, timeout=60*5)

            return HttpResponse(result_html, content_type='text/html')
    else:
        daterange_form = DateRangeForm(required=True, initial_start_date=initial_start,
                                       initial_end_date=initial_end)

        context = {'daterange_form': daterange_form}

        return render(request, 'difference.html', context)

@login_required(login_url='/login/')
def general_indicators(request):
        email = request.user.email
        psw = request.user.api_pass

        conn = api_conn(email, psw)

        info_data = conn.get_client_info()

        # get observation interval
        initial_start = info_data['date_from'].strftime("%m.%d.%Y")
        initial_end = info_data['date_to'].strftime("%m.%d.%Y")

        if request.method == "POST":
            # get date range from ajax request
            date_range_raw = request.POST.get('info', None)
            if date_range_raw:
                # convert dates for use with Datawiz API
                start_date, end_date, period = date_convertor(date_range_raw)

                # creates i_hope_unique key to store response data in cache
                h_key = 'gen_' + str(hash(start_date+end_date))

                in_cache = cache.get(h_key, None)
                # in_cache = False

                if in_cache:
                    return HttpResponse(in_cache, content_type='text/html')
                else:

                    # request to API to get products sales data
                    df = conn.get_products_sale(
                                  date_from = start_date,
                                  date_to = end_date,
                                  interval = period,
                                  view_type = 'raw',
                                  by = ['turnover', 'qty', 'receipts_qty', 'profit'])


                    if not df.empty:
                        html_df = get_salary_data(df)

                        cache.set(h_key, html_df, timeout=60*5)

                        return HttpResponse(html_df, content_type='text/html')
                return HttpResponse('', content_type='text/html')
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

    return render(request, 'register.html', {'form': form})