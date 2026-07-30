import hmac
import hashlib
import base64

# eSewa UAT (test) credentials — replace with your live merchant code/secret when you go live
ESEWA_MERCHANT_CODE = "EPAYTEST"
ESEWA_SECRET_KEY = "8gBm/:&EnhH.1/q"

ESEWA_PAYMENT_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
ESEWA_STATUS_CHECK_URL = "https://rc.esewa.com.np/api/epay/transaction/status/"


def generate_signature(total_amount, transaction_uuid, product_code):
    """
    eSewa requires a signature over specific fields, in this exact order and format.
    """
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    secret_bytes = ESEWA_SECRET_KEY.encode('utf-8')
    message_bytes = message.encode('utf-8')
    hash_bytes = hmac.new(secret_bytes, message_bytes, hashlib.sha256).digest()
    signature = base64.b64encode(hash_bytes).decode('utf-8')
    return signature