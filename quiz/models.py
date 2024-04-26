from django.db import models
from django.contrib.auth.models import User

# Kategori modeli
class Category(models.Model):
    name = models.CharField(max_length=100)  # Kategori adı

    def __str__(self):
        # Nesne string olarak adını döndürür
        return self.name

# Konu modeli
class Topic(models.Model):
    name = models.CharField(max_length=100)  # Konu adı
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Her konu bir kategoriye bağlıdır

    def __str__(self):
        # Nesne string olarak adını döndürür
        return self.name

# Sınav modeli
class Exam(models.Model):
    name = models.CharField(max_length=100)  # Sınav adı
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Her sınav bir konuya bağlıdır

    def __str__(self):
        # Nesne string olarak adını döndürür
        return self.name

# Soru modeli
class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ('low', 'Low'),  # Zorluk seçenekleri
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    BOOLEAN_CHOICES = (
        ('yes', 'Yes'),  # Evet/Hayır seçenekleri
        ('no', 'No'),
    )

    content = models.TextField()  # Soru içeriği
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)  # Soru için resim (opsiyonel)
    correct_answer = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)  # Doğru cevap
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)  # Zorluk seviyesi
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # Soruyu oluşturan kullanıcı
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Sorunun kategorisi
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Sorunun konusu
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)  # Sorunun ait olduğu sınav

    def __str__(self):
        # Nesne string olarak içeriğini döndürür
        return self.content

# Sonuç modeli
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Sonucu olan kullanıcı
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # İlgili soru
    answer = models.CharField(max_length=3, choices=Question.BOOLEAN_CHOICES)  # Kullanıcının verdiği cevap
    is_correct = models.BooleanField(default=False)  # Cevabın doğruluğu
    difficulty = models.CharField(max_length=10, choices=Question.DIFFICULTY_CHOICES)  # Sorunun zorluk seviyesi
    comments_allowed = models.BooleanField(default=True)  # Yorum yapılmasına izin verilip verilmediği

    def __str__(self):
        # Nesne string olarak kullanıcı adı, soru içeriği ve doğruluk durumunu döndürür
        return f"{self.user.username} - {self.question.content} - Correct: {self.is_correct}"

# Yönetici yorumu modeli
class AdminComment(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)  # İlgili sonuç
    admin = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorumu yapan admin
    comment = models.TextField()  # Yorum metni

    def __str__(self):
        # Nesne string olarak yorumun yapıldığı soru içeriği ve admin kullanıcı adını döndürür
        return f"Comment on {self.result.question.content} by {self.admin.username}"

# Kullanıcı yanıtı modeli
class UserResponse(models.Model):
    comment = models.ForeignKey(AdminComment, on_delete=models.CASCADE)  # İlgili yönetici yorumu
    response = models.TextField()  # Kullanıcının yanıtı
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yanıtı veren kullanıcı

    def __str__(self):
        # Nesne string olarak yanıt veren kullanıcının adını ve yanıtın yapıldığı yorumun soru içeriğini döndürür
        return f"Response by {self.user.username} on {self.comment.result.question.content}"
