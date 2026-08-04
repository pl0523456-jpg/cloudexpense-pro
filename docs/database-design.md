# Database Design

## Planned Tables

### users

- id
- first_name
- last_name
- email
- password_hash
- role
- created_at

---

### expenses

- id
- user_id
- category
- amount
- description
- receipt_url
- status
- created_at

---

### approvals

- id
- expense_id
- manager_id
- decision
- comments
- approved_at

---

## Relationships

User
│
├── Many Expenses

Expense
│
└── One Approval
