=========
Changelog
=========

Version 0.2.0 (2025-10-06)
==========================

**BREAKING CHANGES**

* **Authentication System Overhaul**: Removed ``Auth.get_token()`` method
* New authentication flow based on username/password with JWT tokens
* API now uses new authentication endpoints: ``/Auth/login``, ``/Auth/register``, ``/Auth/change-password``

**New Features**

* **Authentication Methods**:

  * ``Auth.login(username, password)``: Authenticate and receive JWT token
  * ``Auth.register(username, email, password, role)``: Register new users (Admin only)
  * ``Auth.change_password(current_password, new_password)``: Change user password

* **Dual Authentication Support in ReeveClient**:

  * Direct API key: ``ReeveClient(api_url, api_key="token")``
  * Username/password with auto-login: ``ReeveClient(api_url, username="user", password="pass")``

* **New Data Models**:

  * ``Face``: Face image representation with id, path, person_id, timestamps
  * ``FaceAttributes``: Face attributes (age, gender, expression, glasses, etc.)
  * ``UserInfo``: User information (id, username, email, role)
  * ``LoginResponse``: Login response with token, expiration, username, role
  * ``RegisterResponse``: Registration response with message and user info
  * ``ChangePasswordResponse``: Password change confirmation

* **Recognition Result Models**:

  * ``IdentifyResult``: Face recognition result with name, score, threshold, attributes
  * ``VerificationResult``: Face verification result with success status and score
  * ``SubjectVerificationResult``: Subject-to-subject verification result

* **Exception Handling**:

  * ``ConflictError``: New exception for 409 HTTP status (e.g., duplicate username)
  * Enhanced error handling in BaseClient for 409 responses

* **Enhanced API Response Structure**:

  * All responses now include: ``success``, ``error``, ``result``, ``statusCode``, ``timestamp``
  * Updated ``APIResponse`` model to match new structure

**Documentation**

* Updated ``docs/swagger.json`` to API v1 specification
* Enhanced ``CLAUDE.md`` with new authentication flows and usage examples
* Updated architecture notes with new models and authentication methods

**Migration Guide from v0.1.x**

1. Replace ``await client.auth.get_token()`` with ``await client.auth.login(username, password)``
2. Update client initialization:

   * Old: ``ReeveClient(api_url, api_key)``
   * New: ``ReeveClient(api_url, username="user", password="pass")`` OR ``ReeveClient(api_url, api_key="token")``

3. Handle new ``ConflictError`` exception for duplicate resources
4. Update response handling to use new structure with ``statusCode`` and ``timestamp``

Version 0.1.0 (2025-10-01)
==========================

* Initial release
* Basic authentication with Bearer JWT
* Person management (create, list, edit, delete)
* Face management (add, list, delete)
* Face recognition and verification
* Async-first architecture with aiohttp
