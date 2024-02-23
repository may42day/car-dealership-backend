from datetime import timedelta
from django.utils import timezone
import pytest
from ddf import G

from users.models import ConfirmationToken


@pytest.mark.django_db
class TestTokenValidation:
    def test_token_is_valid(self):
        """
        Test to check whether token isn't expired.
        """
        token = G(ConfirmationToken)
        assert token.is_valid()

    @pytest.mark.django_db
    def test_token_is_expired(self):
        """
        Test to check whether token is expired.
        """
        created_at = timezone.now() - timedelta(minutes=60)
        token = G(ConfirmationToken, created_at=created_at)
        assert not token.is_valid()
