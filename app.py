from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Rule-based response engine
rules = [
    # Greetings
    (r'\b(hi|hello|hey|good morning|good evening|good afternoon)\b', 
     "Hello! 👋 I'm MediBot, your personal medical assistant. I can help with skincare, wounds, cuts, and general symptoms. What's bothering you?"),
    
    (r'\b(how are you|how r you)\b',
     "I'm functioning perfectly! 😊 More importantly, how are YOU feeling? Tell me your symptoms."),

    (r'\b(bye|goodbye|exit|quit|see you)\b',
     "Take care and stay healthy! 💊 Remember: I'm not a substitute for a real doctor. Goodbye! 👋"),

    (r'\b(thank you|thanks|thx|thank u)\b',
     "You're welcome! 😊 Stay healthy. Let me know if you need anything else."),

    # --- SKINCARE ---
    (r'\b(pimple|acne|breakout|zit|blemish)\b',
     "🧴 **Acne/Pimples:**\n- Wash face twice daily with a gentle cleanser.\n- Use salicylic acid or benzoyl peroxide products.\n- Don't pop pimples — it causes scarring.\n- Stay hydrated and avoid oily foods.\n- If severe, consult a dermatologist for prescription treatment."),

    (r'\b(dry skin|dryness|flaky|peeling skin)\b',
     "💧 **Dry Skin:**\n- Moisturize immediately after bathing.\n- Use fragrance-free, thick creams (like CeraVe or Vaseline).\n- Drink plenty of water.\n- Avoid hot showers — use lukewarm water.\n- Use a humidifier in dry environments."),

    (r'\b(oily skin|oily face|excess oil|shiny face)\b',
     "✨ **Oily Skin:**\n- Use a gentle foaming or gel-based cleanser.\n- Apply oil-free, non-comedogenic moisturizer.\n- Use blotting paper during the day.\n- Try niacinamide serum to control oil.\n- Don't skip moisturizer — dry skin overproduces oil."),

    (r'\b(sunburn|sun burn|tanning|burnt skin)\b',
     "☀️ **Sunburn:**\n- Apply cool (not ice cold) compress to the area.\n- Use aloe vera gel for soothing.\n- Take ibuprofen for pain/inflammation.\n- Stay out of the sun until healed.\n- Keep skin moisturized. If blisters form, see a doctor."),

    (r'\b(dark spot|hyperpigmentation|dark patch|uneven skin tone)\b',
     "🌿 **Dark Spots/Hyperpigmentation:**\n- Use sunscreen daily (SPF 30+) to prevent worsening.\n- Try Vitamin C serum or niacinamide.\n- Kojic acid or retinol can help over time.\n- Be patient — results take weeks to months.\n- Consult a dermatologist for persistent cases."),

    (r'\b(rash|skin rash|itchy skin|hives|allergic reaction|allergy)\b',
     "⚠️ **Skin Rash/Allergy:**\n- Avoid scratching — it worsens irritation.\n- Apply 1% hydrocortisone cream for mild rashes.\n- Take an antihistamine (like cetirizine) for itching.\n- Identify and avoid the trigger (food, soap, fabric).\n- If rash spreads rapidly or you have breathing difficulty, seek emergency care immediately."),

    (r'\b(eczema|dermatitis)\b',
     "🧬 **Eczema/Dermatitis:**\n- Keep skin moisturized with thick creams.\n- Avoid harsh soaps and hot water.\n- Use fragrance-free products.\n- A doctor may prescribe topical steroids.\n- Identify triggers (stress, certain foods, fabrics)."),

    # --- WOUNDS & CUTS ---
    (r'\b(cut|cuts|small cut|bleeding|minor wound)\b',
     "🩹 **Minor Cut/Wound:**\n- Rinse the cut under clean running water for 5 minutes.\n- Apply gentle pressure with a clean cloth to stop bleeding.\n- Apply antiseptic (Dettol, Savlon, or povidone-iodine).\n- Cover with a bandage.\n- Watch for signs of infection: redness, swelling, pus.\n- Get a tetanus shot if the wound was caused by a dirty object."),

    (r'\b(deep cut|deep wound|won\'t stop bleeding|heavy bleeding)\b',
     "🚨 **Deep Cut / Heavy Bleeding:**\n- Apply firm pressure with a clean cloth — do NOT remove it.\n- Elevate the injured area above heart level.\n- Do NOT attempt to clean a deep wound yourself.\n- Go to an emergency room or call emergency services immediately.\n- This may require stitches."),

    (r'\b(burn|burned|scald|hot water burn|fire burn)\b',
     "🔥 **Burns:**\n- Run cool (not cold) water over the burn for 10–20 minutes.\n- Do NOT use ice, butter, or toothpaste.\n- Cover loosely with a clean, non-fluffy material.\n- Take paracetamol for pain.\n- For large/deep burns or burns on face/hands — go to emergency care immediately."),

    (r'\b(bruise|bruising|swollen|bump)\b',
     "🟣 **Bruise/Swelling:**\n- Apply an ice pack (wrapped in cloth) for 15–20 minutes.\n- Elevate the area if possible.\n- Rest the injured area.\n- Bruises typically heal in 2 weeks.\n- If swelling is severe or painful, get an X-ray to rule out fracture."),

    (r'\b(infection|infected|pus|red around wound|wound smells)\b',
     "⚠️ **Wound Infection:**\n- Keep the area clean and dry.\n- Apply antibiotic ointment (like Neosporin).\n- Change dressing twice daily.\n- If you see spreading redness, pus, fever, or red streaks — see a doctor immediately.\n- You may need oral antibiotics."),

    # --- GENERAL SYMPTOMS ---
    (r'\b(fever|high temperature|temperature|hot body)\b',
     "🌡️ **Fever:**\n- Rest and stay hydrated — drink water, ORS, or clear broth.\n- Take paracetamol to reduce temperature.\n- Use a cool damp cloth on forehead.\n- Wear light clothing.\n- See a doctor if fever is above 103°F (39.4°C), lasts more than 3 days, or is in a child under 2."),

    (r'\b(cold|runny nose|sneezing|congestion|stuffy nose|sore throat)\b',
     "🤧 **Common Cold:**\n- Rest as much as possible.\n- Stay hydrated with warm fluids (ginger tea, soup).\n- Use saline nasal spray for congestion.\n- Gargle warm salt water for sore throat.\n- Honey + lemon in warm water can help.\n- Antibiotics don't help — colds are viral."),

    (r'\b(cough|coughing|dry cough|wet cough|chest cough)\b',
     "😮‍💨 **Cough:**\n- Stay hydrated — warm fluids help.\n- Honey is effective for soothing cough (don't give to infants).\n- Use steam inhalation for chest congestion.\n- For dry cough: try cough lozenges.\n- See a doctor if cough lasts 3+ weeks, has blood, or is accompanied by chest pain."),

    (r'\b(headache|head pain|migraine|head hurts)\b',
     "🤕 **Headache/Migraine:**\n- Rest in a quiet, dark room.\n- Stay hydrated — dehydration is a common cause.\n- Apply cold or warm compress to head/neck.\n- Take paracetamol or ibuprofen.\n- For migraines: avoid triggers (bright lights, strong smells).\n- Seek help if headache is sudden/severe (thunderclap) or with fever/stiff neck."),

    (r'\b(stomach ache|stomach pain|stomach cramp|belly pain|abdominal pain)\b',
     "🤢 **Stomach Ache:**\n- Rest and avoid solid foods temporarily.\n- Sip clear fluids slowly.\n- A heating pad on the abdomen can help cramps.\n- Avoid spicy, fatty foods.\n- If pain is severe, sharp, or with fever/vomiting — see a doctor immediately."),

    (r'\b(nausea|vomiting|feeling sick|throwing up)\b',
     "🤮 **Nausea/Vomiting:**\n- Sip small amounts of water or ORS frequently.\n- Eat bland foods (crackers, toast, banana).\n- Avoid dairy, spicy, or heavy foods.\n- Ginger tea can reduce nausea.\n- Seek help if vomiting is persistent (24+ hours), contains blood, or with severe stomach pain."),

    (r'\b(dizziness|dizzy|lightheaded|vertigo)\b',
     "😵 **Dizziness:**\n- Sit or lie down immediately to avoid falling.\n- Drink water — dehydration is a common cause.\n- Avoid sudden position changes (rise slowly).\n- Rest until it passes.\n- Seek care if dizziness is severe, recurring, or with chest pain/vision changes."),

    (r'\b(eye pain|red eye|pink eye|conjunctivitis|itchy eye)\b',
     "👁️ **Eye Issues:**\n- Don't rub your eyes.\n- Rinse with clean water if irritant exposure occurred.\n- Use lubricating eye drops for dryness.\n- For pink eye: warm compress, avoid sharing towels.\n- See a doctor if vision changes, severe pain, or discharge with swelling."),

    (r'\b(sprain|twisted ankle|sprained|joint pain)\b',
     "🦶 **Sprain:**\n- Follow R.I.C.E: Rest, Ice, Compression, Elevation.\n- Apply ice pack for 20 min every 2–3 hours.\n- Use a compression bandage.\n- Avoid putting weight on it.\n- If you can't bear any weight or pain is severe, get an X-ray."),

    # Fallback
]

def get_response(user_input):
    user_input = user_input.lower().strip()
    for pattern, response in rules:
        if re.search(pattern, user_input):
            return response
    return ("🤔 I'm not sure about that specific concern. Could you describe your symptoms in more detail?\n\n"
            "I can help with: **skincare** (acne, dryness, rashes), **wounds** (cuts, burns, bruises), "
            "and **symptoms** (fever, cold, headache, nausea, etc.)\n\n"
            "⚠️ *Remember: I'm a rule-based assistant, not a real doctor. Always consult a healthcare professional for serious concerns.*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    response = get_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
