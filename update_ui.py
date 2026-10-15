import re

path = "app.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

html = r'''
<!DOCTYPE html>
<html lang="te">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b1020">
<title>ScriptToVoice</title>
<style>
*{box-sizing:border-box}
body{margin:0;min-height:100vh;padding:22px 15px;background:radial-gradient(ellipse at top,#202b50 0%,#0b1020 55%,#080b13 100%);color:#f5f7ff;font-family:system-ui,Arial,sans-serif}
.container{max-width:520px;margin:0 auto}
.top{display:flex;align-items:center;gap:13px;margin:10px 0 24px}
.logo{width:55px;height:55px;border-radius:18px;background:linear-gradient(135deg,#7c5cff,#20c9e8);display:grid;place-items:center;font-size:27px;box-shadow:0 8px 28px #6655ff45}
h1{font-size:25px;margin:0;letter-spacing:-.6px}
.subtitle{color:#aebbd5;margin:5px 0 0;font-size:14px}
.card{background:#121a2bd9;border:1px solid #34415e;border-radius:24px;padding:21px;box-shadow:0 18px 55px #0004}
.badge{display:inline-flex;align-items:center;gap:7px;padding:7px 11px;border:1px solid #334765;border-radius:30px;color:#a8e9ff;font-size:12px;margin-bottom:17px}
label{display:block;font-size:14px;font-weight:650;color:#dbe5fa;margin:17px 0 8px}
textarea,select{display:block;width:100%;border:1px solid #34435f;border-radius:13px;background:#0c1323;color:#f5f7ff;padding:14px;font:inherit;outline:none}
textarea{min-height:155px;resize:vertical;line-height:1.65}
textarea:focus,select:focus{border-color:#67cfff;box-shadow:0 0 0 3px #36baff18}
select{min-height:49px}
button{width:100%;border:0;border-radius:14px;padding:15px;margin-top:21px;background:linear-gradient(100deg,#7658ff,#238fe8);color:white;font:inherit;font-weight:750;font-size:16px;box-shadow:0 8px 24px #5366ff30}
button:disabled{opacity:.6}
.note{color:#b6c2d8;font-size:13px;line-height:1.6;overflow-wrap:anywhere}
#status{padding:12px;background:#0c1323;border:1px solid #273650;border-radius:12px}
audio{width:100%;margin-top:12px}
a{color:#79dfff;font-weight:700}
.footer{text-align:center;color:#8190ac;font-size:12px;margin:18px 0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:380px){.card{padding:16px}.grid{grid-template-columns:1fr}h1{font-size:22px}}
</style>
</head>
<body>
<div class="container">
  <div class="top">
    <div class="logo">🎙️</div>
    <div><h1>ScriptToVoice</h1><p class="subtitle" data-i="subtitle">మీ స్క్రిప్ట్‌కు ప్రాణం పోయండి</p></div>
  </div>

  <div class="card">
    <div class="badge">✦ <span data-i="badge">AI వాయిస్ స్టూడియో</span></div>

    <label for="uiLang" data-i="uiLanguage">యాప్ భాష</label>
    <select id="uiLang">
      <option value="te">తెలుగు</option>
      <option value="hi">हिन्दी</option>
      <option value="en">English</option>
      <option value="ta">தமிழ்</option>
      <option value="kn">ಕನ್ನಡ</option>
      <option value="ml">മലയാളം</option>
      <option value="bn">বাংলা</option>
      <option value="gu">ગુજરાતી</option>
      <option value="mr">मराठी</option>
      <option value="ne">नेपाली</option>
      <option value="ur">اردو</option>
    </select>

    <label for="script" data-i="scriptLabel">మీ స్క్రిప్ట్</label>
    <textarea id="script" maxlength="5000" data-ph="scriptPlaceholder" placeholder="మీ కథనం ఇక్కడ టైప్ చేయండి..."></textarea>
    <p class="note" data-i="limit">గరిష్ఠంగా 5000 అక్షరాలు</p>

    <div class="grid">
      <div>
        <label for="voice" data-i="voiceLabel">వాయిస్ ఎంచుకోండి</label>
        <select id="voice">
          {% for id, label in voices.items() %}
          <option value="{{ id }}">{{ label }}</option>
          {% endfor %}
        </select>
      </div>
      <div>
        <label for="narration" data-i="styleLabel">కథనం శైలి</label>
        <select id="narration">
          <option value="mythology" data-i="mythology">🎬 పురాణ కథనం</option>
          <option value="normal" data-i="normal">📖 సాధారణ కథనం</option>
        </select>
      </div>
    </div>

    <button id="generate" onclick="generateVoice()">🎙️ <span data-i="generate">వాయిస్ తయారు చేయండి</span></button>
    <p id="status" class="note" data-i="ready">స్క్రిప్ట్ రాసి వాయిస్ తయారు చేయండి.</p>
    <audio id="player" controls hidden></audio>
    <p><a id="download" hidden download="ScriptToVoice.mp3" data-i="download">⬇️ MP3 డౌన్‌లోడ్ చేసుకోండి</a></p>
    <p class="note" data-i="internet">వాయిస్ తయారీకి ఇంటర్నెట్ అవసరం.</p>
  </div>
  <div class="footer">ScriptToVoice · Voice your story</div>
</div>

<script>
const translations = {
te:{subtitle:"మీ స్క్రిప్ట్‌కు ప్రాణం పోయండి",badge:"AI వాయిస్ స్టూడియో",uiLanguage:"యాప్ భాష",scriptLabel:"మీ స్క్రిప్ట్",scriptPlaceholder:"మీ కథనం ఇక్కడ టైప్ చేయండి...",limit:"గరిష్ఠంగా 5000 అక్షరాలు",voiceLabel:"వాయిస్ ఎంచుకోండి",styleLabel:"కథనం శైలి",mythology:"🎬 పురాణ కథనం",normal:"📖 సాధారణ కథనం",generate:"వాయిస్ తయారు చేయండి",ready:"స్క్రిప్ట్ రాసి వాయిస్ తయారు చేయండి.",working:"వాయిస్ తయారవుతోంది. దయచేసి వేచి ఉండండి...",done:"వాయిస్ తయారైంది! వినండి లేదా MP3 డౌన్‌లోడ్ చేసుకోండి.",empty:"ముందుగా మీ స్క్రిప్ట్ టైప్ చేయండి.",problem:"సమస్య: ",failed:"వాయిస్ తయారు కాలేదు.",download:"⬇️ MP3 డౌన్‌లోడ్ చేసుకోండి",internet:"వాయిస్ తయారీకి ఇంటర్నెట్ అవసరం."},
hi:{subtitle:"अपनी स्क्रिप्ट को आवाज़ दें",badge:"AI वॉइस स्टूडियो",uiLanguage:"ऐप की भाषा",scriptLabel:"आपकी स्क्रिप्ट",scriptPlaceholder:"अपना टेक्स्ट यहाँ लिखें...",limit:"अधिकतम 5000 अक्षर",voiceLabel:"आवाज़ चुनें",styleLabel:"कथन शैली",mythology:"🎬 पौराणिक कथन",normal:"📖 सामान्य कथन",generate:"आवाज़ बनाएँ",ready:"स्क्रिप्ट लिखें और आवाज़ बनाएँ।",working:"आवाज़ बन रही है। कृपया प्रतीक्षा करें...",done:"आवाज़ तैयार है! सुनें या MP3 डाउनलोड करें।",empty:"पहले अपनी स्क्रिप्ट लिखें।",problem:"समस्या: ",failed:"आवाज़ नहीं बन सकी।",download:"⬇️ MP3 डाउनलोड करें",internet:"आवाज़ बनाने के लिए इंटरनेट आवश्यक है।"},
en:{subtitle:"Bring your script to life",badge:"AI VOICE STUDIO",uiLanguage:"App language",scriptLabel:"Your script",scriptPlaceholder:"Type your script here...",limit:"Maximum 5000 characters",voiceLabel:"Choose voice",styleLabel:"Narration style",mythology:"🎬 Mythology narration",normal:"📖 Normal narration",generate:"Generate voice",ready:"Write a script to generate voice.",working:"Generating voice. Please wait...",done:"Voice ready! Play it or download the MP3.",empty:"Please type your script first.",problem:"Error: ",failed:"Voice generation failed.",download:"⬇️ Download MP3",internet:"Internet is required to generate voice."},
ta:{subtitle:"உங்கள் எழுத்துக்கு குரல் கொடுங்கள்",badge:"AI குரல் ஸ்டுடியோ",uiLanguage:"பயன்பாட்டு மொழி",scriptLabel:"உங்கள் உரை",scriptPlaceholder:"உங்கள் உரையை இங்கே எழுதுங்கள்...",limit:"அதிகபட்சம் 5000 எழுத்துகள்",voiceLabel:"குரலைத் தேர்ந்தெடுக்கவும்",styleLabel:"கதை சொல்லும் பாணி",mythology:"🎬 புராணக் கதை",normal:"📖 சாதாரண கதை",generate:"குரலை உருவாக்கு",ready:"உரையை எழுதி குரலை உருவாக்குங்கள்.",working:"குரல் உருவாகிறது. காத்திருக்கவும்...",done:"குரல் தயார்! கேளுங்கள் அல்லது MP3 பதிவிறக்கவும்.",empty:"முதலில் உரையை எழுதுங்கள்.",problem:"பிழை: ",failed:"குரலை உருவாக்க முடியவில்லை.",download:"⬇️ MP3 பதிவிறக்கவும்",internet:"குரலை உருவாக்க இணையம் தேவை."},
kn:{subtitle:"ನಿಮ್ಮ ಬರಹಕ್ಕೆ ಧ್ವನಿ ನೀಡಿ",badge:"AI ಧ್ವನಿ ಸ್ಟುಡಿಯೋ",uiLanguage:"ಅಪ್ಲಿಕೇಶನ್ ಭಾಷೆ",scriptLabel:"ನಿಮ್ಮ ಬರಹ",scriptPlaceholder:"ನಿಮ್ಮ ಬರಹವನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ...",limit:"ಗರಿಷ್ಠ 5000 ಅಕ್ಷರಗಳು",voiceLabel:"ಧ್ವನಿ ಆಯ್ಕೆಮಾಡಿ",styleLabel:"ನಿರೂಪಣೆಯ ಶೈಲಿ",mythology:"🎬 ಪೌರಾಣಿಕ ನಿರೂಪಣೆ",normal:"📖 ಸಾಮಾನ್ಯ ನಿರೂಪಣೆ",generate:"ಧ್ವನಿ ರಚಿಸಿ",ready:"ಬರಹ ನಮೂದಿಸಿ ಮತ್ತು ಧ್ವನಿ ರಚಿಸಿ.",working:"ಧ್ವನಿ ರಚಿಸಲಾಗುತ್ತಿದೆ. ನಿರೀಕ್ಷಿಸಿ...",done:"ಧ್ವನಿ ಸಿದ್ಧವಾಗಿದೆ! ಕೇಳಿ ಅಥವಾ MP3 ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",empty:"ಮೊದಲು ಬರಹ ನಮೂದಿಸಿ.",problem:"ದೋಷ: ",failed:"ಧ್ವನಿ ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",download:"⬇️ MP3 ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",internet:"ಧ್ವನಿ ರಚಿಸಲು ಇಂಟರ್ನೆಟ್ ಅಗತ್ಯವಿದೆ."},
ml:{subtitle:"നിങ്ങളുടെ എഴുത്തിന് ശബ്ദം നൽകൂ",badge:"AI വോയ്സ് സ്റ്റുഡിയോ",uiLanguage:"ആപ്പ് ഭാഷ",scriptLabel:"നിങ്ങളുടെ സ്ക്രിപ്റ്റ്",scriptPlaceholder:"നിങ്ങളുടെ എഴുത്ത് ഇവിടെ നൽകുക...",limit:"പരമാവധി 5000 അക്ഷരങ്ങൾ",voiceLabel:"ശബ്ദം തിരഞ്ഞെടുക്കുക",styleLabel:"ആഖ്യാന ശൈലി",mythology:"🎬 പുരാണ ആഖ്യാനം",normal:"📖 സാധാരണ ആഖ്യാനം",generate:"ശബ്ദം സൃഷ്ടിക്കുക",ready:"എഴുത്ത് നൽകി ശബ്ദം സൃഷ്ടിക്കുക.",working:"ശബ്ദം സൃഷ്ടിക്കുന്നു. കാത്തിരിക്കുക...",done:"ശബ്ദം തയ്യാറായി! കേൾക്കുക അല്ലെങ്കിൽ MP3 ഡൗൺലോഡ് ചെയ്യുക.",empty:"ആദ്യം എഴുത്ത് നൽകുക.",problem:"പിശക്: ",failed:"ശബ്ദം സൃഷ്ടിക്കാനായില്ല.",download:"⬇️ MP3 ഡൗൺലോഡ് ചെയ്യുക",internet:"ശബ്ദം സൃഷ്ടിക്കാൻ ഇന്റർനെറ്റ് ആവശ്യമാണ്."},
bn:{subtitle:"আপনার লেখায় কণ্ঠ দিন",badge:"AI ভয়েস স্টুডিও",uiLanguage:"অ্যাপের ভাষা",scriptLabel:"আপনার স্ক্রিপ্ট",scriptPlaceholder:"এখানে আপনার লেখা লিখুন...",limit:"সর্বোচ্চ ৫০০০ অক্ষর",voiceLabel:"কণ্ঠ বেছে নিন",styleLabel:"বর্ণনার ধরন",mythology:"🎬 পৌরাণিক বর্ণনা",normal:"📖 সাধারণ বর্ণনা",generate:"কণ্ঠ তৈরি করুন",ready:"লেখা লিখে কণ্ঠ তৈরি করুন।",working:"কণ্ঠ তৈরি হচ্ছে। অপেক্ষা করুন...",done:"কণ্ঠ তৈরি হয়েছে! শুনুন বা MP3 ডাউনলোড করুন।",empty:"প্রথমে আপনার লেখা লিখুন।",problem:"সমস্যা: ",failed:"কণ্ঠ তৈরি করা যায়নি।",download:"⬇️ MP3 ডাউনলোড করুন",internet:"কণ্ঠ তৈরি করতে ইন্টারনেট প্রয়োজন।"},
gu:{subtitle:"તમારા લખાણને અવાજ આપો",badge:"AI વૉઇસ સ્ટુડિયો",uiLanguage:"ઍપની ભાષા",scriptLabel:"તમારું લખાણ",scriptPlaceholder:"તમારું લખાણ અહીં લખો...",limit:"વધુમાં વધુ 5000 અક્ષરો",voiceLabel:"અવાજ પસંદ કરો",styleLabel:"વર્ણન શૈલી",mythology:"🎬 પૌરાણિક વર્ણન",normal:"📖 સામાન્ય વર્ણન",generate:"અવાજ બનાવો",ready:"લખાણ લખીને અવાજ બનાવો.",working:"અવાજ બની રહ્યો છે. રાહ જુઓ...",done:"અવાજ તૈયાર છે! સાંભળો અથવા MP3 ડાઉનલોડ કરો.",empty:"પહેલાં તમારું લખાણ લખો.",problem:"સમસ્યા: ",failed:"અવાજ બનાવી શકાયો નથી.",download:"⬇️ MP3 ડાઉનલોડ કરો",internet:"અવાજ બનાવવા માટે ઇન્ટરનેટ જરૂરી છે."},
mr:{subtitle:"तुमच्या लिखाणाला आवाज द्या",badge:"AI व्हॉइस स्टुडिओ",uiLanguage:"अॅपची भाषा",scriptLabel:"तुमची स्क्रिप्ट",scriptPlaceholder:"तुमचे लिखाण येथे टाइप करा...",limit:"कमाल 5000 अक्षरे",voiceLabel:"आवाज निवडा",styleLabel:"निवेदन शैली",mythology:"🎬 पौराणिक निवेदन",normal:"📖 सामान्य निवेदन",generate:"आवाज तयार करा",ready:"लिखाण टाइप करून आवाज तयार करा.",working:"आवाज तयार होत आहे. कृपया थांबा...",done:"आवाज तयार आहे! ऐका किंवा MP3 डाउनलोड करा.",empty:"प्रथम तुमचे लिखाण टाइप करा.",problem:"समस्या: ",failed:"आवाज तयार झाला नाही.",download:"⬇️ MP3 डाउनलोड करा",internet:"आवाज तयार करण्यासाठी इंटरनेट आवश्यक आहे."},
ne:{subtitle:"आफ्नो लेखलाई आवाज दिनुहोस्",badge:"AI आवाज स्टुडियो",uiLanguage:"एपको भाषा",scriptLabel:"तपाईंको स्क्रिप्ट",scriptPlaceholder:"यहाँ आफ्नो लेख लेख्नुहोस्...",limit:"अधिकतम ५००० अक्षर",voiceLabel:"आवाज छान्नुहोस्",styleLabel:"वाचन शैली",mythology:"🎬 पौराणिक कथन",normal:"📖 सामान्य कथन",generate:"आवाज बनाउनुहोस्",ready:"लेख लेखेर आवाज बनाउनुहोस्।",working:"आवाज बनिरहेको छ। कृपया पर्खनुहोस्...",done:"आवाज तयार भयो! सुन्नुहोस् वा MP3 डाउनलोड गर्नुहोस्।",empty:"पहिले आफ्नो लेख लेख्नुहोस्।",problem:"समस्या: ",failed:"आवाज बनाउन सकिएन।",download:"⬇️ MP3 डाउनलोड गर्नुहोस्",internet:"आवाज बनाउन इन्टरनेट आवश्यक छ।"},
ur:{subtitle:"اپنی تحریر کو آواز دیں",badge:"AI وائس اسٹوڈیو",uiLanguage:"ایپ کی زبان",scriptLabel:"آپ کا متن",scriptPlaceholder:"اپنا متن یہاں لکھیں...",limit:"زیادہ سے زیادہ 5000 حروف",voiceLabel:"آواز منتخب کریں",styleLabel:"بیان کا انداز",mythology:"🎬 دیومالائی بیان",normal:"📖 عام بیان",generate:"آواز بنائیں",ready:"متن لکھ کر آواز بنائیں۔",working:"آواز بن رہی ہے۔ انتظار کریں...",done:"آواز تیار ہے! سنیں یا MP3 ڈاؤن لوڈ کریں۔",empty:"پہلے اپنا متن لکھیں۔",problem:"مسئلہ: ",failed:"آواز نہیں بن سکی۔",download:"⬇️ MP3 ڈاؤن لوڈ کریں",internet:"آواز بنانے کے لیے انٹرنیٹ ضروری ہے۔"}
};

function setLanguage(lang){
 const d=translations[lang]||translations.te;
 document.documentElement.lang=lang;
 document.documentElement.dir=lang==="ur"?"rtl":"ltr";
 document.querySelectorAll("[data-i]").forEach(el=>{
   const key=el.dataset.i;
   if(d[key]) el.textContent=d[key];
 });
 document.querySelectorAll("[data-ph]").forEach(el=>{
   const key=el.dataset.ph;
   if(d[key]) el.placeholder=d[key];
 });
}
document.getElementById("uiLang").addEventListener("change",e=>setLanguage(e.target.value));
setLanguage("te");

async function generateVoice(){
 const script=document.getElementById("script").value.trim();
 const voice=document.getElementById("voice").value;
 const narration=document.getElementById("narration").value;
 const status=document.getElementById("status");
 const button=document.getElementById("generate");
 const player=document.getElementById("player");
 const download=document.getElementById("download");
 const d=translations[document.getElementById("uiLang").value]||translations.te;
 if(!script){status.textContent=d.empty;return;}
 button.disabled=true;
 status.textContent=d.working;
 player.hidden=true;
 download.hidden=true;
 try{
   const response=await fetch("/generate",{
     method:"POST",
     headers:{"Content-Type":"application/json"},
     body:JSON.stringify({script:script,voice:voice,narration:narration})
   });
   const data=await response.json();
   if(!response.ok) throw new Error(data.error||d.failed);
   player.src=data.url;
   player.hidden=false;
   download.href=data.url;
   download.hidden=false;
   status.textContent=d.done;
 }catch(error){
   status.textContent=d.problem+error.message;
 }finally{
   button.disabled=false;
 }
}
</script>
</body>
</html>
'''

pattern = r'HTML = """.*?"""'
updated, count = re.subn(pattern, lambda _: "HTML = " + repr(html), code, count=1, flags=re.S)
if count != 1:
    raise SystemExit("HTML block not found; app.py was not changed.")
with open(path, "w", encoding="utf-8") as f:
    f.write(updated)
print("Premium UI and 11-language selector added.")
