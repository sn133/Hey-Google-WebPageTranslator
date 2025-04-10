from django.shortcuts import render
from django.http import HttpResponse
import razorpay
import re
import requests
from bs4 import BeautifulSoup
#from .models import Translation
from googletrans import Translator
# from translate import Translator  # Import the translation library

#import your Razorpay API keys from settings
from TranslationTool.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRETKEY
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRETKEY))

def generate_order(request):
    if request.method == 'POST':
        # Create a Razorpay order
            order_amount = 100  # Set your desired amount in paise (e.g., 100 paise = 1 INR)
            order_currency = 'INR'
            order_receipt = 'receipt#1'

            order = client.order.create({
                'amount': order_amount,
                'currency': order_currency,
                'receipt': order_receipt,
                'payment_capture': 1
            })

            order_id = order['id']

            # Pass the Razorpay order details to the template
            context = {
                'order_id': order_id,
                'order_amount': order_amount,
                'order_currency': order_currency,
                'api_key': RAZORPAY_API_KEY,
                
            }
 
            return render(request, 'razorpay_payment.html', context)
    else:
        return HttpResponse("Error: Invalid request method.")
    
def welcome_page(request):
    return render(request, 'welcome.html')
    
def home(request):
    return render(request,'translation_form.html')

def split_text(text, max_length):
    """
    Split the text into smaller chunks of maximum length.
    """
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def translate_paragraphs(paragraphs, target_language='en'):
    """
    Translate a list of paragraphs to the target language.
    """
    translator = Translator()

    translated_paragraphs = []
    for paragraph in paragraphs:
        # Translate the paragraph to the target language
        translated_text = translator.translate(paragraph, dest=target_language)
        translated_paragraphs.append(translated_text.text)

    return translated_paragraphs

def translate_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        target_language = request.POST['targetLanguage']
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text()
            paragraph_elements = soup.find_all('p')
            paragraphs = [p.get_text().strip() for p in paragraph_elements]

            # Translate paragraphs individually and split into smaller chunks
            max_query_length = 500
            translated_paragraphs = []
            for paragraph in paragraphs:
                paragraph_chunks = split_text(paragraph, max_query_length)
                translated_chunks = translate_paragraphs(paragraph_chunks, target_language)
                translated_paragraph = ' '.join(translated_chunks)
                translated_paragraphs.append(translated_paragraph)

            translated_text = '\n'.join(translated_paragraphs)

            # Now you can use the regular expression to extract a specific group
            pattern = r'pattern_to_match_text'
            match = re.search(pattern, translated_text)
            group_value = match.group(1) if match else None

            # Pass the translated text and extracted group value to the template
            context = {
                "translated_text": translated_text,
                "group_value": group_value
            }

            return render(request, 'translation_result.html', {'context': context, 'text_content': text_content, 'translated_text': translated_text})
        else:
            return HttpResponse("Error: Unable to fetch content from the provided URL.")
    else:
        return HttpResponse("Error: Invalid request method.")

