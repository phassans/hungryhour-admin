from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import json
from django.http import JsonResponse
from urllib.request import urlopen
from django.utils.dateformat import DateFormat
import datetime


class IndexPageView(TemplateView):
    template_name = 'main/index.html'


class BusinessPageView(TemplateView):
    template_name = 'main/business.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BusinessPageView, self).get_context_data(
            *args, **kwargs)
        context['message'] = 'Hello World!'
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all')
        data = response.json()
        # print(data)
        context['data'] = data
        return context


class ListingPageView(TemplateView):
    template_name = 'main/listing.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ListingPageView, self).get_context_data(
            *args, **kwargs)
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all')
        print(response)
        business_list = response.json()
        context['business_list'] = business_list
        return context


class AddBusinessPageView(TemplateView):
    template_name = 'main/addbusiness.html'


class AddListingPageView(TemplateView):
    template_name = 'main/addlisting.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AddListingPageView, self).get_context_data(
            *args, **kwargs)
        context['message'] = 'Hello World!'
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all')
        data = response.json()
        # print(data)
        context['data'] = data
        return context


def InsertBusiness(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    website = request.POST.get('website')
    city = request.POST.get('city')
    state = request.POST.get('state')
    street = request.POST.get('street')
    postalCode = request.POST.get('postalCode')
    cuisine = request.POST.getlist('cuisine')
    day = request.POST.getlist('day[]')
    # print(day)
    open_time_session_one = request.POST.getlist('open_time_session_one[]')
    open_time_session_two = request.POST.getlist('open_time_session_two[]')
    close_time_session_one = request.POST.getlist('close_time_session_one[]')
    close_time_session_two = request.POST.getlist('close_time_session_two[]')
    hours = []
    for x in range(7):
        # print(day[x])
        if open_time_session_one[x] != '':
            hours.append({'day': day[x],
                          'open_time_session_one': open_time_session_one[x],
                          'close_time_session_one': close_time_session_one[x],
                          'open_time_session_two': open_time_session_two[x],
                          'close_time_session_two': close_time_session_two[x]})
    userid = 1
    # hours = json.dumps(hours)
    print(hours)
    # for item in request.POST.items():
    #     print(item)
    payload = {'userId': userid,
               'name': name,
               'phone': phone,
               'website': website,
               'city': city,
               'state': state,
               'street': street,
               'postalCode': postalCode,
               'cuisine': cuisine,
               'hours': hours,
               }
    response = requests.post(
        'https://www.itshungryhour.com/api/v1//business/add', data=json.dumps(payload))
    print(response.text)
    return redirect('business')


def InsertListing(request):
    sdt = request.POST.get('startDate')
    sdt = datetime.datetime.strptime(sdt, "%Y-%m-%d").date()
    sdt = sdt.strftime('%m/%d/%Y')
    edt = request.POST.get('recurringEndDate')
    edt = datetime.datetime.strptime(edt, "%Y-%m-%d").date()
    edt = edt.strftime('%m/%d/%Y')
    print(sdt)
    print(request.POST.dict())

    # # headers = {
    #     'Content-type': 'multipart/form-data;boundary=f0d7eb0b58c94f8ea3e665e28cffffdc'}
    response = requests.post(
        'https://www.itshungryhour.com/api/v1/listing/add', files=dict(
            images=request.FILES['images']), data=dict(
                businessId=request.POST.get('businessId'),
            title=request.POST.get('title'),
            discountDescription=request.POST.get('discountDescription'),
            description=request.POST.get('description'),
            startDate=sdt,
            recurringEndDate=edt,
            startTime=request.POST.get('startTime'),
            endTime=request.POST.get('endTime'),
        ))
    print(response.text)
    return redirect('listing')


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


class EditBusinessPageView(TemplateView):
    template_name = 'main/editbusiness.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EditBusinessPageView, self).get_context_data(
            *args, **kwargs)
        context['message'] = 'Hello World!'
        bid = self.kwargs['id']
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business?businessId='+bid)
        data = response.json()
        # print(data)
        context['data'] = data
        return context


class DeleteBusinessPageView(TemplateView):
    template_name = 'main/business.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EditBusinessPageView, self).get_context_data(
            *args, **kwargs)
        context['message'] = 'Hello World!'
        bid = self.kwargs['id']
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business?businessId='+bid)
        data = response.json()
        # print(data)
        context['data'] = data
        return context


class BusinessListingView(View):

    def get(self, request):
        print(request.GET)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/all',
                                 data=json.dumps({"businessId": int(request.GET.get('business_id'))}))
        # import code;
        # code.interact(local=dict(globals(), **locals()))
        print(response.status_code==200)
        business_listing = response.json()
        context = {'business_listing': business_listing}
        return JsonResponse(context)


class BusinessListingEditView(View):

    def get(self, request, id):
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/listing/admin?listingId=' + str(id))
        listing_data = response.json()
        print(listing_data)
        context = {'listing_data': listing_data}
        return render(request, 'main/listing_edit.html', context)

    def post(self, request, id):
        print(id)
        print(request.FILES.getlist('images'))
        print(json.dumps(request.POST))
        import code;
        code.interact(local=dict(globals(), **locals()))
        recurring = request.POST.get('recurring')
        if recurring == 'true':
            recurring = True
        else:
            recurring = False
        data = {'businessId': int(request.POST.get('businessId')), 'listingId': int(request.POST.get('listingId')),
                'title': request.POST.get('title'), 'discountDescription': request.POST.get('discountDescription'),
                'description': request.POST.get('description'), 'startDate': request.POST.get('startDate'),
                'recurringEndDate': request.POST.get('recurringEndDate'), 'startTime': request.POST.get('startTime'),
                'endTime': request.POST.get('endTime'), 'recurring': recurring}
        if request.POST.getlist('recurringDays'):
            data.update({'recurringDays': request.POST.getlist('recurringDays')})
        print(data)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/edit',
                                 files={'file': request.FILES['images'].file.read()}, data=data, headers={'Content-Type': 'multipart/form-data'})
        print(response.content)
        print(response.json())
        return


class BusinessListingDeleteView(View):

    def post(self, request, id):
        print(id)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/delete',
                                 data=json.dumps({"listingId": id}))
        print(response.json())
        return JsonResponse({})
