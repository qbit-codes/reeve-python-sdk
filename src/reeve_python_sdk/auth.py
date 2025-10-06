"""
Authentication module for the Reeve Python SDK.
"""

from typing import Dict, Optional

from .client import BaseClient
from .models import LoginResponse, RegisterResponse, ChangePasswordResponse


class AuthModule:
    """Handles authentication operations with the Reeve API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the Auth module.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    async def login(self, username: str, password: str) -> LoginResponse:
        """
        Authenticate with username and password to receive JWT token.

        Args:
            username: Username for authentication
            password: Password for authentication

        Returns:
            LoginResponse containing token, expiration, username, and role

        Raises:
            AuthenticationError: If credentials are invalid
            ValidationError: If username or password is missing

        Example:
            >>> async with ReeveClient(api_url="https://api.reeve.example.com") as client:
            ...     login_response = await client.auth.login(
            ...         username="admin",
            ...         password="password123"
            ...     )
            ...     print(f"Token: {login_response.token}")
        """
        data = {
            "username": username,
            "password": password
        }
        response = await self.client.post("/Auth/login", json_data=data)
        return LoginResponse.from_dict(response)

    async def register(
        self,
        username: str,
        email: str,
        password: str,
        role: Optional[str] = "User"
    ) -> RegisterResponse:
        """
        Register a new user (Admin only).

        Args:
            username: Username for the new user
            email: Email address for the new user
            password: Password for the new user
            role: Role for the new user (default: "User")

        Returns:
            RegisterResponse containing success message and user info

        Raises:
            AuthenticationError: If not authenticated or not an admin
            ConflictError: If username already exists
            ValidationError: If registration data is invalid

        Example:
            >>> async with ReeveClient(
            ...     api_url="https://api.reeve.example.com",
            ...     api_key="admin-token"
            ... ) as client:
            ...     register_response = await client.auth.register(
            ...         username="newuser",
            ...         email="user@example.com",
            ...         password="password123",
            ...         role="User"
            ...     )
            ...     print(register_response.message)
        """
        data = {
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
        response = await self.client.post("/Auth/register", json_data=data)
        return RegisterResponse.from_dict(response)

    async def change_password(
        self,
        current_password: str,
        new_password: str
    ) -> ChangePasswordResponse:
        """
        Change password for the authenticated user.

        Args:
            current_password: Current password for verification
            new_password: New password to set

        Returns:
            ChangePasswordResponse containing success message

        Raises:
            AuthenticationError: If not authenticated or current password is wrong
            ValidationError: If password requirements are not met

        Example:
            >>> async with ReeveClient(
            ...     api_url="https://api.reeve.example.com",
            ...     api_key="user-token"
            ... ) as client:
            ...     response = await client.auth.change_password(
            ...         current_password="oldpass123",
            ...         new_password="newpass456"
            ...     )
            ...     print(response.message)
        """
        data = {
            "currentPassword": current_password,
            "newPassword": new_password
        }
        response = await self.client.post("/Auth/change-password", json_data=data)
        return ChangePasswordResponse.from_dict(response)
