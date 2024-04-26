from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# URL düzenlemelerini içeren urlpatterns listesi
urlpatterns = [
    
    # Ana sayfa için URL yolu ve view fonksiyonu
    path('home/', views.index, name='home'),
    # Kategori ekleme sayfası için URL yolu ve view fonksiyonu
    path('add_category/', views.add_category, name='add_category'),
    # Soru ekleme sayfası için URL yolu ve view fonksiyonu
    path('add/', views.add_question, name='add_question'), 

    # Kategori seçim sayfası için URL yolu ve view fonksiyonu
    path('select_category', views.select_category, name='select_category'),
    # Konu seçim sayfası için dinamik URL yolu (kategoriye göre) ve view fonksiyonu
    path('topic/<int:category_id>/', views.select_topic, name='select_topic'),
    # Sınav seçim sayfası için dinamik URL yolu (konuya göre) ve view fonksiyonu
    path('exam/<int:topic_id>/', views.select_exam, name='select_exam'),
    # Soruları gösterme sayfası için dinamik URL yolu (sınava göre) ve view fonksiyonu
    path('questions/<int:exam_id>/', views.display_questions, name='display_questions'),
    # Kullanıcı dashboard sayfası için URL yolu ve view fonksiyonu
    path('dashboard/', views.dashboard, name='dashboard'),
    # Sonuç sayfası için URL yolu ve view fonksiyonu
    path('result/', views.result_page, name='result_page'),

    # Ayarlar sayfası için URL yolu ve view fonksiyonu
    path('settings/', views.settings_view, name='settings'),
    # Denetim sayfası için URL yolu ve view fonksiyonu
    path('denetim/', views.denetim_view, name='denetim'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Statik dosyalar için URL konfigürasyonu

