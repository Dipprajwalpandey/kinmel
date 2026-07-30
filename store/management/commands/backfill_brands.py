from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = "One-time backfill: derive Product.brand from the first word of product_name"

    def handle(self, *args, **options):
        updated = 0
        skipped = []

        for product in Product.objects.filter(brand=""):
            first_word = product.product_name.strip().split(" ")[0]
            product.brand = first_word
            product.save(update_fields=["brand"])
            updated += 1
            self.stdout.write(f"  {product.product_name!r} -> brand={first_word!r}")

        self.stdout.write(self.style.SUCCESS(f"\nUpdated {updated} product(s)."))
        self.stdout.write("Please review the output above — some entries (e.g. multi-word brand names) may need manual correction in the admin.")