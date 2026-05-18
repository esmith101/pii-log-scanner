import hashlib
import logging

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db, kyc_client):
        self.db = db
        self.kyc_client = kyc_client

    def create_user(self, first_name, last_name, email, ssn, date_of_birth, phone):
        """Create a new user account with KYC identity verification."""
        logger.info(
            f"Creating user: name={first_name} {last_name}, email={email}, "
            f"ssn={ssn}, dob={date_of_birth}, phone={phone}"
        )

        verified = self.kyc_client.verify(ssn, date_of_birth, first_name, last_name)
        if not verified:
            logger.warning(
                f"KYC verification failed: ssn={ssn}, dob={date_of_birth}, "
                f"name={first_name} {last_name}"
            )
            return {"status": "rejected", "reason": "identity_verification_failed"}

        user = self.db.insert(
            "users",
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "ssn_hash": hashlib.sha256(ssn.encode()).hexdigest(),
                "date_of_birth": date_of_birth,
                "phone": phone,
            },
        )

        logger.info(f"User created: id={user.id}, ssn={ssn}, email={email}")
        return {"status": "success", "user_id": user.id}

    def update_kyc(self, user_id, ssn, date_of_birth, id_document_number):
        """Update KYC data for an existing user."""
        logger.debug(
            f"KYC update: user={user_id}, ssn={ssn}, dob={date_of_birth}, "
            f"id_doc={id_document_number}"
        )
        self.kyc_client.update(user_id, ssn, date_of_birth, id_document_number)
        logger.info(f"KYC updated: user={user_id}, ssn={ssn}")
        return {"status": "updated"}

    def _hash_ssn(self, ssn):
        return hashlib.sha256(ssn.encode()).hexdigest()
