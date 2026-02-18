import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import User
from education.models import LessonAnalysis, WorkPlan
from library.models import Book
from inventory.models import Item
from performance.models import KPIRecord


class Command(BaseCommand):
    help = 'Seed database with fake data for all workflow stages'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # === USERS ===
        roles_data = [
            ('rektor_user', 'rektor', 'Abdullayev', 'Karimjon'),
            ('prorektor_user', 'prorektor', 'Rahimov', 'Bobur'),
            ('tyuter_user', 'tyuter', 'Karimova', 'Nilufar'),
            ('tyuter2_user', 'tyuter', 'Sobirov', 'Jasur'),
            ('oquv_bolimi_user', 'oquv_bolimi', 'Toshmatov', 'Dilshod'),
            ('dekanat_user', 'dekanat', 'Normatov', 'Sardor'),
            ('kadirlar_user', 'kadirlar', 'Ergasheva', 'Madina'),
            ('kutubxona_user', 'kutubxona', 'Hamidova', 'Zulfiya'),
            ('ombor_user', 'ombor', 'Qodirov', 'Anvar'),
        ]

        users = []
        for username, role, last, first in roles_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'role': role,
                    'is_staff': role in ['rektor', 'admin']
                }
            )
            if created:
                user.set_password('pass1234')
                user.save()
            users.append(user)

        admin, _ = User.objects.get_or_create(username='admin', defaults={'role': 'rektor'})
        admin.set_password('admin')
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        users.append(admin)

        self.stdout.write(f'Successfully seeded {len(users)} users')

        # === LESSON ANALYSES at different workflow stages ===
        LessonAnalysis.objects.all().delete()

        subjects = [
            "Oliy Matematika", "Fizika", "Informatika", "Ingliz tili",
            "Kimyo", "Biologiya", "Tarix", "Iqtisodiyot",
            "Dasturlash", "Ma'lumotlar bazasi", "Elektrotexnika", "Falsafa"
        ]
        teachers = [
            "Karimov A.B.", "Hasanova M.D.", "Toshmatov S.K.", "Raximova G.N.",
            "Sobirov J.A.", "Ergashev D.F.", "Nazarov R.T.", "Yusupova L.M.",
            "Aliyev H.S.", "Mirzayev B.Q.", "Xolmatova N.I.", "Qodirov U.P."
        ]
        groups = ["101-A", "102-B", "201-A", "202-B", "301-A", "301-B", "401-A"]
        times = ["08:30", "09:50", "11:20", "13:00", "14:40", "16:00"]

        analyses = []

        # 1. Pending (AI analyzed, awaiting O'quv Bo'limi grading)  
        for i in range(6):
            score = random.randint(15, 95)
            grade = LessonAnalysis.calculate_grade(score)
            a = LessonAnalysis.objects.create(
                subject=random.choice(subjects),
                teacher=random.choice(teachers),
                group=random.choice(groups),
                time=random.choice(times),
                score=score,
                grade=grade,
                summary=f"Dars tahlili: {random.choice(subjects)} fani bo'yicha o'qituvchi dars o'tdi.",
                suggestion="O'quv jarayonini yaxshilash bo'yicha tavsiyalar.",
                status='pending',
                user=random.choice(users)
            )
            analyses.append(a)

        # 2. Graded but archived (good grades: alo, yaxshi, qoniqarli)
        for i in range(4):
            score = random.randint(56, 95)
            grade = LessonAnalysis.calculate_grade(score)
            LessonAnalysis.objects.create(
                subject=random.choice(subjects),
                teacher=random.choice(teachers),
                group=random.choice(groups),
                time=random.choice(times),
                score=score,
                grade=grade,
                edu_comment="Dars sifati yaxshi. Arxivga yo'naltirildi.",
                summary=f"Dars tahlili natijalari qoniqarli.",
                suggestion="Davom ettirish tavsiya etiladi.",
                status='archived',
                user=random.choice(users)
            )

        # 3. Sent to Dekanat (hayfsan/shtraf/haydash, awaiting document)
        problem_data = [
            (45, 'hayfsan', None, "O'qituvchi darsga yetarli tayyorlanmagan."),
            (30, 'shtraf', 500000, "Darsda jiddiy kamchiliklar. Jarima tayinlandi."),
            (18, 'haydash', None, "Dars o'tilmadi deyarli. Ishdan bo'shatish tavsiya."),
            (35, 'shtraf', 300000, "Past natija. Jarima tayinlandi."),
        ]
        for score, grade, fine, comment in problem_data:
            LessonAnalysis.objects.create(
                subject=random.choice(subjects),
                teacher=random.choice(teachers),
                group=random.choice(groups),
                time=random.choice(times),
                score=score,
                grade=grade,
                fine_amount=fine,
                edu_comment=comment,
                summary=f"Dars past saviyada. Dekanatga yo'naltirildi.",
                suggestion="Chora ko'rilishi kerak.",
                status='sent_to_dekanat',
                user=random.choice(users)
            )

        # 4. Dekanat ready (document prepared, awaiting Rektor)
        for i in range(2):
            score = random.choice([25, 42])
            grade = LessonAnalysis.calculate_grade(score)
            LessonAnalysis.objects.create(
                subject=random.choice(subjects),
                teacher=random.choice(teachers),
                group=random.choice(groups),
                time=random.choice(times),
                score=score,
                grade=grade,
                fine_amount=400000 if grade == 'shtraf' else None,
                edu_comment="O'quv bo'limi tomonidan tekshirildi.",
                dekanat_document=f"BUYRUQ #{random.randint(100, 999)}\n\nO'qituvchiga nisbatan {grade} darajasida chora ko'rilsin.\n\nAsos: dars tahlili natijasi.",
                dekanat_comment="Hujjat tayyorlandi, Rektorga yuborildi.",
                summary=f"Dars past saviyada. Rektor imzosi kutilmoqda.",
                suggestion="Zudlik bilan chora ko'rilishi lozim.",
                status='dekanat_ready',
                user=random.choice(users)
            )

        # 5. Rector signed (executed)
        for i in range(2):
            score = random.choice([15, 38])
            grade = LessonAnalysis.calculate_grade(score)
            LessonAnalysis.objects.create(
                subject=random.choice(subjects),
                teacher=random.choice(teachers),
                group=random.choice(groups),
                time=random.choice(times),
                score=score,
                grade=grade,
                fine_amount=250000 if grade == 'shtraf' else None,
                edu_comment="Tekshirildi.",
                dekanat_document=f"BUYRUQ #{random.randint(100, 999)}\n\nChora ko'rilsin.",
                dekanat_comment="Rektorga yuborildi.",
                rector_signed=True,
                rector_comment="Ijroga kiritilsin.",
                rector_signed_at=timezone.now() - timedelta(days=random.randint(1, 10)),
                summary=f"Bajarildi. Rektor tomonidan imzolandi.",
                suggestion="Chora ko'rildi.",
                status='rector_signed',
                user=random.choice(users)
            )

        self.stdout.write(f'Successfully seeded {LessonAnalysis.objects.count()} lesson analyses')

        # === WORK PLANS ===
        plan_titles = [
            ("O'quv yili uchun ish rejasi", "prorektor"),
            ("Tyuterning haftalik ish rejasi", "tyuter"),
            ("Fakultet bo'limi ish rejasi", "bolim"),
            ("Ilmiy tadqiqot rejasi", "prorektor"),
            ("Talabalar bilan ishlash rejasi", "tyuter"),
        ]

        for title, role in plan_titles:
            WorkPlan.objects.get_or_create(
                title_uz=title,
                defaults={
                    'description_uz': f"{title} bo'yicha batafsil ma'lumotlar.",
                    'role': role,
                    'deadline': timezone.now().date() + timedelta(days=random.randint(5, 30)),
                    'is_completed': random.choice([True, False])
                }
            )
        self.stdout.write('Successfully seeded work plans')

        # === LIBRARY ===
        books = [
            ("Oliy Matematika", "Azimov A."),
            ("Fizika asoslari", "Rahimov B."),
            ("Informatika va AT", "Toshmatov S."),
            ("Ingliz tili grammatikasi", "Karimova G."),
            ("Kimyo fanidan ma'ruzalar", "Sobirov D."),
        ]
        for title, author in books:
            Book.objects.get_or_create(
                title_uz=title,
                defaults={
                    'author': author,
                    'category': random.choice(['textbook', 'manual', 'fiction']),
                    'total_copies': random.randint(5, 50),
                    'available_copies': random.randint(0, 5),
                    'published_year': random.randint(2010, 2024)
                }
            )
        self.stdout.write('Successfully seeded library')

        # === INVENTORY ===
        items = [
            ("Kompyuter i7", "electronics"),
            ("Proyektor Epson", "electronics"),
            ("Parta va stul", "furniture"),
            ("Kitob javoni", "furniture"),
            ("Printer HP", "electronics"),
        ]
        for name, cat in items:
            Item.objects.get_or_create(
                name_uz=name,
                defaults={
                    'category': cat,
                    'quantity': random.randint(10, 100),
                    'unit': 'dona',
                    'location': f"{random.randint(1, 4)}-bino, {random.randint(100, 500)}-xona"
                }
            )
        self.stdout.write('Successfully seeded inventory')

        # === KPI ===
        for user in users:
            if user.role in ['tyuter', 'prorektor']:
                for m in range(1, 4):
                    KPIRecord.objects.get_or_create(
                        user=user,
                        month=date(2026, m, 1),
                        defaults={
                            'score': random.randint(60, 98),
                            'comment': "Yaxshi ko'rsatkich."
                        }
                    )
        self.stdout.write('Successfully seeded KPI records')

        self.stdout.write(self.style.SUCCESS('Seed completed!'))
