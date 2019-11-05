from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
import requests
import json
from django.http import JsonResponse, HttpResponseRedirect
import datetime
from django.contrib import messages


class IndexPageView(TemplateView):
    template_name = 'business/index.html'


class LoginView(View):
    template_name = 'business/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        print(request.POST)
        response = requests.post('https://www.itshungryhour.com/api/v1/user/verify',
                                 data=json.dumps(request.POST))
        if response.status_code == 200:
            messages.success(request, "Successfully logged in.")
            return redirect('business')
        messages.error(request, response.text)
        return HttpResponseRedirect(request.path_info)


class RegisterView(View):
    template_name = 'business/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        print(request.POST)
        response = requests.post('https://www.itshungryhour.com/api/v1/user/add',
                                 data=json.dumps(request.POST))
        if response.status_code == 200:
            messages.success(request, "Successfully registered.")
            return redirect('business')
        messages.error(request, response.text)
        return HttpResponseRedirect(request.path_info)


class BusinessPageView(TemplateView):
    template_name = 'business/business.html'

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
    template_name = 'business/listing.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ListingPageView, self).get_context_data(
            *args, **kwargs)
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all')
        print(response)
        business_list = response.json()
        context['business_list'] = business_list
        return context


class BusinessListingPageView(View):

    def get(self, request, id):
        print(id)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/all',
                                 data=json.dumps({"businessId": id}))
        print(response.text)
        business_listing = response.json()
        context = {'business_listing': business_listing}
        print(context)
        return render(request, 'business/business_listing.html', context)


class AddBusinessPageView(TemplateView):
    template_name = 'business/addbusiness.html'


class AddListingPageView(TemplateView):
    template_name = 'business/addlisting.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AddListingPageView, self).get_context_data(
            *args, **kwargs)
        context['message'] = 'Hello World!'
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all')
        data = response.json()
        # print(data)
        context['business_list'] = data
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
    if response.status_code == 200:
        messages.success(request, 'Business added successfully.')
    else:
        messages.error(request, response.text)
    return redirect('business')


def InsertListing(request):
    start_date = datetime.datetime.strptime(request.POST.get('startDate'), "%Y-%m-%d").date().strftime('%m/%d/%Y')
    end_date = datetime.datetime.strptime(request.POST.get('recurringEndDate'), "%Y-%m-%d").date().strftime('%m/%d/%Y')
    print(request.POST)
    print(request.FILES.getlist('images'))
    # # headers = {
    #     'Content-type': 'multipart/form-data;boundary=f0d7eb0b58c94f8ea3e665e28cffffdc'}
    response = requests.post(
        'https://www.itshungryhour.com/api/v1/listing/add',
        files=dict(images=request.FILES['images']),
        data=dict(businessId=request.POST.get('businessId'), title=request.POST.get('title'),
                  discountDescription=request.POST.get('discountDescription'),
                  description=request.POST.get('description'), startDate=start_date,
                  recurringEndDate=end_date, startTime=request.POST.get('startTime'),
                  endTime=request.POST.get('endTime'),
                  recurringDays=request.POST.getlist('recurringDays')))
    print(response.text)
    if response.status_code == 200:
        messages.success(request, 'Listing added successfully.')
    else:
        messages.error(request, response.text)
    return redirect('listing')


class ChangeLanguageView(TemplateView):
    template_name = 'business/change_language.html'


class BusinessEditView(View):

    def get(self, request, id):
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business?businessId=' + str(id))
        business_list = response.json()
        context = {'data': business_list}
        return render(request, 'business/editbusiness.html', context)

    def post(self, request, id):
        day = request.POST.getlist('day[]')
        open_time_session_one = request.POST.getlist('open_time_session_one[]')
        open_time_session_two = request.POST.getlist('open_time_session_two[]')
        close_time_session_one = request.POST.getlist('close_time_session_one[]')
        close_time_session_two = request.POST.getlist('close_time_session_two[]')
        hours = []
        for x in range(7):
            if open_time_session_one[x] != '':
                hours.append({'day': day[x],
                              'open_time_session_one': open_time_session_one[x],
                              'close_time_session_one': close_time_session_one[x],
                              'open_time_session_two': open_time_session_two[x],
                              'close_time_session_two': close_time_session_two[x]})
        print(hours)
        data = {'userId': 1, 'name': request.POST.get('name'), 'phone': request.POST.get('phone'),
                'website': request.POST.get('website'), 'city': request.POST.get('city'),
                'state': request.POST.get('state'), 'street': request.POST.get('street'),
                'postalCode': request.POST.get('postalCode'), 'businessId': id,
                'addressId': int(request.POST.get('addressId')),
                'cuisine': request.POST.getlist('cuisine'), 'hours': hours}
        print(data)
        response = requests.post(
            'https://www.itshungryhour.com/api/v1//business/edit', data=json.dumps(data))
        print(response.text)
        if response.status_code == 200:
            messages.success(request, 'Business updated successfully.')
        else:
            messages.error(request, response.text)
        return redirect('business')


class BusinessDeleteView(View):

    def post(self, request, id):
        print(id)
        response = requests.post('https://www.itshungryhour.com/api/v1//business/delete',
                                 data=json.dumps({"businessId": id}))
        if response.status_code == 200:
            data = {'deleted': True}
        else:
            data = {'deleted': False, 'message': response.text}
        return JsonResponse(data)


class BusinessListingAjaxView(View):

    def get(self, request):
        print(request.GET)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/all',
                                 data=json.dumps({"businessId": int(request.GET.get('business_id'))}))
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
        return render(request, 'business/listing_edit.html', context)

    def post(self, request, id):
        print(id)
        print(request.FILES.getlist('images'))
        print(json.dumps(request.POST))
        start_date = datetime.datetime.strptime(request.POST.get('startDate'), "%Y-%m-%d").date().strftime('%m/%d/%Y')
        end_date = datetime.datetime.strptime(request.POST.get('recurringEndDate'), "%Y-%m-%d").date().strftime('%m/%d/%Y')
        data = {'businessId': int(request.POST.get('businessId')), 'listingId': int(request.POST.get('listingId')),
                'title': request.POST.get('title'), 'discountDescription': request.POST.get('discountDescription'),
                'description': request.POST.get('description'), 'startDate': start_date,
                'recurringEndDate': end_date, 'startTime': request.POST.get('startTime'),
                'endTime': request.POST.get('endTime'),
                'recurringDays': request.POST.getlist('recurringDays')}
        print(data)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/edit',
                                 files=dict(images=request.FILES.get('images')), data=data)
        print(response.content)
        if response.status_code == 200:
            messages.success(request, 'Listing updated successfully.')
        else:
            messages.error(request, response.text)
        return redirect('listing')


class BusinessListingDeleteView(View):

    def post(self, request, id):
        print(id)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/delete',
                                 data=json.dumps({"listingId": id}))
        if response.status_code == 200:
            data = {'deleted': True}
        else:
            data = {'deleted': False, 'message': response.text}
        return JsonResponse(data)