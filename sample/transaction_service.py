import logging

logger = logging.getLogger(__name__)


class TransactionService:
    def __init__(self, db):
        self.db = db

    def get_transactions(self, account_number, start_date, end_date, user_id):
        """Retrieve transaction history for an account."""
        logger.debug(
            f"Fetching transactions: account={account_number}, user={user_id}, "
            f"range={start_date} to {end_date}"
        )
        transactions = self.db.query(
            "SELECT * FROM transactions WHERE account_number = ? AND date BETWEEN ? AND ?",
            (account_number, start_date, end_date),
        )
        logger.info(
            f"Fetched {len(transactions)} transactions: account={account_number}, user={user_id}"
        )
        return transactions

    def transfer(self, from_account, to_account, amount, routing_number, user_id):
        """Transfer funds between accounts."""
        logger.info(
            f"Transfer initiated: from={from_account}, to={to_account}, "
            f"routing={routing_number}, amount={amount}, user={user_id}"
        )
        try:
            result = self._execute_transfer(from_account, to_account, amount, routing_number)
            logger.info(
                f"Transfer complete: from={from_account}, to={to_account}, "
                f"amount={amount}, ref={result.ref_id}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Transfer failed: from={from_account}, to={to_account}, "
                f"routing={routing_number}, amount={amount}, error={e}"
            )
            raise

    def flag_suspicious(self, account_number, transaction_id, reason, user_ssn=None):
        """Flag a transaction for fraud review."""
        logger.warning(
            f"Suspicious activity: account={account_number}, tx={transaction_id}, "
            f"reason={reason}, ssn={user_ssn}"
        )
        self.db.insert(
            "fraud_flags",
            {"account_number": account_number, "transaction_id": transaction_id, "reason": reason},
        )

    def _execute_transfer(self, from_account, to_account, amount, routing_number):
        pass
