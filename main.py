from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ✅ Your crypto commission wallets
WALLETS = {
    "BTC": {
        "commission_wallet": "bc1qh8es4m9mjua5w08qv00",
    },
    "USDT": {
        "commission_wallet": "UQCtCm584SIWPddaOQ9ec8MULk2Aqi5ucw2s073DzNtQQc6L",
    },
    "ETH": {
        "commission_wallet": "0xf22566f4a5b70437e33f8c846e3780f4609e2abe",
    },
    "XRP": {
        "commission_wallet": "rf9nJMNU3Y2D8EkeDG4Z4f9qUPhThdrsGk",
    },
    "SOL": {
        "commission_wallet": "5msvCNwA3boDLKrgBEA8MPTnFq4bfeEqTttyEnr2nnsM",
    },
    "BCH": {
        "commission_wallet": "bitcoincash:qzk5keejgnc0urhqtrq3lk8xrus6nef5gvxh4476qa",
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

@app.post("/process")
async def process_payment(
    request: Request,
    crypto: str = Form(...),
    recipient_wallet: str = Form(...),
    amount: float = Form(...)
):
    try:
        crypto = crypto.upper()
        if crypto not in WALLETS:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "message": "Unsupported crypto selected."
            })

        commission_wallet = WALLETS[crypto]["commission_wallet"]
        commission_amount = round(amount * 0.04, 8)
        send_amount = round(amount - commission_amount, 8)

        return templates.TemplateResponse("success.html", {
            "request": request,
            "crypto": crypto,
            "recipient_wallet": recipient_wallet,
            "send_amount": send_amount,
            "commission_wallet": commission_wallet,
            "commission_amount": commission_amount
        })

    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": f"Error: {str(e)}"
        })

# ✅ This section auto-detects port for Render or local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
