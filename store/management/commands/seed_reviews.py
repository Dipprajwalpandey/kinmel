import random
from django.core.management.base import BaseCommand
from store.models import Product, Review

SAMPLE_NAMES = ["Sarah J.", "Michael C.", "David R.", "Priya S.", "Anish K.", "Maria G.", "Tom W.", "Aisha B."]
SAMPLE_COMMENTS = [
    "Great product, exactly as described.",
    "Fast delivery and good quality.",
    "Works well, happy with the purchase.",
    "Good value for the price.",
    "Would recommend to others.",
]

class Command(BaseCommand):
    help = "One-time seed: generate sample reviews for products that have none yet"

    def handle(self, *args, **options):
        created = 0
        for product in Product.objects.all():
            if Review.objects.filter(product=product).exists():
                continue
            review_count = random.randint(8, 45)
            for _ in range(review_count):
                rating = random.choices([5, 4, 3, 2], weights=[55, 30, 10, 5])[0]
                Review.objects.create(
                    product=product,
                    reviewer_name=random.choice(SAMPLE_NAMES),
                    rating=rating,
                    comment=random.choice(SAMPLE_COMMENTS),
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} sample review(s) across {Product.objects.count()} products."))
