"""
Reeve Python SDK - A facial recognition API client.
"""

import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

from typing import Optional

from .client import BaseClient
from .auth import AuthModule
from .person import PersonModule
from .face import FaceModule
from .subject import SubjectModule
from .exceptions import (
    ReeveAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    ConflictError,
    APIError,
)
from .models import (
    Person,
    Face,
    FaceAttributes,
    UserInfo,
    LoginResponse,
    RegisterResponse,
    ChangePasswordResponse,
    IdentifyResult,
    VerificationResult,
    SubjectVerificationResult,
    APIResponse,
)

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "reeve_python_sdk"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


class ReeveClient(BaseClient):
    """
    Main client for interacting with the Reeve API.

    This client provides access to all Reeve API functionality including
    person management, face management, recognition, and verification.

    Authentication Methods:
        1. Direct API key (for existing tokens):
            >>> async with ReeveClient(
            ...     api_url="https://api.reeve.example.com",
            ...     api_key="your-jwt-token"
            ... ) as client:
            ...     persons = await client.person.list()

        2. Username/Password (auto-login):
            >>> async with ReeveClient(
            ...     api_url="https://api.reeve.example.com",
            ...     username="admin",
            ...     password="password123"
            ... ) as client:
            ...     persons = await client.person.list()

    Example:
        >>> import asyncio
        >>> from reeve_python_sdk import ReeveClient
        >>>
        >>> async def main():
        ...     # Login with username/password
        ...     async with ReeveClient(
        ...         api_url="https://api.reeve.example.com",
        ...         username="admin",
        ...         password="password123"
        ...     ) as client:
        ...         # Create a person
        ...         person = await client.person.add(firstname="John", lastname="Doe")
        ...         print(person)
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_url: str,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize the Reeve client.

        Args:
            api_url: Base URL of the Reeve API
            api_key: API key for authentication (Bearer token). If provided,
                     this will be used directly without login.
            username: Username for authentication. Requires password.
            password: Password for authentication. Requires username.

        Note:
            Either api_key OR (username + password) should be provided.
            If both are provided, api_key takes precedence.
            If username/password is used, login will be performed automatically
            when the client context is entered.
        """
        super().__init__(api_url, api_key)

        self._username = username
        self._password = password
        self._auto_login = username and password and not api_key

        # Initialize modules
        self.auth = AuthModule(self)
        self.person = PersonModule(self)
        self.face = FaceModule(self)
        self.subject = SubjectModule(self)

    async def __aenter__(self):
        """Async context manager entry with optional auto-login."""
        await self._create_session()

        # Perform auto-login if username/password provided
        if self._auto_login:
            login_response = await self.auth.login(self._username, self._password)
            # Update the session with the new token
            self.api_key = login_response.token
            if self._session and not self._session.closed:
                await self._session.close()
            await self._create_session()

        return self


__all__ = [
    "ReeveClient",
    # Exceptions
    "ReeveAPIError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "APIError",
    # Models
    "Person",
    "Face",
    "FaceAttributes",
    "UserInfo",
    "LoginResponse",
    "RegisterResponse",
    "ChangePasswordResponse",
    "IdentifyResult",
    "VerificationResult",
    "SubjectVerificationResult",
    "APIResponse",
    # Version
    "__version__",
]
