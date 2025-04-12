import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .ocr_utils import extract_text_from_image_file
from openAi.receipt_parser import extract_fields_with_llm
import traceback

@csrf_exempt 
@require_POST
def upload_receipt(request):
    print("📥 Receipt upload request received", flush=True)
    uid = request.POST.get('uid')
    receipt_files = request.FILES.getlist('receipt')
    # print the uid
    print(f"UID: {uid}")

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

        # ✅ OCR this image
        ocr_result = extract_text_from_image_file(full_path)

        # ✅ Combine each OCR language result
        for key in combined_ocr:
            combined_ocr[key].append(ocr_result.get(key, ""))

    # ✅ Join results into one string per language
    final_ocr = {
        key: "\n".join(combined_ocr[key]).strip()
        for key in combined_ocr
    }

    # ✅ Send to GPT-4o for structured parsing
    try:
        print("🚀 Final OCR Result:")
        print(final_ocr)

        structured_data = extract_fields_with_llm(final_ocr)
        print("✅ Structured data received from LLM:")
        print(structured_data)
        return JsonResponse({
            'status': 'success',
            'data': structured_data,
            'saved_files': saved_files
        })

    except Exception as e:
        traceback_str = traceback.format_exc()
        print("❌ Exception while calling LLM:")
        print(traceback_str)

        return JsonResponse({
            'error': 'Failed to process receipt with OpenAI',
            'details': str(e),
            'trace': traceback_str
        }, status=500)