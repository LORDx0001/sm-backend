import random

class AIService:
    @staticmethod
    def analyze_lesson(topic, teacher_name):
        """
        Simulates AI analysis of a lesson.
        Returns a dictionary with score, summary, and suggestion.
        """
        # Mock logic to generate varied results
        score = random.randint(15, 95) # Wide range to test low/high score workflows
        
        status = 'approved'
        if score < 60:
            status = 'pending' # Needs review
        if score < 20:
            status = 'flagged' # Critical
            
        summary = f"Mavzu: {topic}. O'qituvchi: {teacher_name}. "
        suggestions = []
        
        if score > 80:
            summary += "Dars juda yuqori saviyada o'tildi. O'quvchilar faol ishtirok etdi."
            suggestions = ["Tajriba almashish uchun ochiq dars tashkil etish tavsiya etiladi."]
        elif score > 50:
            summary += "Dars qoniqarli, lekin interaktiv metodlar yetishmayapti."
            suggestions = ["Ko'rgazmali qurollardan ko'proq foydalanish.", "O'quvchilarni guruhlarga bo'lib ishlash."]
        else:
            summary += "Darsda jiddiy kamchiliklar kuzatildi. Mavzu to'liq ochib berilmadi."
            suggestions = ["Pedagogik malaka oshirish kursiga yuborish.", "Dars ishlanmasini qayta ko'rib chiqish.", "Mentor biriktirish."]

        return {
            'score': score,
            'summary': summary,
            'suggestion': " ".join(suggestions),
            'status': status
        }
