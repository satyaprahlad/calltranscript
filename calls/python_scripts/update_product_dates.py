from django.utils import timezone
from datetime import timedelta
from random import randint
from ..models import Product


def update_created_at_randomly():
    # Fetch all instances of your model
    all_objects = Product.objects.all()

    # Calculate date range (last one year)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)

    for obj in all_objects:
        # Generate a random date within the last year range
        random_date = start_date + timedelta(days=randint(0, 365))

        # Update the 'created_at' field with the random date
        obj.created_at = random_date
        obj.save()

# Call the function to update 'created_at' field randomly
update_created_at_randomly()
