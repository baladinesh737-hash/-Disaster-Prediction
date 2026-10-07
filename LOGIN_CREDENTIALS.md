# GravityShift AI - Login Credentials

## Role-Based Login System

The system now uses a simple role-based login flow with 4 dashboard options.

### Login Flow

1. **User Dashboard** - No password required, direct access
2. **Admin Dashboard** - Requires admin password
3. **Rescue Team Dashboard** - Requires rescue password
4. **Government Dashboard** - Requires government password

---

## Default Passwords

| Role | Password | Environment Variable |
|------|----------|----------------------|
| Admin | `admin123` | `ADMIN_PASSWORD` |
| Rescue | `rescue123` | `RESCUE_PASSWORD` |
| Government | `gov123` | `GOVERNMENT_PASSWORD` |

---

## How to Change Passwords

### Option 1: Environment Variables (.env file)

Create or edit `.env` file in the `backend/` directory:

```env
ADMIN_PASSWORD=your_admin_password
RESCUE_PASSWORD=your_rescue_password
GOVERNMENT_PASSWORD=your_government_password
```

### Option 2: Direct in app.py

Edit `backend/app.py` around line 50:

```python
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
RESCUE_PASSWORD = os.getenv("RESCUE_PASSWORD", "rescue123")
GOVERNMENT_PASSWORD = os.getenv("GOVERNMENT_PASSWORD", "gov123")
```

Change the default values (second parameter) to your desired passwords.

---

## API Endpoint

**POST** `/role-login`

### Request
```json
{
  "role": "admin|rescue|government",
  "password": "entered_password"
}
```

### Response (Success)
```json
{
  "success": true,
  "message": "Admin login successful",
  "token": "jwt_token_here"  // Only for admin
}
```

### Response (Failure)
```json
{
  "success": false,
  "message": "Invalid admin password"
}
```

---

## Frontend Behavior

- Click on a dashboard card
- If **User** → Direct redirect to `user.html`
- If **Admin/Rescue/Government** → Password modal appears
- Enter password and click "Login"
- On success → Redirect to respective dashboard
- On failure → Error message in modal, password field cleared

---

## Testing

1. Start backend: `python app.py`
2. Open `frontend/index.html` in browser
3. Click "Admin Dashboard"
4. Enter password: `admin123`
5. Should redirect to `admin.html`

---

## Security Notes

- Passwords are validated server-side
- Admin receives JWT token for session management
- Change default passwords before production deployment
- Use environment variables for sensitive credentials
