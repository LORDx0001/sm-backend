from django.core.management.base import BaseCommand
from api.models import User
from education.models import LessonAnalysis, WorkPlan
from library.models import Book
from inventory.models import Item
from performance.models import KPIRecord
from django.utils import timezone
import random
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Seeds the database with fake university data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. Seed Users
        roles_data = [
            ('rektor_user', 'rektor', 'Rektor User'),
            ('prorektor_user', 'prorektor', 'Prorektor User'),
            ('tyuter_user', 'tyuter', 'Tyuter User'),
            ('edu_user', 'oquv_bolimi', "O'quv Bolimi User"),
            ('insp_user', 'inspekciya', 'Inspekciya User'),
            ('hr_user', 'kadirlar', 'HR User'),
            ('lib_user', 'library', 'Kutubxonachi'),
            ('store_user', 'ombor', 'Omborchi'),
        ]

        users = []
        for username, role, name in roles_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': name.split()[0],
                    'last_name': name.split()[1] if len(name.split()) > 1 else 'User',
                    'role': role,
                    'is_staff': True if role in ['rektor', 'admin'] else False
                }
            )
            if created:
                user.set_password('pass1234')
                user.save()
            users.append(user)
        
        # Ensure admin user exists with admin role
        admin, _ = User.objects.get_or_create(username='admin', defaults={'role': 'admin'})
        admin.set_password('admin')
        admin.save()
        users.append(admin)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(users)} users'))

        # 2. Seed Lesson Analysis
        subjects = ['Matematika', 'Fizika', 'Informatika', 'Tarix', 'Oliy Geometriya', 'Ingliz tili', 'Falsafa']
        teachers = ['Aliyev Vali', 'Karimova Gulnoza', 'Sodiqov Jasur', 'Azizov Bekzod', 'Normatov Sherzod']
        groups = ['101-A', '202-B', '303-C', '404-D']
        
        analyses = []
        for _ in range(20):
            score = random.randint(15, 95)
            status = 'approved' if score >= 20 else 'flagged'
            
            # If low score, some might already be processed
            if status == 'flagged' and random.random() > 0.5:
                status = random.choice(['inspected', 'approved'])

            a = LessonAnalysis.objects.create(
                subject=random.choice(subjects),
                teacher=random.choice(teachers),
                group=random.choice(groups),
                score=score,
                summary="Dars o'tilishi bo'yicha qisqacha xulosa. O'qituvchi mavzuni tushuntirishda pedagogik usullardan samarali foydalandi.",
                suggestion="Yangi texnologiyalardan ko'proq foydalanish tavsiya etiladi.",
                status=status,
                user=random.choice(users)
            )
            analyses.append(a)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(analyses)} lesson analyses'))

        # 3. Seed Work Plans
        plan_titles = [
            ("O'quv yili uchun ish rejasi", "prorektor"),
            ("Tyuterning haftalik ish rejasi", "tyuter"),
            ("Bo'lim yillik hisoboti", "bolim"),
            ("Strategik rivojlanish rejasi", "prorektor")
        ]
        
        for title, role in plan_titles:
            WorkPlan.objects.create(
                title_uz=title,
                description_uz=f"{title} bo'yicha batafsil ma'lumotlar bu yerda keltirilgan.",
                role=role,
                deadline=timezone.now().date() + timedelta(days=random.randint(5, 30)),
                is_completed=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded work plans'))

        # 4. Seed Library
        books = [
            ("Oliy Matematika", "Azimov A."),
            ("Fizika asoslari", "Rahimov B."),
            ("Python dasturlash tili", "Gvancho M."),
            ("O'zbekiston tarixi", "Jo'rayev N."),
            ("Iqtisodiyot nazariyasi", "Abdurahmonov Q.")
        ]
        
        for title, author in books:
            Book.objects.create(
                title_uz=title,
                author=author,
                category=random.choice(['textbook', 'manual', 'fiction']),
                total_copies=random.randint(5, 50),
                available_copies=random.randint(0, 5),
                published_year=random.randint(2010, 2024)
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded library'))

        # 5. Seed Inventory
        items = [
            ("Kompyuter i7", "electronics"),
            ("Proyektor Epson", "electronics"),
            ("Parta va stul", "furniture"),
            ("Doska (Whiteboard)", "furniture"),
            ("Printer HP", "electronics")
        ]
        
        for name, cat in items:
            Item.objects.create(
                name_uz=name,
                category=cat,
                quantity=random.randint(10, 100),
                unit='dona',
                location=f"{random.randint(1, 4)}-bino, {random.randint(100, 500)}-xona"
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded inventory'))

        # 6. Seed KPI Records
        for user in users:
            if user.role in ['tyuter', 'prorektor']:
                for m in range(1, 4): # Last 3 months
                    KPIRecord.objects.get_or_create(
                        user=user,
                        month=date(2026, m, 1),
                        defaults={
                            'score': random.randint(60, 98),
                            'comment': "Yaxshi ko'rsatkich."
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully seeded KPI records'))
        self.stdout.write(self.style.SUCCESS('Seed completed!'))
