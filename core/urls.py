from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    path('faq/', views.faq, name='faq'),
    path('cases/', views.cases, name='cases'),
    # path('single_cases/<int:pk>/', views.single_cases, name='single_cases'),
    path('cases/<int:case_id>/', views.case_detail, name='case_detail'),
    # path('test-payment/', views.test_payment, name='test_payment'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('blog/', views.blog, name='blog'),
    path('blog_detail/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('error/', views.error, name='error'),
    path('beneficiary-dashboard/', views.beneficiary_dashboard, name='beneficiary-dashboard'),
    path('campaign/',views.campaign,name='campaign'),
    path('make-payment/', views.payment_page, name='payment'),

    
]


