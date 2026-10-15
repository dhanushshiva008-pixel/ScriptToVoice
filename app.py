from flask import Flask, request, jsonify, render_template_string, send_from_directory
import asyncio
import os
import uuid
import edge_tts

app = Flask(__name__)

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "te-IN-ShrutiNeural": "తెలుగు - ఆడ వాయిస్",
    "te-IN-MohanNeural": "తెలుగు - మగ వాయిస్",
    "hi-IN-SwaraNeural": "హిందీ - ఆడ వాయిస్",
    "hi-IN-MadhurNeural": "హిందీ - మగ వాయిస్",
    "en-IN-NeerjaNeural": "ఇంగ్లీష్ - ఆడ వాయిస్",
    "en-IN-PrabhatNeural": "ఇంగ్లీష్ - మగ వాయిస్",
    "ta-IN-PallaviNeural": "తమిళం - ఆడ వాయిస్",
    "ta-IN-ValluvarNeural": "తమిళం - మగ వాయిస్",
    "kn-IN-SapnaNeural": "కన్నడ - ఆడ వాయిస్",
    "kn-IN-GaganNeural": "కన్నడ - మగ వాయిస్",
    "ml-IN-SobhanaNeural": "మలయాళం - ఆడ వాయిస్",
    "ml-IN-MidhunNeural": "మలయాళం - మగ వాయిస్",
    "bn-IN-BashkarNeural": "బెంగాలీ - మగ వాయిస్",
    "bn-IN-TanishaaNeural": "బెంగాలీ - ఆడ వాయిస్",
    "gu-IN-DhwaniNeural": "గుజరాతీ - ఆడ వాయిస్",
    "gu-IN-NiranjanNeural": "గుజరాతీ - మగ వాయిస్",
    "mr-IN-AarohiNeural": "మరాఠీ - ఆడ వాయిస్",
    "mr-IN-ManoharNeural": "మరాఠీ - మగ వాయిస్",
    "ne-NP-HemkalaNeural": "నేపాలీ - ఆడ వాయిస్",
    "ne-NP-SagarNeural": "నేపాలీ - మగ వాయిస్",
    "ur-IN-GulNeural": "ఉర్దూ - ఆడ వాయిస్",
    "ur-IN-SalmanNeural": "ఉర్దూ - మగ వాయిస్",
}

HTML = '\n<!DOCTYPE html>\n<html lang="te">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="theme-color" content="#0b1020">\n<title>ScriptToVoice</title>\n<style>\n*{box-sizing:border-box}\nbody{margin:0;min-height:100vh;padding:22px 15px;background:radial-gradient(ellipse at top,#202b50 0%,#0b1020 55%,#080b13 100%);color:#f5f7ff;font-family:system-ui,Arial,sans-serif}\n.container{max-width:520px;margin:0 auto}\n.top{display:flex;align-items:center;gap:13px;margin:10px 0 24px}\n.logo{width:55px;height:55px;border-radius:18px;background:linear-gradient(135deg,#7c5cff,#20c9e8);display:grid;place-items:center;font-size:27px;box-shadow:0 8px 28px #6655ff45}\nh1{font-size:25px;margin:0;letter-spacing:-.6px}\n.subtitle{color:#aebbd5;margin:5px 0 0;font-size:14px}\n.card{background:#121a2bd9;border:1px solid #34415e;border-radius:24px;padding:21px;box-shadow:0 18px 55px #0004}\n.badge{display:inline-flex;align-items:center;gap:7px;padding:7px 11px;border:1px solid #334765;border-radius:30px;color:#a8e9ff;font-size:12px;margin-bottom:17px}\nlabel{display:block;font-size:14px;font-weight:650;color:#dbe5fa;margin:17px 0 8px}\ntextarea,select{display:block;width:100%;border:1px solid #34435f;border-radius:13px;background:#0c1323;color:#f5f7ff;padding:14px;font:inherit;outline:none}\ntextarea{min-height:155px;resize:vertical;line-height:1.65}\ntextarea:focus,select:focus{border-color:#67cfff;box-shadow:0 0 0 3px #36baff18}\nselect{min-height:49px}\nbutton{width:100%;border:0;border-radius:14px;padding:15px;margin-top:21px;background:linear-gradient(100deg,#7658ff,#238fe8);color:white;font:inherit;font-weight:750;font-size:16px;box-shadow:0 8px 24px #5366ff30}\nbutton:disabled{opacity:.6}\n.note{color:#b6c2d8;font-size:13px;line-height:1.6;overflow-wrap:anywhere}\n#status{padding:12px;background:#0c1323;border:1px solid #273650;border-radius:12px}\naudio{width:100%;margin-top:12px}\na{color:#79dfff;font-weight:700}\n.footer{text-align:center;color:#8190ac;font-size:12px;margin:18px 0}\n.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}\n@media(max-width:380px){.card{padding:16px}.grid{grid-template-columns:1fr}h1{font-size:22px}}\n</style>\n</head>\n<body>\n<div class="container">\n  <div class="top">\n    <div class="logo">🎙️</div>\n    <div><h1>ScriptToVoice</h1><p class="subtitle" data-i="subtitle">మీ స్క్రిప్ట్\u200cకు ప్రాణం పోయండి</p></div>\n  </div>\n\n  <div class="card">\n    <div class="badge">✦ <span data-i="badge">AI వాయిస్ స్టూడియో</span></div>\n\n    <label for="uiLang" data-i="uiLanguage">యాప్ భాష</label>\n    <select id="uiLang">\n      <option value="te">తెలుగు</option>\n      <option value="hi">हिन्दी</option>\n      <option value="en">English</option>\n      <option value="ta">தமிழ்</option>\n      <option value="kn">ಕನ್ನಡ</option>\n      <option value="ml">മലയാളം</option>\n      <option value="bn">বাংলা</option>\n      <option value="gu">ગુજરાતી</option>\n      <option value="mr">मराठी</option>\n      <option value="ne">नेपाली</option>\n      <option value="ur">اردو</option>\n    </select>\n\n    <label for="script" data-i="scriptLabel">మీ స్క్రిప్ట్</label>\n    <textarea id="script" maxlength="5000" data-ph="scriptPlaceholder" placeholder="మీ కథనం ఇక్కడ టైప్ చేయండి..."></textarea>\n    <p class="note" data-i="limit">గరిష్ఠంగా 5000 అక్షరాలు</p>\n\n    <div class="grid">\n      <div>\n        <label for="voice" data-i="voiceLabel">వాయిస్ ఎంచుకోండి</label>\n        <select id="voice">\n          {% for id, label in voices.items() %}\n          <option value="{{ id }}">{{ label }}</option>\n          {% endfor %}\n        </select>\n      </div>\n      <div>\n        <label for="narration" data-i="styleLabel">కథనం శైలి</label>\n        <select id="narration">\n          <option value="mythology" data-i="mythology">🎬 పురాణ కథనం</option>\n          <option value="normal" data-i="normal">📖 సాధారణ కథనం</option>\n        </select>\n      </div>\n    </div>\n\n    <button id="generate" onclick="generateVoice()">🎙️ <span data-i="generate">వాయిస్ తయారు చేయండి</span></button>\n    <p id="status" class="note" data-i="ready">స్క్రిప్ట్ రాసి వాయిస్ తయారు చేయండి.</p>\n    <audio id="player" controls hidden></audio>\n    <p><a id="download" hidden download="ScriptToVoice.mp3" data-i="download">⬇️ MP3 డౌన్\u200cలోడ్ చేసుకోండి</a></p>\n    <p class="note" data-i="internet">వాయిస్ తయారీకి ఇంటర్నెట్ అవసరం.</p>\n  </div>\n  <div class="footer">ScriptToVoice · Voice your story</div>\n</div>\n\n<script>\nconst translations = {\nte:{subtitle:"మీ స్క్రిప్ట్\u200cకు ప్రాణం పోయండి",badge:"AI వాయిస్ స్టూడియో",uiLanguage:"యాప్ భాష",scriptLabel:"మీ స్క్రిప్ట్",scriptPlaceholder:"మీ కథనం ఇక్కడ టైప్ చేయండి...",limit:"గరిష్ఠంగా 5000 అక్షరాలు",voiceLabel:"వాయిస్ ఎంచుకోండి",styleLabel:"కథనం శైలి",mythology:"🎬 పురాణ కథనం",normal:"📖 సాధారణ కథనం",generate:"వాయిస్ తయారు చేయండి",ready:"స్క్రిప్ట్ రాసి వాయిస్ తయారు చేయండి.",working:"వాయిస్ తయారవుతోంది. దయచేసి వేచి ఉండండి...",done:"వాయిస్ తయారైంది! వినండి లేదా MP3 డౌన్\u200cలోడ్ చేసుకోండి.",empty:"ముందుగా మీ స్క్రిప్ట్ టైప్ చేయండి.",problem:"సమస్య: ",failed:"వాయిస్ తయారు కాలేదు.",download:"⬇️ MP3 డౌన్\u200cలోడ్ చేసుకోండి",internet:"వాయిస్ తయారీకి ఇంటర్నెట్ అవసరం."},\nhi:{subtitle:"अपनी स्क्रिप्ट को आवाज़ दें",badge:"AI वॉइस स्टूडियो",uiLanguage:"ऐप की भाषा",scriptLabel:"आपकी स्क्रिप्ट",scriptPlaceholder:"अपना टेक्स्ट यहाँ लिखें...",limit:"अधिकतम 5000 अक्षर",voiceLabel:"आवाज़ चुनें",styleLabel:"कथन शैली",mythology:"🎬 पौराणिक कथन",normal:"📖 सामान्य कथन",generate:"आवाज़ बनाएँ",ready:"स्क्रिप्ट लिखें और आवाज़ बनाएँ।",working:"आवाज़ बन रही है। कृपया प्रतीक्षा करें...",done:"आवाज़ तैयार है! सुनें या MP3 डाउनलोड करें।",empty:"पहले अपनी स्क्रिप्ट लिखें।",problem:"समस्या: ",failed:"आवाज़ नहीं बन सकी।",download:"⬇️ MP3 डाउनलोड करें",internet:"आवाज़ बनाने के लिए इंटरनेट आवश्यक है।"},\nen:{subtitle:"Bring your script to life",badge:"AI VOICE STUDIO",uiLanguage:"App language",scriptLabel:"Your script",scriptPlaceholder:"Type your script here...",limit:"Maximum 5000 characters",voiceLabel:"Choose voice",styleLabel:"Narration style",mythology:"🎬 Mythology narration",normal:"📖 Normal narration",generate:"Generate voice",ready:"Write a script to generate voice.",working:"Generating voice. Please wait...",done:"Voice ready! Play it or download the MP3.",empty:"Please type your script first.",problem:"Error: ",failed:"Voice generation failed.",download:"⬇️ Download MP3",internet:"Internet is required to generate voice."},\nta:{subtitle:"உங்கள் எழுத்துக்கு குரல் கொடுங்கள்",badge:"AI குரல் ஸ்டுடியோ",uiLanguage:"பயன்பாட்டு மொழி",scriptLabel:"உங்கள் உரை",scriptPlaceholder:"உங்கள் உரையை இங்கே எழுதுங்கள்...",limit:"அதிகபட்சம் 5000 எழுத்துகள்",voiceLabel:"குரலைத் தேர்ந்தெடுக்கவும்",styleLabel:"கதை சொல்லும் பாணி",mythology:"🎬 புராணக் கதை",normal:"📖 சாதாரண கதை",generate:"குரலை உருவாக்கு",ready:"உரையை எழுதி குரலை உருவாக்குங்கள்.",working:"குரல் உருவாகிறது. காத்திருக்கவும்...",done:"குரல் தயார்! கேளுங்கள் அல்லது MP3 பதிவிறக்கவும்.",empty:"முதலில் உரையை எழுதுங்கள்.",problem:"பிழை: ",failed:"குரலை உருவாக்க முடியவில்லை.",download:"⬇️ MP3 பதிவிறக்கவும்",internet:"குரலை உருவாக்க இணையம் தேவை."},\nkn:{subtitle:"ನಿಮ್ಮ ಬರಹಕ್ಕೆ ಧ್ವನಿ ನೀಡಿ",badge:"AI ಧ್ವನಿ ಸ್ಟುಡಿಯೋ",uiLanguage:"ಅಪ್ಲಿಕೇಶನ್ ಭಾಷೆ",scriptLabel:"ನಿಮ್ಮ ಬರಹ",scriptPlaceholder:"ನಿಮ್ಮ ಬರಹವನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ...",limit:"ಗರಿಷ್ಠ 5000 ಅಕ್ಷರಗಳು",voiceLabel:"ಧ್ವನಿ ಆಯ್ಕೆಮಾಡಿ",styleLabel:"ನಿರೂಪಣೆಯ ಶೈಲಿ",mythology:"🎬 ಪೌರಾಣಿಕ ನಿರೂಪಣೆ",normal:"📖 ಸಾಮಾನ್ಯ ನಿರೂಪಣೆ",generate:"ಧ್ವನಿ ರಚಿಸಿ",ready:"ಬರಹ ನಮೂದಿಸಿ ಮತ್ತು ಧ್ವನಿ ರಚಿಸಿ.",working:"ಧ್ವನಿ ರಚಿಸಲಾಗುತ್ತಿದೆ. ನಿರೀಕ್ಷಿಸಿ...",done:"ಧ್ವನಿ ಸಿದ್ಧವಾಗಿದೆ! ಕೇಳಿ ಅಥವಾ MP3 ಡೌನ್\u200cಲೋಡ್ ಮಾಡಿ.",empty:"ಮೊದಲು ಬರಹ ನಮೂದಿಸಿ.",problem:"ದೋಷ: ",failed:"ಧ್ವನಿ ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",download:"⬇️ MP3 ಡೌನ್\u200cಲೋಡ್ ಮಾಡಿ",internet:"ಧ್ವನಿ ರಚಿಸಲು ಇಂಟರ್ನೆಟ್ ಅಗತ್ಯವಿದೆ."},\nml:{subtitle:"നിങ്ങളുടെ എഴുത്തിന് ശബ്ദം നൽകൂ",badge:"AI വോയ്സ് സ്റ്റുഡിയോ",uiLanguage:"ആപ്പ് ഭാഷ",scriptLabel:"നിങ്ങളുടെ സ്ക്രിപ്റ്റ്",scriptPlaceholder:"നിങ്ങളുടെ എഴുത്ത് ഇവിടെ നൽകുക...",limit:"പരമാവധി 5000 അക്ഷരങ്ങൾ",voiceLabel:"ശബ്ദം തിരഞ്ഞെടുക്കുക",styleLabel:"ആഖ്യാന ശൈലി",mythology:"🎬 പുരാണ ആഖ്യാനം",normal:"📖 സാധാരണ ആഖ്യാനം",generate:"ശബ്ദം സൃഷ്ടിക്കുക",ready:"എഴുത്ത് നൽകി ശബ്ദം സൃഷ്ടിക്കുക.",working:"ശബ്ദം സൃഷ്ടിക്കുന്നു. കാത്തിരിക്കുക...",done:"ശബ്ദം തയ്യാറായി! കേൾക്കുക അല്ലെങ്കിൽ MP3 ഡൗൺലോഡ് ചെയ്യുക.",empty:"ആദ്യം എഴുത്ത് നൽകുക.",problem:"പിശക്: ",failed:"ശബ്ദം സൃഷ്ടിക്കാനായില്ല.",download:"⬇️ MP3 ഡൗൺലോഡ് ചെയ്യുക",internet:"ശബ്ദം സൃഷ്ടിക്കാൻ ഇന്റർനെറ്റ് ആവശ്യമാണ്."},\nbn:{subtitle:"আপনার লেখায় কণ্ঠ দিন",badge:"AI ভয়েস স্টুডিও",uiLanguage:"অ্যাপের ভাষা",scriptLabel:"আপনার স্ক্রিপ্ট",scriptPlaceholder:"এখানে আপনার লেখা লিখুন...",limit:"সর্বোচ্চ ৫০০০ অক্ষর",voiceLabel:"কণ্ঠ বেছে নিন",styleLabel:"বর্ণনার ধরন",mythology:"🎬 পৌরাণিক বর্ণনা",normal:"📖 সাধারণ বর্ণনা",generate:"কণ্ঠ তৈরি করুন",ready:"লেখা লিখে কণ্ঠ তৈরি করুন।",working:"কণ্ঠ তৈরি হচ্ছে। অপেক্ষা করুন...",done:"কণ্ঠ তৈরি হয়েছে! শুনুন বা MP3 ডাউনলোড করুন।",empty:"প্রথমে আপনার লেখা লিখুন।",problem:"সমস্যা: ",failed:"কণ্ঠ তৈরি করা যায়নি।",download:"⬇️ MP3 ডাউনলোড করুন",internet:"কণ্ঠ তৈরি করতে ইন্টারনেট প্রয়োজন।"},\ngu:{subtitle:"તમારા લખાણને અવાજ આપો",badge:"AI વૉઇસ સ્ટુડિયો",uiLanguage:"ઍપની ભાષા",scriptLabel:"તમારું લખાણ",scriptPlaceholder:"તમારું લખાણ અહીં લખો...",limit:"વધુમાં વધુ 5000 અક્ષરો",voiceLabel:"અવાજ પસંદ કરો",styleLabel:"વર્ણન શૈલી",mythology:"🎬 પૌરાણિક વર્ણન",normal:"📖 સામાન્ય વર્ણન",generate:"અવાજ બનાવો",ready:"લખાણ લખીને અવાજ બનાવો.",working:"અવાજ બની રહ્યો છે. રાહ જુઓ...",done:"અવાજ તૈયાર છે! સાંભળો અથવા MP3 ડાઉનલોડ કરો.",empty:"પહેલાં તમારું લખાણ લખો.",problem:"સમસ્યા: ",failed:"અવાજ બનાવી શકાયો નથી.",download:"⬇️ MP3 ડાઉનલોડ કરો",internet:"અવાજ બનાવવા માટે ઇન્ટરનેટ જરૂરી છે."},\nmr:{subtitle:"तुमच्या लिखाणाला आवाज द्या",badge:"AI व्हॉइस स्टुडिओ",uiLanguage:"अॅपची भाषा",scriptLabel:"तुमची स्क्रिप्ट",scriptPlaceholder:"तुमचे लिखाण येथे टाइप करा...",limit:"कमाल 5000 अक्षरे",voiceLabel:"आवाज निवडा",styleLabel:"निवेदन शैली",mythology:"🎬 पौराणिक निवेदन",normal:"📖 सामान्य निवेदन",generate:"आवाज तयार करा",ready:"लिखाण टाइप करून आवाज तयार करा.",working:"आवाज तयार होत आहे. कृपया थांबा...",done:"आवाज तयार आहे! ऐका किंवा MP3 डाउनलोड करा.",empty:"प्रथम तुमचे लिखाण टाइप करा.",problem:"समस्या: ",failed:"आवाज तयार झाला नाही.",download:"⬇️ MP3 डाउनलोड करा",internet:"आवाज तयार करण्यासाठी इंटरनेट आवश्यक आहे."},\nne:{subtitle:"आफ्नो लेखलाई आवाज दिनुहोस्",badge:"AI आवाज स्टुडियो",uiLanguage:"एपको भाषा",scriptLabel:"तपाईंको स्क्रिप्ट",scriptPlaceholder:"यहाँ आफ्नो लेख लेख्नुहोस्...",limit:"अधिकतम ५००० अक्षर",voiceLabel:"आवाज छान्नुहोस्",styleLabel:"वाचन शैली",mythology:"🎬 पौराणिक कथन",normal:"📖 सामान्य कथन",generate:"आवाज बनाउनुहोस्",ready:"लेख लेखेर आवाज बनाउनुहोस्।",working:"आवाज बनिरहेको छ। कृपया पर्खनुहोस्...",done:"आवाज तयार भयो! सुन्नुहोस् वा MP3 डाउनलोड गर्नुहोस्।",empty:"पहिले आफ्नो लेख लेख्नुहोस्।",problem:"समस्या: ",failed:"आवाज बनाउन सकिएन।",download:"⬇️ MP3 डाउनलोड गर्नुहोस्",internet:"आवाज बनाउन इन्टरनेट आवश्यक छ।"},\nur:{subtitle:"اپنی تحریر کو آواز دیں",badge:"AI وائس اسٹوڈیو",uiLanguage:"ایپ کی زبان",scriptLabel:"آپ کا متن",scriptPlaceholder:"اپنا متن یہاں لکھیں...",limit:"زیادہ سے زیادہ 5000 حروف",voiceLabel:"آواز منتخب کریں",styleLabel:"بیان کا انداز",mythology:"🎬 دیومالائی بیان",normal:"📖 عام بیان",generate:"آواز بنائیں",ready:"متن لکھ کر آواز بنائیں۔",working:"آواز بن رہی ہے۔ انتظار کریں...",done:"آواز تیار ہے! سنیں یا MP3 ڈاؤن لوڈ کریں۔",empty:"پہلے اپنا متن لکھیں۔",problem:"مسئلہ: ",failed:"آواز نہیں بن سکی۔",download:"⬇️ MP3 ڈاؤن لوڈ کریں",internet:"آواز بنانے کے لیے انٹرنیٹ ضروری ہے۔"}\n};\n\nfunction setLanguage(lang){\n const d=translations[lang]||translations.te;\n document.documentElement.lang=lang;\n document.documentElement.dir=lang==="ur"?"rtl":"ltr";\n document.querySelectorAll("[data-i]").forEach(el=>{\n   const key=el.dataset.i;\n   if(d[key]) el.textContent=d[key];\n });\n document.querySelectorAll("[data-ph]").forEach(el=>{\n   const key=el.dataset.ph;\n   if(d[key]) el.placeholder=d[key];\n });\n}\ndocument.getElementById("uiLang").addEventListener("change",e=>setLanguage(e.target.value));\nsetLanguage("te");\n\nasync function generateVoice(){\n const script=document.getElementById("script").value.trim();\n const voice=document.getElementById("voice").value;\n const narration=document.getElementById("narration").value;\n const status=document.getElementById("status");\n const button=document.getElementById("generate");\n const player=document.getElementById("player");\n const download=document.getElementById("download");\n const d=translations[document.getElementById("uiLang").value]||translations.te;\n if(!script){status.textContent=d.empty;return;}\n button.disabled=true;\n status.textContent=d.working;\n player.hidden=true;\n download.hidden=true;\n try{\n   const response=await fetch("/generate",{\n     method:"POST",\n     headers:{"Content-Type":"application/json"},\n     body:JSON.stringify({script:script,voice:voice,narration:narration})\n   });\n   const data=await response.json();\n   if(!response.ok) throw new Error(data.error||d.failed);\n   player.src=data.url;\n   player.hidden=false;\n   download.href=data.url;\n   download.hidden=false;\n   status.textContent=d.done;\n }catch(error){\n   status.textContent=d.problem+error.message;\n }finally{\n   button.disabled=false;\n }\n}\n</script>\n</body>\n</html>\n'

@app.route("/")
def home():
    return render_template_string(HTML, voices=VOICES)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    text = str(data.get("script", "")).strip()
    voice = data.get("voice", "te-IN-ShrutiNeural")

    narration = data.get("narration", "normal")
    if narration not in ("mythology", "normal"):
        return jsonify(error="సరైన కథనం శైలిని ఎంచుకోండి."), 400
    if not text:
        return jsonify(error="ముందుగా స్క్రిప్ట్ ఇవ్వండి."), 400
    if len(text) > 5000:
        return jsonify(error="స్క్రిప్ట్ 5000 అక్షరాల లోపు ఉండాలి."), 400
    if voice not in VOICES:
        return jsonify(error="సరైన వాయిస్‌ను ఎంచుకోండి."), 400

    filename = str(uuid.uuid4()) + ".mp3"
    path = os.path.join(OUT_DIR, filename)

    try:
        async def create_audio():
            rate = "-15%" if narration == "mythology" else "+0%"
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            await communicate.save(path)

        asyncio.run(create_audio())
        return jsonify(url="/audio/" + filename)
    except Exception as exc:
        if os.path.exists(path):
            os.remove(path)
        app.logger.exception("Voice generation failed")
        return jsonify(error="వాయిస్ తయారీలో సమస్య వచ్చింది. ఇంటర్నెట్‌ను తనిఖీ చేసి మళ్లీ ప్రయత్నించండి."), 502

@app.route("/audio/<path:filename>")
def audio_file(filename):
    if not filename.endswith(".mp3"):
        return "Not found", 404
    return send_from_directory(OUT_DIR, filename, as_attachment=False)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)


