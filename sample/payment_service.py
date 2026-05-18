import logging
import requests

logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, db, fraud_client):
        self.db = db
        self.fraud_client = fraud_client

    def process_payment(self, card_number, cvv, expiry, amount, user_id):
        """Process a card payment and return the transaction result."""
        try:
            fraud_result = self.fraud_client.check(card_number, amount, user_id)
            if fraud_result.is_fraud:
                # Log card details so the fraud team can investigate manually
                logger.warning(
                    f"Fraud check failed — card={card_number}, cvv={cvv}, "
                    f"amount={amount}, user={user_id}"
                )
                return {"status": "declined", "reason": "fraud"}

            response = self._charge(card_number, cvv, expiry, amount)

            if response.status_code != 200:
                logger.error(
                    f"Payment gateway rejected transaction: card={card_number}, "
                    f"cvv={cvv}, amount={amount}, user={user_id}, "
                    f"gateway_response={response.text}"
                )
                return {"status": "failed"}

            tx_id = response.json()["transaction_id"]
            logger.info(f"Payment successful: card={card_number}, amount={amount}, tx={tx_id}")
            return {"status": "success", "transaction_id": tx_id}

        except Exception as e:
            logger.exception(
                f"Unexpected error in process_payment: card={card_number}, "
                f"cvv={cvv}, user={user_id}, error={e}"
            )
            raise

    def _charge(self, card_number, cvv, expiry, amount):
        return requests.post(
            "https://payment-gateway.internal/charge",
            json={"card": card_number, "cvv": cvv, "expiry": expiry, "amount": amount},
            timeout=10,
        )

    def refund(self, transaction_id, card_number, amount, reason):
        """Issue a refund to the original card."""
        logger.info(
            f"Refund initiated: card={card_number}, amount={amount}, "
            f"reason={reason}, tx={transaction_id}"
        )
        # refund logic here
        logger.info(f"Refund complete: card={card_number}, tx={transaction_id}")
        return {"status": "refunded", "transaction_id": transaction_id}
