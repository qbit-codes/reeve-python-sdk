"""
Data models for the Reeve Python SDK.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from dateutil import parser


@dataclass
class Person:
    """Represents a person in the Reeve system."""

    id: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Person":
        """Create a Person instance from a dictionary."""
        return cls(
            id=data.get("id"),
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            created_at=parser.parse(data["createdAt"]) if data.get("createdAt") else None,
            updated_at=parser.parse(data["updatedAt"]) if data.get("updatedAt") else None,
        )

    def to_dict(self) -> dict:
        """Convert Person instance to a dictionary."""
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class Face:
    """Represents a face image in the Reeve system."""

    id: int
    path: Optional[str] = None
    person_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Face":
        """Create a Face instance from a dictionary."""
        return cls(
            id=data.get("id"),
            path=data.get("path"),
            person_id=data.get("personId"),
            created_at=parser.parse(data["createdAt"]) if data.get("createdAt") else None,
            updated_at=parser.parse(data["updatedAt"]) if data.get("updatedAt") else None,
        )

    def to_dict(self) -> dict:
        """Convert Face instance to a dictionary."""
        return {
            "id": self.id,
            "path": self.path,
            "personId": self.person_id,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class FaceAttributes:
    """Face attributes returned from recognition/verification operations."""

    age: Optional[str] = None
    gender: Optional[str] = None
    expression: Optional[str] = None
    blink: Optional[str] = None
    mouth_open: Optional[str] = None
    glasses: Optional[str] = None
    dark_glasses: Optional[str] = None
    ethnicity: Optional[str] = None
    beard: Optional[str] = None
    mustache: Optional[str] = None
    smile: Optional[str] = None
    face_mask: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "FaceAttributes":
        """Create a FaceAttributes instance from a dictionary."""
        if not data:
            return cls()
        return cls(
            age=data.get("age"),
            gender=data.get("gender"),
            expression=data.get("expression"),
            blink=data.get("blink"),
            mouth_open=data.get("mouthOpen"),
            glasses=data.get("glasses"),
            dark_glasses=data.get("darkGlasses"),
            ethnicity=data.get("ethnicity"),
            beard=data.get("beard"),
            mustache=data.get("mustache"),
            smile=data.get("smile"),
            face_mask=data.get("faceMask"),
        )


@dataclass
class UserInfo:
    """User information."""

    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "UserInfo":
        """Create a UserInfo instance from a dictionary."""
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            email=data.get("email"),
            role=data.get("role"),
        )


@dataclass
class LoginResponse:
    """Response from login endpoint."""

    token: str
    expires_at: Optional[datetime] = None
    username: Optional[str] = None
    role: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "LoginResponse":
        """Create a LoginResponse instance from a dictionary."""
        return cls(
            token=data.get("token"),
            expires_at=parser.parse(data["expiresAt"]) if data.get("expiresAt") else None,
            username=data.get("username"),
            role=data.get("role"),
        )


@dataclass
class RegisterResponse:
    """Response from register endpoint."""

    message: str
    user: Optional[UserInfo] = None

    @classmethod
    def from_dict(cls, data: dict) -> "RegisterResponse":
        """Create a RegisterResponse instance from a dictionary."""
        return cls(
            message=data.get("message"),
            user=UserInfo.from_dict(data["user"]) if data.get("user") else None,
        )


@dataclass
class ChangePasswordResponse:
    """Response from change password endpoint."""

    message: str

    @classmethod
    def from_dict(cls, data: dict) -> "ChangePasswordResponse":
        """Create a ChangePasswordResponse instance from a dictionary."""
        return cls(message=data.get("message"))


@dataclass
class IdentifyResult:
    """Result from face recognition operation."""

    name: Optional[str] = None
    threshold: Optional[int] = None
    score: Optional[int] = None
    is_match_found: Optional[bool] = None
    attributes: Optional[FaceAttributes] = None

    @classmethod
    def from_dict(cls, data: dict) -> "IdentifyResult":
        """Create an IdentifyResult instance from a dictionary."""
        if not data:
            return cls()
        return cls(
            name=data.get("name"),
            threshold=data.get("thresold"),  # Note: API has typo "thresold" instead of "threshold"
            score=data.get("score"),
            is_match_found=data.get("isMatchFound"),
            attributes=FaceAttributes.from_dict(data["attributes"]) if data.get("attributes") else None,
        )


@dataclass
class VerificationResult:
    """Result from face verification against a person."""

    success: bool
    verification_succeeded: bool
    error: Optional[str] = None
    score: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "VerificationResult":
        """Create a VerificationResult instance from a dictionary."""
        if not data:
            return cls(success=False, verification_succeeded=False)
        return cls(
            success=data.get("success", False),
            verification_succeeded=data.get("verificationSucceeded", False),
            error=data.get("error"),
            score=data.get("score"),
        )


@dataclass
class SubjectVerificationResult:
    """Result from subject-to-subject face verification."""

    subject_not_suitable: bool
    verification_succeeded: bool
    score: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "SubjectVerificationResult":
        """Create a SubjectVerificationResult instance from a dictionary."""
        if not data:
            return cls(subject_not_suitable=True, verification_succeeded=False)
        return cls(
            subject_not_suitable=data.get("subjectNotSuitable", False),
            verification_succeeded=data.get("verificationSucceeded", False),
            score=data.get("score"),
        )


@dataclass
class APIResponse:
    """Wrapper for API responses from Reeve."""

    success: bool
    result: Any = None
    error: Optional[Dict] = None
    status_code: Optional[int] = None
    timestamp: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "APIResponse":
        """Create an APIResponse instance from a dictionary."""
        # Handle different response formats
        if "error" in data and data["error"]:
            return cls(
                success=data.get("success", False),
                error=data.get("error"),
                status_code=data.get("statusCode"),
                timestamp=data.get("timestamp")
            )

        return cls(
            success=data.get("success", True),
            result=data.get("result"),
            status_code=data.get("statusCode"),
            timestamp=data.get("timestamp")
        )

    def is_success(self) -> bool:
        """Check if the API call was successful."""
        return self.success and not self.error
