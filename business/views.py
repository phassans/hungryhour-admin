from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
import requests
import json
from django.http import JsonResponse, HttpResponseRedirect
import datetime
from django.contrib import messages
from .mixins import UserRequiredMixin


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
            request.session['userId'] = response.json().get('userId')
            request.session['fullName'] = response.json().get('fullName')
            return redirect('business')
        try:
            messages.error(request, response.json().get('message').split('"')[-2])
        except:
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
            request.session['userId'] = response.json().get('userId')
            request.session['fullName'] = response.json().get('fullName')
            return redirect('business')
        try:
            messages.error(request, response.json().get('message').split('"')[-2])
        except:
            messages.error(request, response.text)
        return HttpResponseRedirect(request.path_info)


class LogoutView(View):

    def get(self, request):
        request.session['userId'] = None
        return redirect('login')


class BusinessView(UserRequiredMixin, View):
    template_name = 'business/business.html'

    def get(self, request):
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all', params={'userId': request.session.get('userId')})
        business_list = response.json()
        context = {'data': business_list}
        return render(request, self.template_name, context)


class BusinessListingPageView(UserRequiredMixin, View):

    def get(self, request, id):
        print(id)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/all',
                                 data=json.dumps({"businessId": id, "userId": request.session.get('userId')}))
        print(response.text)
        business_listing = response.json()
        context = {'business_listing': business_listing}
        print(context)
        return render(request, 'business/business_listing.html', context)


class BusinessAddView(UserRequiredMixin, View):
    template_name = 'business/business_add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        city = request.POST.get('city')
        state = request.POST.get('state')
        street = request.POST.get('street')
        postalCode = request.POST.get('postalCode')
        cuisine = request.POST.getlist('cuisine')
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
        payload = {'userId': request.session.get('userId'),
                   'name': name, 'phone': phone, 'website': website, 'city': city,
                   'state': state, 'street': street, 'postalCode': postalCode,
                   'cuisine': cuisine, 'hours': hours}
        response = requests.post(
            'https://www.itshungryhour.com/api/v1//business/add', data=json.dumps(payload))
        print(response.text)
        if response.status_code == 200:
            messages.success(request, 'Business added successfully.')
        else:
            try:
                messages.error(request, response.json().get('message').split('"')[-2])
            except:
                messages.error(request, response.text)
        return redirect('business')


class ListingPageView(UserRequiredMixin, View):
    template_name = 'business/listing.html'

    def get(self, request):
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all', params={'userId': request.session.get('userId')})
        print(response)
        business_list = response.json()
        context = {'business_list': business_list}
        return render(request, self.template_name, context)


class BusinessListingAddView(UserRequiredMixin, View):
    template_name = 'business/listing_add.html'

    def get(self, request, id):
        context = {'business_id': id, 'business_name': request.GET.get('name')}
        return render(request, self.template_name, context)



class ListingAddView(UserRequiredMixin, View):
    template_name = 'business/listing_add.html'

    def get(self, request):
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business/all', params={'userId': request.session.get('userId')})
        business_list = response.json()
        context = {'business_list': business_list}
        return render(request, self.template_name, context)

    def post(self, request):
        start_date = datetime.datetime.strptime(request.POST.get('startDate'), "%Y-%m-%d").date().strftime('%m/%d/%Y')
        end_date = datetime.datetime.strptime(request.POST.get('recurringEndDate'), "%Y-%m-%d").date().strftime(
            '%m/%d/%Y')
        print(request.POST)
        print(request.FILES.getlist('images'))
        response = requests.post(
            'https://www.itshungryhour.com/api/v1/listing/add',
            files=dict(images=request.FILES['images']),
            data=dict(businessId=request.POST.get('businessId'), title=request.POST.get('title'),
                      discountDescription=request.POST.get('discountDescription'),
                      description=request.POST.get('description'), startDate=start_date,
                      recurringEndDate=end_date, startTime=request.POST.get('startTime'),
                      endTime=request.POST.get('endTime'), userId=request.session.get('userId'),
                      recurringDays=request.POST.getlist('recurringDays')))
        print(response.text)
        if response.status_code == 200:
            messages.success(request, 'Listing added successfully.')
        else:
            try:
                messages.error(request, response.json().get('message').split('"')[-2])
            except:
                messages.error(request, response.text)
        return redirect('listing')


class BusinessEditView(UserRequiredMixin, View):

    def get(self, request, id):
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/business',
            params={'businessId': id, 'userId': request.session.get('userId')})
        business_list = response.json()
        context = {'data': business_list}
        return render(request, 'business/business_edit.html', context)

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
        data = {'userId': request.session.get('userId'), 'name': request.POST.get('name'),
                'phone': request.POST.get('phone'),
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
            try:
                messages.error(request, response.json().get('message').split('"')[-2])
            except:
                messages.error(request, response.text)
        return redirect('business')


class BusinessDeleteView(UserRequiredMixin, View):

    def post(self, request, id):
        print(id)
        response = requests.post('https://www.itshungryhour.com/api/v1//business/delete',
                                 data=json.dumps({"businessId": id, "userId": request.session.get('userId')}))
        if response.status_code == 200:
            data = {'deleted': True}
        else:
            data = {'deleted': False, 'message': response.text}
        return JsonResponse(data)


class BusinessListingAjaxView(UserRequiredMixin, View):

    def get(self, request):
        print(request.GET)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/all',
                                 data=json.dumps({"businessId": int(request.GET.get('business_id')),
                                                  "userId": request.session.get('userId')}))
        print(response.status_code==200)
        business_listing = response.json()
        context = {'business_listing': business_listing}
        return JsonResponse(context)


class BusinessListingEditView(UserRequiredMixin, View):

    def get(self, request, id):
        response = requests.get(
            'https://www.itshungryhour.com/api/v1/listing/admin',
            params={'listingId': id, 'userId': request.session.get('userId')})
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
                'endTime': request.POST.get('endTime'), 'userId': request.session.get('userId'),
                'recurringDays': request.POST.getlist('recurringDays')}
        print(data)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/edit',
                                 files=dict(images=request.FILES.get('images')), data=data)
        print(response.content)
        if response.status_code == 200:
            messages.success(request, 'Listing updated successfully.')
        else:
            try:
                messages.error(request, response.json().get('message').split('"')[-2])
            except:
                messages.error(request, response.text)
        return redirect('listing')


class BusinessListingDeleteView(UserRequiredMixin, View):

    def post(self, request, id):
        print(id)
        response = requests.post('https://www.itshungryhour.com/api/v1//listing/delete',
                                 data=json.dumps({"listingId": id, "userId": request.session.get('userId')}))
        if response.status_code == 200:
            data = {'deleted': True}
        else:
            data = {'deleted': False, 'message': response.text}
        return JsonResponse(data)
