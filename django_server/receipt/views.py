import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.conf import settings
from .ocr_utils import extract_text_from_image_file
from openAi.receipt_parser import extract_fields_with_llm
import traceback
from .models import Receipt, PaymentMethod
import json
from django.core.serializers.json import DjangoJSONEncoder

@csrf_exempt
@require_POST
def upload_receipt(request):
    uid = request.POST.get('uid')
    receipt_files = request.FILES.getlist('receipt')

    if not uid or not receipt_files:
        return JsonResponse({'error': 'Missing uid or receipt(s)'}, status=400)

    saved_files = []
    combined_ocr = {
        'text_eng': [],
        'text_heb_eng': [],
        'text_heb': []
    }

    for file in receipt_files:
        filename = file.name
        upload_path = os.path.join('receipts', uid, filename)
        full_path = os.path.join(settings.MEDIA_ROOT, upload_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        saved_files.append(upload_path)

        ocr_result = extract_text_from_image_file(full_path)

        for key in combined_ocr:
            combined_ocr[key].append(ocr_result.get(key, ""))

    final_ocr = {
        key: "\n".join(combined_ocr[key]).strip()
        for key in combined_ocr
    }

    try:

        structured_data = extract_fields_with_llm(final_ocr)

        return JsonResponse({
            'status': 'success',
            'data': structured_data,
            'saved_files': saved_files
        })


    except Exception as e:
        traceback_str = traceback.format_exc()

        return JsonResponse({
            'error': 'Failed to process receipt with OpenAI',
            'details': str(e),
            'trace': traceback_str
        }, status=500)

@csrf_exempt
@require_POST
def create_receipt(request):
    data = json.loads(request.body)
    required_fields = ['uid', 'business_name', 'receipt_number', 'total_price', 'payment_method', 'credit_card_last_4_digits', 'items']
    for field in required_fields:
        if field not in data and field != 'credit_card_last_4_digits':
            return JsonResponse({'error': f'Missing field: {field}'}, status=400)
            

    if data['payment_method'] not in PaymentMethod.values:
        return JsonResponse({'error': 'Invalid payment method'}, status=400)

    # Save to DB
    receipt_obj = Receipt.objects.create(
        uid=data['uid'],
        business_name=data['business_name'],
        receipt_number=data['receipt_number'],
        total_price=data['total_price'],
        payment_method=data['payment_method'],
        credit_card_last_4_digits=data['credit_card_last_4_digits'],
        items=data['items'],
    )

    return JsonResponse({'status': 'success', 'receipt_id': receipt_obj.id})

@csrf_exempt
@require_GET
def get_all_receipts(request):
    uid = request.GET.get('uid')  # Get the UID from the query params

    if not uid:
        return JsonResponse({'error': 'Missing uid in query parameters'}, status=400)

    try:
        receipts = Receipt.objects.filter(uid=uid).values()
        return JsonResponse(list(receipts), safe=False, encoder=DjangoJSONEncoder)
    except Exception as e:
        return JsonResponse({'error': 'Failed to retrieve receipts'}, status=500)