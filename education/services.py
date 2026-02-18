import random
from education.models import LessonAnalysis


class AIService:
    @staticmethod
    def analyze_lesson(topic, teacher_name):
        """
        Simulates AI analysis of a lesson.
        Returns a dictionary with score, summary, suggestion, grade, and status.
        """
        score = random.randint(15, 95)
        grade = LessonAnalysis.calculate_grade(score)

        summary = f"Mavzu: {topic}. O'qituvchi: {teacher_name}. "
        suggestions = []

        if score >= 86:
            summary += "Dars juda yuqori saviyada o'tildi. O'quvchilar faol ishtirok etdi."
            suggestions = ["Tajriba almashish uchun ochiq dars tashkil etish tavsiya etiladi."]
        elif score >= 71:
            summary += "Dars yaxshi o'tildi, ammo ba'zi jihatlari yaxshilanishi mumkin."
            suggestions = ["Ko'rgazmali qurollardan ko'proq foydalanish.", "Talabalar bilan muloqotni oshirish."]
        elif score >= 56:
            summary += "Dars qoniqarli, lekin interaktiv metodlar yetishmayapti."
            suggestions = ["Ko'rgazmali qurollardan ko'proq foydalanish.", "O'quvchilarni guruhlarga bo'lib ishlash."]
        elif score >= 41:
            summary += "Darsda kamchiliklar mavjud. O'qituvchiga ogohlantirish beriladi."
            suggestions = ["Dars ishlanmasini qayta ko'rib chiqish.", "Metodist bilan maslahatlashish."]
        elif score >= 21:
            summary += "Darsda jiddiy kamchiliklar kuzatildi. Jarimaga tortish tavsiya etiladi."
            suggestions = ["Pedagogik malaka oshirish kursiga yuborish.", "Dars ishlanmasini qayta ko'rib chiqish."]
        else:
            summary += "Dars juda past saviyada o'tildi. Ishdan bo'shatish tavsiya etiladi."
            suggestions = ["Pedagogik malaka oshirish kursiga yuborish.", "Dars ishlanmasini qayta ko'rib chiqish.", "Mentor biriktirish."]

        return {
            'score': score,
            'grade': grade,
            'summary': summary,
            'suggestion': " ".join(suggestions),
            'status': 'pending',  # Always starts as pending, O'quv Bo'limi will grade
        }
