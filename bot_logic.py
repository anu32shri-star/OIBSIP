# Food Delivery Support Knowledge Base
FOOD_DELIVERY_KB = {
    "order_status": {
        "keywords": ["order", "status", "कहाँ है", "order kahan hai", "delivery", "pahuncha"],
        "response": "आपका खाना रेस्टोरेंट से निकल चुका है और लगभग 10 मिनट में आपके पास पहुँच जाएगा।"
    },
    "missing_item": {
        "keywords": ["missing", "item", "khana kam hai", "nahi hai", "भोजन", "गायब"],
        "response": "हमें खेद है कि आपका कुछ सामान छूट गया है। हमने इस पर तुरंत कार्रवाई कर दी है और रिफंड आपके वॉलेट में भेज दिया गया है।"
    },
    "cancel_order": {
        "keywords": ["cancel", "radd", "रद्द", "बदलाव", "order cancel"],
        "response": "आपका ऑर्डर रद्द कर दिया गया है। भुगतान की गई राशि 24 घंटे के भीतर आपके खाते में वापस आ जाएगी।"
    },
    "delivery_boy": {
        "keywords": ["driver", "delivery partner", "phone number", "नंबर", "बात करनी है"],
    "response": "आपकी सुरक्षा के लिए हमने डिलीवरी पार्टनर का सीधा संपर्क नंबर आपकी ऐप स्क्रीन पर भेज दिया है।"
    }
}

def get_bot_response(user_text: str) -> str:
    user_text_lower = user_text.lower()
    
    for intent, data in FOOD_DELIVERY_KB.items():
        if any(kw in user_text_lower for kw in data["keywords"]):
            return data["response"]
            
    return "क्षमा करें, मुझे आपका प्रश्न समझ नहीं आया। क्या आप अपना सवाल दोबारा पूछ सकते हैं?"