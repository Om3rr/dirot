from flask import Flask, request, jsonify
from models import Dira
from helpers import SheetsAPI, GmailAPI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
sheets_api = SheetsAPI()
gmail_api = GmailAPI()
AVAILABLE_IDS = sheets_api.get_all_ids()

@app.route('/dira', methods=["POST"])
def create_dira():
    content = request.get_json(silent=True)
    d = Dira(**content.get("dira"))
    if d.id in AVAILABLE_IDS:
        return jsonify({"error": "Already exists"})
    AVAILABLE_IDS.append(d.id)
    sheets_api.append(d.to_sheet())
    return jsonify(content)


@app.route("/dira/<dira_id>", methods=["GET"])
def send_dira(dira_id):
    dira_row = sheets_api.get(dira_id)[0]
    d = Dira.from_sheet(*dira_row)
    if not sheets_api.is_sent(dira_id):
        gmail_api.send_message(d.subject, d.body)
        sheets_api.set_sent(dira_id)
    return jsonify(d.to_dict())



@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    return response

if __name__ == '__main__':
    app.run()