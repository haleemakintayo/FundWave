from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator
from .forms import DonationForm
from decimal import Decimal
from userauths.models import UserProfile

# from django.db import models




class Case(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cases/images/')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed'), ('paused', 'Paused')], default='active')
    
    campaign_creator = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'account_type': 'creator'},
        related_name='cases',
        null=True
    )

    tags = models.ManyToManyField('Tag', blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    funding_type = models.CharField(max_length=20, choices=[('all_or_nothing', 'All or Nothing'), ('keep_what_you_raise', 'Keep What You Raise')], default='all_or_nothing')
    description = models.TextField(max_length=1000, blank=True)

    
    def get_absolute_url(self):
        return reverse('case_detail', args=[str(self.id)])


    


    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        return (self.raised_amount / self.goal_amount) * 100
    
    @property
    def amount_remaining(self):
        return max(0, self.goal_amount - self.raised_amount)
    
    @property
    def donors(self):
        return self.donations.values('first_name', 'last_name', 'email').distinct()

    




class Donation(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    donation_type = models.CharField(max_length=20, choices=DonationForm.DONATION_TYPES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )

    class Meta:
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
