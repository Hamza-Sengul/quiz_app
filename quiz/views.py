from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Topic, Exam, Question, Result, UserResponse, AdminComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def index(request):
    # Ana sayfayı render etme işlevi
    return render(request, "index.html")

def add_category(request):
    # Kategori, konu ve sınav eklemek için POST isteklerini ele alma fonksiyonu
    if request.method == 'POST':
        if 'add_category' in request.POST:
            category_name = request.POST.get('category_name')
            if category_name:
                # Yeni bir kategori oluşturur
                Category.objects.create(name=category_name)
        elif 'add_topic' in request.POST:
            category_id = request.POST.get('category')
            topic_name = request.POST.get('topic_name')
            if category_id and topic_name:
                # Belirtilen kategori ID'sine sahip kategoriyi getirir
                category = Category.objects.get(pk=category_id)
                # Yeni bir konu oluşturur ve kategoriye bağlar
                Topic.objects.create(name=topic_name, category=category)
        elif 'add_exam' in request.POST:
            topic_id = request.POST.get('topic')
            exam_name = request.POST.get('exam_name')
            if topic_id and exam_name:
                # Belirtilen konu ID'sine sahip konuyu getirir
                topic = Topic.objects.get(pk=topic_id)
                # Yeni bir sınav oluşturur ve konuya bağlar
                Exam.objects.create(name=exam_name, topic=topic)
        # İşlem tamamlandıktan sonra 'add_category' sayfasına yönlendirme yapar
        return redirect('add_category')

    # POST dışındaki istekler için tüm kategorileri ve konuları getirir
    categories = Category.objects.all()
    topics = Topic.objects.all()
    # 'add_category.html' şablonunu kategoriler ve konular ile birlikte render eder
    return render(request, 'add_category.html', {'categories': categories, 'topics': topics})

def add_question(request):
    # Soru eklemek için POST isteklerini ele alma fonksiyonu
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        correct_answer = request.POST.get('correct_answer')
        difficulty = request.POST.get('difficulty')
        category_id = request.POST.get('category')
        topic_id = request.POST.get('topic')
        exam_id = request.POST.get('exam')

        # Gerekli alanların doldurulduğunu kontrol eder
        if content and correct_answer and difficulty and category_id and topic_id and exam_id:
            try:
                # İlgili kategori, konu ve sınavı veritabanından çeker
                category = Category.objects.get(id=category_id)
                topic = Topic.objects.get(id=topic_id)
                exam = Exam.objects.get(id=exam_id)

                # Yeni bir soru nesnesi oluşturur ve veritabanına kaydeder
                new_question = Question.objects.create(
                    content=content,
                    image=image,
                    correct_answer=correct_answer,
                    difficulty=difficulty,
                    creator=request.user,
                    category=category,
                    topic=topic,
                    exam=exam
                )
                # Soru başarıyla eklendi mesajı gösterir
                messages.success(request, 'Question added successfully!')
                # Ana sayfaya yönlendirme yapar
                return redirect('home')
            except (Category.DoesNotExist, Topic.DoesNotExist, Exam.DoesNotExist) as e:
                # Veritabanında ilgili nesneler bulunamazsa hata mesajı gösterir
                messages.error(request, 'An error occurred while adding the question.')
        else:
            # Gerekli alanlar doldurulmadıysa hata mesajı gösterir
            messages.error(request, 'Please fill in all the required fields.')
    
    # POST dışındaki isteklerde veya form doğru doldurulmadıysa, formu tekrar gösterir
    return render(request, 'add_question.html', {'categories': Category.objects.all(),
                                                 'topics': Topic.objects.all(),
                                                 'exams': Exam.objects.all()})








def select_category(request):
    # Tüm kategorileri veritabanından çeker
    categories = Category.objects.all()
    # 'select_category.html' şablonunu kategoriler ile birlikte render eder
    return render(request, 'select_category.html', {'categories': categories})

def select_topic(request, category_id):
    # Belirtilen kategori ID'ye göre kategori nesnesini getirir veya 404 hatası verir
    category = get_object_or_404(Category, pk=category_id)
    # Belirtilen kategoriye bağlı konuları getirir
    topics = category.topic_set.all()
    # 'select_topic.html' şablonunu kategori ve konular ile birlikte render eder
    return render(request, 'select_topic.html', {'category': category, 'topics': topics})

def select_exam(request, topic_id):
    # Belirtilen konu ID'ye göre konu nesnesini getirir veya 404 hatası verir
    topic = get_object_or_404(Topic, pk=topic_id)
    # Belirtilen konuya bağlı sınavları getirir
    exams = topic.exam_set.all()
    # 'select_exam.html' şablonunu konu ve sınavlar ile birlikte render eder
    return render(request, 'select_exam.html', {'topic': topic, 'exams': exams})

def display_questions(request, exam_id):
    # Belirtilen sınav ID'ye göre sınav nesnesini getirir veya 404 hatası verir
    exam = get_object_or_404(Exam, pk=exam_id)
    # Belirtilen sınava bağlı soruları getirir
    questions = exam.question_set.all()

    if request.method == 'POST':
        for question in questions:
            answer = request.POST.get(str(question.id))
            is_correct = answer == question.correct_answer
            difficulty = question.difficulty
            
            # Kullanıcının daha önce bu soruya cevap verip vermediğini kontrol eder
            existing_result = Result.objects.filter(user=request.user, question=question).exists()
            if existing_result:
                # Soru daha önce cevaplandıysa uyarı mesajı gösterir
                messages.warning(request, f"Question '{question.content}' has already been answered.")
            else:
                # Cevabı sonuçlar tablosuna kaydeder
                Result.objects.create(
                    user=request.user,
                    question=question,
                    answer=answer,
                    is_correct=is_correct,
                    difficulty=difficulty
                )
        # Sonuçlar başarıyla kaydedildi mesajını gösterir
        messages.success(request, 'Results saved successfully!')
        # Kategori seçim sayfasına yönlendirme yapar
        return redirect('select_category')

    # 'display_questions.html' şablonunu sınav ve sorular ile birlikte render eder
    return render(request, 'display_questions.html', {'exam': exam, 'questions': questions})


@login_required
def dashboard(request):
    user = request.user

    # Kullanıcıya ait toplam soru sayısını getirir
    total_questions = Question.objects.filter(creator=user).count()
    # Sistemdeki toplam kategori sayısını getirir
    total_categories = Category.objects.count()
    # Sistemdeki toplam konu sayısını getirir
    total_topics = Topic.objects.count()
    # Sistemdeki toplam sınav sayısını getirir
    total_exams = Exam.objects.count()

    # Kullanıcının sonuçlarını getirir
    user_results = Result.objects.filter(user=user)
    # Kullanıcının denediği toplam soru sayısını hesaplar
    total_attempted = user_results.count()
    # Kullanıcının doğru cevapladığı toplam soru sayısını hesaplar
    total_correct = user_results.filter(is_correct=True).count()
    # Kullanıcının yanlış cevapladığı toplam soru sayısını hesaplar
    total_incorrect = total_attempted - total_correct

    # Genel başarı oranını hesaplar
    overall_success_rate = int((total_correct / total_attempted) * 100) if total_attempted > 0 else 0

    # Zorluk seviyelerine göre başarı oranlarını hesaplar
    difficulty_levels = Question.DIFFICULTY_CHOICES
    success_rates = {}
    for level in difficulty_levels:
        level_results = user_results.filter(question__difficulty=level[0])
        total_level_attempted = level_results.count()
        total_level_correct = level_results.filter(is_correct=True).count()
        success_rate = int((total_level_correct / total_level_attempted) * 100) if total_level_attempted > 0 else 0
        success_rates[level[0]] = success_rate

    # Yanlış cevaplanan sorular ve ilgili yorumları getirir
    incorrect_results = user_results.filter(is_correct=False)
    comments = AdminComment.objects.filter(result__in=incorrect_results)

    context = {
        'username': user.username,
        'email': user.email,
        'total_questions': total_questions,
        'total_categories': total_categories,
        'total_topics': total_topics,
        'total_exams': total_exams,
        'total_attempted': total_attempted,
        'total_correct': total_correct,
        'total_incorrect': total_incorrect,
        'success_rate': overall_success_rate,
        'success_rates': success_rates,
        'incorrect_results': incorrect_results,
        'comments': comments,
    }

    # 'dashboard.html' şablonunu kullanıcı verileri ile birlikte render eder
    return render(request, 'dashboard.html', context)


def result_page(request):
    # Kullanıcının sonuçlarını zorluk seviyelerine göre getirir
    user_results = Result.objects.filter(user=request.user)
    difficulty_levels = [choice[0] for choice in Question.DIFFICULTY_CHOICES]

    result_data = {}
    for level in difficulty_levels:
        # Belirli bir zorluk seviyesindeki kullanıcı sonuçlarını getirir
        user_results_by_level = user_results.filter(difficulty=level)
        total_questions = user_results_by_level.count()
        correct_answers = user_results_by_level.filter(is_correct=True).count()

        # Başarı oranını hesaplar
        success_rate = 0
        if total_questions != 0:
            success_rate = (correct_answers / total_questions) * 100

        result_data[level] = {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'success_rate': success_rate
        }

    # 'result_page.html' şablonunu sonuç verileri ile birlikte render eder
    return render(request, 'result_page.html', {'result_data': result_data})

def settings_view(request):
    if request.method == 'POST':
        if 'end_comments' in request.POST:
            result_id = request.POST.get('result_id')
            result = Result.objects.get(id=result_id)
            # Yorum yapmayı devre dışı bırakır
            result.comments_allowed = False
            result.save()
            # Ayarlar sayfasına yönlendirme yapar
            return redirect('settings')
        elif 'comment' in request.POST:
            result_id = request.POST.get('result_id')
            comment_text = request.POST.get('comment')
            result = Result.objects.get(id=result_id)
            if result.comments_allowed:
                # Yeni bir yorum oluşturur ve kaydeder
                AdminComment.objects.create(result=result, comment=comment_text, admin=request.user)
            return redirect('settings')

    # Yanlış cevaplanan sonuçları getirir
    incorrect_results = Result.objects.filter(is_correct=False)
    # 'settings.html' şablonunu sonuçlar ile birlikte render eder
    return render(request, 'settings.html', {'results': incorrect_results})

from django.db.models import Exists, OuterRef

def denetim_view(request):
    # Yönetici yorumlarını getirir ve kullanıcının yanıtladığı yorumları belirtir
    admin_comments = AdminComment.objects.select_related('result').annotate(
        has_responded=Exists(UserResponse.objects.filter(comment=OuterRef('pk'), user=request.user))
    ).all()

    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        response_text = request.POST.get('response')
        comment = AdminComment.objects.get(id=comment_id)

        # Kullanıcının daha önce yanıt verip vermediğini kontrol eder
        if not comment.userresponse_set.filter(user=request.user).exists():
            if comment.result.comments_allowed:
                # Yeni bir kullanıcı yanıtı oluşturur ve kaydeder
                UserResponse.objects.create(comment=comment, response=response_text, user=request.user)
                # Denetim sayfasına yönlendirme yapar
                return redirect('denetim')
            else:
                # Yorumlar kapalıysa hata mesajı verir
                return HttpResponse("Comments are closed for this question.", status=403)

    # 'denetim.html' şablonunu yönetici yorumları ile birlikte render eder
    return render(request, 'denetim.html', {'comments': admin_comments})




