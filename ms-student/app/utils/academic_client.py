import logging
import os

import requests
from pybreaker import CircuitBreaker

logger = logging.getLogger(__name__)


class AcademicServiceClient:

    BASE_URL = os.getenv("ACADEMIC_SERVICE_URL", "http://academico.universidad.localhost")
    TIMEOUT = int(os.getenv("ACADEMIC_SERVICE_TIMEOUT", "5"))

    # Circuit breaker configuration
    breaker = CircuitBreaker(
        fail_max=5,  # Open circuit after 5 failures
        reset_timeout=60,  # Try to recover after 60 seconds
        listeners=[],  # Add listeners for monitoring if needed
        name="academic_service_breaker"
    )

    def validate_specialty(self, specialty_id: int) -> bool:
        try:
            return self.breaker.call(self._call_validate_specialty, specialty_id)
        except Exception as e:
            logger.error(f"Circuit breaker open or error validating specialty {specialty_id}: {str(e)}")
            raise

    def _call_validate_specialty(self, specialty_id: int) -> bool:
        try:
            url = f"{self.BASE_URL}/especialidades/{specialty_id}"
            response = requests.get(url, timeout=self.TIMEOUT)

            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            response.raise_for_status()
            return False

        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            logger.error(f"Error validating specialty {specialty_id}: {str(e)}")
            raise

    def get_specialty(self, specialty_id: int) -> dict | None:
        try:
            return self.breaker.call(self._call_get_specialty, specialty_id)
        except Exception as e:
            logger.error(f"Circuit breaker open or error fetching specialty {specialty_id}: {str(e)}")
            return None

    def _call_get_specialty(self, specialty_id: int) -> dict | None:
        try:
            url = f"{self.BASE_URL}/especialidades/{specialty_id}"
            response = requests.get(url, timeout=self.TIMEOUT)

            if response.status_code == 200:
                return response.json()
            return None

        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            logger.error(f"Error fetching specialty {specialty_id}: {str(e)}")
            return None


# Singleton instance
academic_service_client = AcademicServiceClient()
