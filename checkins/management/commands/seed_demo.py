from django.core.management.base import BaseCommand

from accounts.models import User
from checkins.models import Cafe

# Clearly labeled DEMO data (fictional cafés) for development and grading.
# (name, area, price range). Areas in Mandaue City / Lapu-Lapu City are listed under their own city.
DEMO_CAFES = [
    ("Demo Matcha House", "Lahug", "2"), ("Demo Whisk & Leaf", "IT Park", "2"),
    ("Demo Green Ceremony", "Banilad", "3"), ("Demo Usucha Corner", "Mabolo", "1"),
    ("Demo Kyoto Kettle", "Ayala Center", "3"), ("Demo Sip & Stir Matcha", "Mandaue", "1"),
    ("Demo Hojicha & Co.", "Capitol Site", "2"), ("Demo Chasen Studio", "Guadalupe", "2"),
    ("Demo Tencha Table", "Talamban", "2"), ("Demo Emerald Cup", "Escario", "1"),
    ("Demo Jade Bowl", "Colon", "1"), ("Demo Uji Lane", "Lapu-Lapu City", "2"),
    ("Demo Matcha Mornings", "Basak", "1"), ("Demo Shizuoka Bar", "Kasambagan", "3"),
    ("Demo Verdant Brew", "Apas", "2"),
]
CITY_OVERRIDES = {"Mandaue": "Mandaue City", "Lapu-Lapu City": "Lapu-Lapu City"}
PASSWORD = "Matcha!demo-2026"


class Command(BaseCommand):
    help = "Seed 15 demo cafés and two test accounts (explorer_demo, owner_demo). Safe to re-run."

    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(
            username="owner_demo",
            defaults={"email": "owner_demo@example.com", "role": User.Role.OWNER},
        )
        explorer, _ = User.objects.get_or_create(
            username="explorer_demo", defaults={"email": "explorer_demo@example.com"},
        )
        for user in (owner, explorer):
            user.set_password(PASSWORD)
            user.save()
        for index, (name, area, price) in enumerate(DEMO_CAFES):
            Cafe.objects.update_or_create(name=name, defaults={
                "address": area, "city": CITY_OVERRIDES.get(area, "Cebu City"),
                "price_range": price, "description": "Demo listing for development.",
                "owner": owner if index < 2 else None,
            })
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(DEMO_CAFES)} cafés. Test accounts: explorer_demo / owner_demo (password: {PASSWORD})"
        ))
