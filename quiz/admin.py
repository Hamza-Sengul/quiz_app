from django.contrib import admin
from .models import Category, Topic, Exam, Question, Result, AdminComment, UserResponse

# Kategori modelini Django admin paneline kaydetme
admin.site.register(Category)
# Konu modelini Django admin paneline kaydetme
admin.site.register(Topic)
# Sınav modelini Django admin paneline kaydetme
admin.site.register(Exam)
# Soru modelini Django admin paneline kaydetme
admin.site.register(Question)
# Sonuç modelini Django admin paneline kaydetme
admin.site.register(Result)
# Yönetici yorum modelini Django admin paneline kaydetme
admin.site.register(AdminComment)
# Kullanıcı yanıtı modelini Django admin paneline kaydetme
admin.site.register(UserResponse)
