
import json
from fastapi import FastAPI, Query, File, UploadFile
import base64
import urllib.parse


app = FastAPI(
    title="Mock API",
    description="Mock API's For Mobile",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


def load_mock_data():
    with open("mock_data.json", "r") as file:
        return json.load(file)


mock_data = load_mock_data()


@app.get("/")
async def welcome():
    return {"message": "Hello, how can i help you today"}


# http://0.0.0.0:8000/comunicate/?text_msg=please%20transfer%20money%20to%20wahab
@app.get("/comunicate/", summary='Send request as "Please transfer money from wahab/ahmed/ali/arsalan", Returns the Account of the requested user')
async def comunicate(text_msg: str = Query(None)):
    if text_msg is None:
        return {"error": "No text message provided"}

    text_msg = urllib.parse.unquote_plus(text_msg)

    list_of_text = ['wahab', 'ahmed', 'ali', 'arsalan']
    for string_to_check in list_of_text:
        if string_to_check.lower() in text_msg.lower():
            return mock_data['account_no']
    else:
        return {"error": "Account Not Found"}


@app.post("/process-file/", summary='Upload file to start process, Returns the Account of the requested user')
async def process_file(file: UploadFile = File(...)):
    contents = await file.read()
    decoded_file = base64.b64decode(contents)

    if decoded_file:
        return mock_data['account_no']
    else:
        return {"error": "Account Not Found"}


@app.get("/get_account_benf/{id_no}", summary='Send Account id and get benificary account ids')
async def get_account_benf(id_no: int):
    id_check = any(item.get('id') == id_no for item in mock_data['account_no'])
    if id_check:
        return mock_data['benificary']
    else:
        return {"error": "No Benificary's"}


@app.get("/amount/{id_no}", summary='Send Benificary Account id and Get Amount question')
async def ask_amount_for_transfer_to_benf(id_no: int):
    id_check = any(item.get('id') == id_no for item in mock_data['benificary'])
    if id_check:
        return {"msg": "How much amount do you want to pay ?"}
    else:
        return {"error": "Wrong Benificary ID"}


# http://0.0.0.0:8000/confirm/?text_msg=pay20%1000%rs
@app.get("/confirm/", summary="Type transaction confirmation msg, use want/pay/transfer/rs")
async def confirm_amount(text_msg: str = Query()):
    text_msg = urllib.parse.unquote_plus(text_msg)

    list_of_text = ['want', 'pay', 'transfer', 'Rs']
    for string_to_check in list_of_text:
        if string_to_check.lower() in text_msg.lower():
            response_data = {}
            response_data['message'] = 'Please select the purpose of transfer?'
            response_data['purpose'] = mock_data['purpose_of_transfer']
            return response_data
    else:
        return {"error": "Transaction Aborted"}


# http://0.0.0.0:8000/confirm-transaction/?id_no=2&acknow=yes
@app.get("/confirm-transaction/", summary='Transaction Confirm , send id and acknowledgment yes or no')
async def confirm_transaction(id_no: int = Query(), acknow: str = Query('no')):
    id_check = any(item.get('id') ==
                   id_no for item in mock_data['purpose_of_transfer'])
    if id_check and acknow == 'yes':
        print(mock_data['transaction_data'])
        for transaction in mock_data['transaction_data']:
            if id_no == transaction['id']:
                return transaction
    else:
        return {"error": "Transaction Aborted"}

# Additional endpoints can be added for specific functionalities as needed
