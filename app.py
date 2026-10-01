from flask import Flask, request
import requests, os
app = Flask(__name__)
TOKEN_META = os.environ.get("META_TOKEN", "")
PHONE_ID = os.environ.get("PHONE_ID", "")
VERIFY = os.environ.get("VERIFY_TOKEN", "kelimu123")
def reponse_kelimu(text):
    text = text.lower()
    if "hp" in text or "ryzen" in text or "360" in text:
        return "HP Ryzen 7 Pro à 360$ - 1 pièce seulement! Très rapide, pro. Batterie OK, garantie 1 mois. Il ne reste que 1! Tu veux que je te le réserve? Envoie nom + adresse."
    if "dell" in text or "7420" in text or "320" in text:
        return "Dell Latitude 7420 i5 11e génération à 320$ - 1 pièce seulement! Tactile, léger, excellent. Il ne reste que 1! Tu veux que je te le réserve? Envoie nom + adresse."
    if "lenovo" in text or "t470" in text or "i7" in text:
        return "Lenovo T470 i7 6e gen 500GB - 2 pièces dispo. Solide, clavier lumineux, parfait pour bureau. Tu veux que j'en réserve 1? Envoie nom + adresse."
    if "prix" in text or "combien" in text or "liste" in text:
        return "Stock actuel:\n- HP Ryzen 7 Pro: 360$ (1 pc)\n- Dell 7420 i5 11e: 320$ (1 pc)\n- Lenovo T470 i7 500GB: 2 pcs\nLivraison 5000fc, Gombe gratuit. Lequel tu veux?"
    if "commande" in text or "acheter" in text or "reserve" in text or "je veux" in text:
        return "Parfait! Envoie: 1) Ton nom 2) Adresse exacte 3) Modèle choisi. Je transmets au patron direct."
    return "Salut! Je suis KELIMU shop ordi. On a: HP Ryzen 7 Pro 360$ (1pc), Dell 7420 320$ (1pc), Lenovo T470 2pcs. Quel modèle t'intéresse?"
@app.route('/')
def home():
    return "KELIMU ORDI SHOP EN LIGNE"
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY:
        return request.args.get("hub.challenge")
    return "error", 403
@app.route('/webhook', methods=['POST'])
def receive():
    data = request.get_json()
    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        num = msg['from']
        txt = msg['text']['body']
        rep = reponse_kelimu(txt)
        requests.post(f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages",
            headers={"Authorization": f"Bearer {TOKEN_META}"},
            json={"messaging_product": "whatsapp", "to": num, "type": "text", "text": {"body": rep}})
    except: pass
    return "ok", 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
