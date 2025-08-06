# ProNet Connect Product Requirements (PRD)

## Product Overview

ProNet Connect is a professional networking platform inspired by BNI Connect. The platform enables members to register, build profiles, make meaningful connections, track business referrals, schedule meetings, and manage notifications, all from a modern, web-based interface.

---

## Functional Requirements

### User Roles & Registration
- **Members** can register, log in, create/update their profiles, send/accept connections, referrals, meetings, view notifications.
- **Admins** may be added for moderation (future enhancement; code role exists).

### Core Features

#### 1. Authentication & Security
- User registration with email/password
- Login issues JWT token
- JWT checks required for all protected routes

#### 2. Profile Management
- Profile creation prompted post-registration
- Allows: name, business, title, phone, bio, location, LinkedIn
- Edit profile anytime

#### 3. Connection Management
- List members with search
- Send/accept/reject connection requests
- View current connections

#### 4. Referrals
- Send referrals (business leads) to other members
- Track sent and received referrals
- Referral status: sent, accepted, rejected, completed

#### 5. Meetings
- Schedule meetings with other members
- View meetings list, update/cancel meetings
- Meetings include topic, datetime, location, status

#### 6. Notifications
- Automatic notification on key actions (e.g., new connection request)
- View unread/read notifications

#### 7. Dashboard
- Personalized member dashboard with links to all major sections and at-a-glance info

---

## User Flow Overview

1. **Registration:** User registers, logs in, and is directed to create their profile.
2. **Dashboard:** Shows all sections and quick navigation: Members, Referrals, Meetings, Notifications, Profile.
3. **Members:** Browse/search network, initiate connections.
4. **Connections:** View, accept, decline requests.
5. **Referrals:** Send/track business leads—status visible throughout workflow.
6. **Meetings:** Schedule/view meetings with reminders.
7. **Notifications:** Timely system alerts regarding referrals, meetings, etc.

---

## Non-Functional Requirements

- **Responsiveness:** Web app usable on desktop, tablet, mobile.
- **Security:** All personal data protected; backend enforces access control via JWT.
- **Extensibility:** Architecture allows future enhancements (e.g., payments, chapter management, reports).

---

## Acceptance Criteria

- Registration/login, JWT-protected flows, and UI should function as described.
- All flows (connections, referrals, meetings, notifications, profile) testable with independent users.
- Database health check and entity presence are automated.
- End-to-end integration between containers (frontend, backend, database).

---

## References

See:
- [ARCHITECTURE.md](../pronet-connect-127616-127627/ARCHITECTURE.md)
- [DESIGN.md](../pronet-connect-127616-127625/DESIGN.md)
