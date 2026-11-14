def get_treatment(disease):

    disease_name = disease.lower().replace("___", " ").replace("_", " ")

    treatments = {

        "healthy": {
            "status": "Healthy Plant",
            "symptoms": "पौधा स्वस्थ दिखाई दे रहा है।",
            "treatment": "किसी विशेष उपचार की आवश्यकता नहीं है।",
            "prevention": "नियमित रूप से पौधे की देखभाल करें।"
        },

        "early blight": {
            "status": "Early Blight Detected",
            "symptoms": "पत्तियों पर भूरे गोल धब्बे और पीले किनारे दिखाई देते हैं।",
            "treatment": "प्रभावित पत्तियों को हटाएँ। उचित उपचार के लिए कृषि विशेषज्ञ से सलाह लें।",
            "prevention": "पौधों के बीच उचित दूरी रखें और पत्तियों को अनावश्यक रूप से गीला न करें।"
        },

        "late blight": {
            "status": "Late Blight Detected",
            "symptoms": "पत्तियों पर गहरे भूरे या काले धब्बे दिखाई देते हैं।",
            "treatment": "प्रभावित हिस्सों को हटाएँ और कृषि विशेषज्ञ से उचित उपचार की सलाह लें।",
            "prevention": "खेत में जलभराव न होने दें और पौधों के बीच हवा का आवागमन बनाए रखें।"
        },

        "bacterial spot": {
            "status": "Bacterial Spot Detected",
            "symptoms": "पत्तियों पर छोटे गहरे धब्बे दिखाई देते हैं।",
            "treatment": "संक्रमित पत्तियों को हटाएँ और कृषि विशेषज्ञ से सलाह लें।",
            "prevention": "स्वच्छ बीजों का उपयोग करें और गीले पौधों को छूने से बचें।"
        },

        "powdery mildew": {
            "status": "Powdery Mildew Detected",
            "symptoms": "पत्तियों पर सफेद पाउडर जैसा पदार्थ दिखाई देता है।",
            "treatment": "प्रभावित पत्तियों को हटाएँ और विशेषज्ञ से उचित उपचार पूछें।",
            "prevention": "पौधों के बीच पर्याप्त दूरी रखें।"
        },

        "leaf mold": {
            "status": "Leaf Mold Detected",
            "symptoms": "पत्तियों के नीचे पीले या भूरे रंग की परत दिखाई दे सकती है।",
            "treatment": "संक्रमित पत्तियों को हटाएँ।",
            "prevention": "नमी और हवा के आवागमन को नियंत्रित रखें।"
        },

        "septoria": {
            "status": "Septoria Leaf Spot Detected",
            "symptoms": "पत्तियों पर छोटे गोल धब्बे दिखाई देते हैं।",
            "treatment": "प्रभावित पत्तियों को हटाकर नष्ट करें।",
            "prevention": "खेत में सफाई रखें और पत्तियों को गीला करने से बचें।"
        },

        "spider mite": {
            "status": "Spider Mite Detected",
            "symptoms": "पत्तियों पर छोटे पीले धब्बे और जाले दिखाई दे सकते हैं।",
            "treatment": "पत्तियों की जाँच करें और कृषि विशेषज्ञ से नियंत्रण के उपाय पूछें।",
            "prevention": "पौधों की नियमित निगरानी करें।"
        },

        "mosaic virus": {
            "status": "Mosaic Virus Detected",
            "symptoms": "पत्तियों पर हल्के और गहरे हरे रंग के धब्बे दिखाई देते हैं।",
            "treatment": "संक्रमित पौधों को अलग करें। विशेषज्ञ से सलाह लें।",
            "prevention": "स्वस्थ बीजों का उपयोग करें और कीटों को नियंत्रित रखें।"
        },

        "yellow leaf curl": {
            "status": "Yellow Leaf Curl Detected",
            "symptoms": "पत्तियाँ पीली होकर मुड़ने लगती हैं।",
            "treatment": "प्रभावित पौधों की जाँच करवाएँ और विशेषज्ञ की सलाह लें।",
            "prevention": "सफेद मक्खी जैसे कीटों की नियमित निगरानी करें।"
        },

        "black rot": {
            "status": "Black Rot Detected",
            "symptoms": "पत्तियों पर गहरे रंग के धब्बे दिखाई देते हैं।",
            "treatment": "संक्रमित पौधों के हिस्सों को हटाएँ।",
            "prevention": "खेत और कृषि उपकरण साफ रखें।"
        },

        "cedar apple rust": {
            "status": "Cedar Apple Rust Detected",
            "symptoms": "पत्तियों पर नारंगी या पीले धब्बे दिखाई दे सकते हैं।",
            "treatment": "प्रभावित पत्तियों की जाँच करवाएँ और विशेषज्ञ से सलाह लें।",
            "prevention": "बगीचे की नियमित सफाई करें।"
        },

        "common rust": {
            "status": "Common Rust Detected",
            "symptoms": "पत्तियों पर लाल-भूरे रंग के छोटे धब्बे दिखाई देते हैं।",
            "treatment": "प्रभावित पत्तियों की निगरानी करें और विशेषज्ञ से सलाह लें।",
            "prevention": "रोग प्रतिरोधी किस्मों का उपयोग करें।"
        },

        "leaf blight": {
            "status": "Leaf Blight Detected",
            "symptoms": "पत्तियों पर भूरे या सूखे धब्बे दिखाई देते हैं।",
            "treatment": "संक्रमित पत्तियों को हटाएँ।",
            "prevention": "खेत में उचित दूरी और साफ-सफाई बनाए रखें।"
        },

        "esca": {
            "status": "Esca Disease Detected",
            "symptoms": "अंगूर की पत्तियों पर सूखे और रंग बदले हुए हिस्से दिखाई दे सकते हैं।",
            "treatment": "प्रभावित बेलों की जाँच कृषि विशेषज्ञ से करवाएँ।",
            "prevention": "छँटाई के उपकरण साफ रखें।"
        },

        "cercospora": {
            "status": "Cercospora Disease Detected",
            "symptoms": "पत्तियों पर गोल भूरे धब्बे दिखाई देते हैं।",
            "treatment": "प्रभावित पत्तियों को हटाएँ।",
            "prevention": "खेत में उचित हवा का आवागमन बनाए रखें।"
        },

        "huanglongbing": {
            "status": "Citrus Greening Detected",
            "symptoms": "नींबू या सिट्रस की पत्तियाँ पीली और असमान रंग की हो सकती हैं।",
            "treatment": "पौधे की पुष्टि कृषि विशेषज्ञ से करवाएँ।",
            "prevention": "संक्रमित पौधों और कीटों की नियमित निगरानी करें।"
        }
    }

    for key, value in treatments.items():

        if key in disease_name:

            return value

    return {
        "status": "Information Unavailable",
        "symptoms": "इस बीमारी के लक्षणों की जानकारी उपलब्ध नहीं है।",
        "treatment": "कृषि विशेषज्ञ से सलाह लें।",
        "prevention": "पौधों की नियमित निगरानी और साफ-सफाई करें।"
    }