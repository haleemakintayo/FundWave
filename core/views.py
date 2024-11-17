from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Case , Donation
from .forms import DonationForm
from django.db import transaction
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Sum, Count, F
from django.contrib.auth.decorators import login_required


# Create your views here.


from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import urllib.parse
from django.conf import settings


def payment_page(request):
    if request.method == "POST":
        # Retrieve form data
        merchant_key = settings.PAYAZA_API_KEY
        connection_mode = request.POST.get("connection_mode")
        checkout_amount = request.POST.get("checkout_amount")
        currency_code = request.POST.get("currency_code", "NGN")
        email_address = request.POST.get("email_address")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        transaction_reference = request.POST.get("transaction_reference")
        redirect_url = "https://jexceltech.com"  # Your redirect URL

        # Optional custom details
        additional_details = {
            "pnr": request.POST.get("pnr"),
            "ticket_number": request.POST.get("ticket_number"),
        }
        encoded_additional_details = json.dumps(additional_details)

        # Build the Payment URL
        base_url = "https://business.payaza.africa/payment-page/"
        query_params = {
            "merchant_key": merchant_key,
            "connection_mode": connection_mode,
            "checkout_amount": checkout_amount,
            "currency_code": currency_code,
            "email_address": email_address,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "transaction_reference": transaction_reference,
            "additional_details": encoded_additional_details,
            "redirect_url": redirect_url,
        }
        payment_url = f"{base_url}?{urllib.parse.urlencode(query_params)}"

        # Redirect to the Payment Page
        return redirect(payment_url)

    return render(request, "payment_form.html")


def home(request):
    cases = Case.objects.all()
    return render(request, 'index.html', {'cases': cases})


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')



def donate(request):
    try:
        case = Case.objects.get(pk=1)  
    except Case.DoesNotExist:
        case = None
    return render(request, 'donate.html', {'case': case})


def faq(request):
    return render(request, 'faqs.html')

def cases(request):
    cases = Case.objects.all()
    return render(request, 'cases.html', {'cases': cases})

# def single_cases(request):

#     cases = Case.objects.all()
#     return render(request, 'single-cases.html', {'cases': cases})


def case_detail(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    amounts = [2500, 10000]
    
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                form = DonationForm(request.POST)
                if form.is_valid():
                    with transaction.atomic():
                        # Create the donation record
                        donation = Donation.objects.create(
                            case=case,
                            amount=form.cleaned_data['final_amount'],
                            donation_type=form.cleaned_data['donation_type'],
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            comment=form.cleaned_data['comment'],
                            anonymous=form.cleaned_data['anonymous_donation'],
                        )
                        
                        if form.cleaned_data['donation_type'] == 'regular':
                            case.raised_amount += form.cleaned_data['final_amount']
                            case.progress = (case.raised_amount / case.goal_amount) * 100
                            case.save()
                        
                        # Here you would integrate with your payment processor
                        # payment_result = process_payment(donation)
                        # if payment_result.requires_redirect:
                        #     return JsonResponse({
                        #         'redirect_url': payment_result.redirect_url
                        #     })
                        
                        return JsonResponse({
                            'success': True,
                            'message': 'Thank you for your donation!'
                        })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Please correct the errors below.',
                        'errors': form.errors
                    }, status=400)
                    
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'An error occurred while processing your donation.'
                }, status=500)
        else:
            
            pass
    
    context = {
        'case': case,
        'form': DonationForm(),
        'amounts': amounts,
        'min_amount': Decimal('100'),
    }
    
    return render(request, 'single-cases.html', context)


def team(request):
    return render(request, 'team.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def blog(request):
    return render(request, 'blog.html')

def blog_detail(request):
    return render(request, 'blog-details.html')

def gallery(request):
    return render(request, 'gallery.html')

def volunteer(request):
    return render(request, 'volunteer.html')

def error(request):
    return render(request, 'error.html')

def campaign(request):
    if request.method == 'POST':
        # Retrieve data from the form
        title = request.POST.get('title')
        category = request.POST.get('category')
        location = request.POST.get('location')
        goal_amount = request.POST.get('goal_amount')
        funding_type = request.POST.get('funding_type')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # Handle the uploaded image

        # Create and save the new case
        case = Case(
            title=title,
            category=category,
            location=location,
            goal_amount=goal_amount,
            funding_type=funding_type,
            description=description,
            campaign_creator=request.user.userprofile,  # Assuming the user is the campaign creator
            image=image  # Assign the uploaded image
        )
        case.save()

        # Redirect to a success page or dashboard
        return redirect('cases')  # Change this to the appropriate URL name


    return render(request, 'campaign.html')
 

def beneficiary_dashboard(request):
    user_cases = Case.objects.filter(campaign_creator=request.user.userprofile)

    total_raised = user_cases.aggregate(Sum('raised_amount'))['raised_amount__sum'] or 0
    total_goal = user_cases.aggregate(Sum('goal_amount'))['goal_amount__sum'] or 0
    active_cases = user_cases.filter(status="active").count()
    progress_percentage = (total_raised / total_goal) * 100 if total_goal > 0 else 0
    donors_count = (
        Donation.objects.filter(case__in=user_cases)
        .values('email')
        .distinct()
        .count()
    ) 
    
    # Pass data to the template
    context = {
        'raised_amount': total_raised,
        'goal_amount': total_goal,
        'progress_percentage': round(progress_percentage, 2),
        'active_donors_count': donors_count,
        'cases': user_cases,
    }

    return render(request, 'beneficiary-dashboard.html', context) 

