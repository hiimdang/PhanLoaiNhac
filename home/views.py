# imported our models
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from home.dl_model import predict_genre_from_audio_and_lyrics
from . models import Song
import json
import pickle
import os

# Create your views here.
from django.shortcuts import render, redirect
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    paginator= Paginator(Song.objects.all(), 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request,"index.html",context)

@csrf_exempt
def predict_genre(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        audio_path = data.get('audio_path')
        lyrics = data.get('lyrics', '')

        if not audio_path:
            return JsonResponse({'error': 'Missing audio_path'}, status=400)

        # Hàm này nhận đường dẫn file audio + lyrics, trả về thể loại
        (genre, conf) = predict_genre_from_audio_and_lyrics(audio_path, lyrics)

        return JsonResponse({'genre': genre, 'confidence': conf})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def model_view(request):
    history_path = os.path.join(BASE_DIR, 'home', 'predict_ults', 'history.pkl') 
    # Kiểm tra xem file history.pkl có tồn tại không
    if not os.path.exists(history_path):
        return render(request, 'model.html', {'error': 'History file not found'})

    with open(history_path, 'rb') as f:
        history = pickle.load(f)
        
    confusion_matrix = history.get('confusion_matrix', [])
    labels_text = history.get('labels_text', [])

    if hasattr(confusion_matrix, 'tolist'):
        confusion_matrix = confusion_matrix.tolist()

    confusion_matrix_with_labels = list(zip(confusion_matrix, labels_text))
    
    classification_report = history.get('classification_report', {})
    print(classification_report)
        
    context = {
        'loss': history.get('loss', []),
        'val_loss': history.get('val_loss', []),
        'accuracy': history.get('accuracy', []),
        'val_accuracy': history.get('val_accuracy', []),
        'learning_rate': history.get('learning_rate', []),
        'classification_report': history.get('classification_report', {}),
        'labels_text': history.get('labels_text', []),
        'confusion_matrix_with_labels': confusion_matrix_with_labels,  # thêm biến này
    }
    return render(request, 'model.html', context)