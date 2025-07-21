# API Endpoints Documentation

Dokumentasi lengkap untuk semua endpoint API yang tersedia di `main_api.py`.

## 📚 Book Management Endpoints

### GET /books
Mendapatkan daftar buku dengan filtering dan pagination.

**Parameters:**
- `page` (int, optional): Halaman yang diminta (default: 1)
- `per_page` (int, optional): Jumlah item per halaman (max: 100, default: 20)
- `status` (string, optional): Filter berdasarkan status download
- `extension` (string, optional): Filter berdasarkan ekstensi file

**Example:**
```bash
curl "http://localhost:8080/books?page=1&per_page=20&status=pending"
```

**Response:**
```json
{
  "status": "success",
  "page": 1,
  "per_page": 20,
  "total": 150,
  "total_pages": 8,
  "books": [
    {
      "id": "book_123",
      "title": "Sample Book",
      "author": "Sample Author",
      "download_status": "pending",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### GET /books/{book_id}
Mendapatkan detail buku tertentu.

**Example:**
```bash
curl "http://localhost:8080/books/book_123"
```

### PUT /books/{book_id}
Update data buku tertentu.

**Example:**
```bash
curl -X PUT "http://localhost:8080/books/book_123" \
  -H "Content-Type: application/json" \
  -d '{"download_status": "done", "files_url_drive": "https://drive.google.com/..."}'
```

### DELETE /books/{book_id}
Hapus buku tertentu.

**Example:**
```bash
curl -X DELETE "http://localhost:8080/books/book_123"
```

### POST /books/bulk_update
Update multiple buku sekaligus.

**Example:**
```bash
curl -X POST "http://localhost:8080/books/bulk_update" \
  -H "Content-Type: application/json" \
  -d '[
    {"id": "book_123", "download_status": "done"},
    {"id": "book_124", "download_status": "failed"}
  ]'
```

### POST /books/cleanup
Cleanup buku tidak lengkap atau duplikat.

**Parameters:**
- `type` (string): Jenis cleanup (`incomplete`, `duplicate`, `old`)
- `delete` (boolean): Jika true, hapus data. Jika false, hanya analisis
- `days` (int, optional): Untuk type `old`, jumlah hari (default: 30)

**Example:**
```bash
curl -X POST "http://localhost:8080/books/cleanup" \
  -H "Content-Type: application/json" \
  -d '{"type": "incomplete", "delete": false}'
```

## 🔍 Keyword Management Endpoints

### GET /keywords
Mendapatkan daftar keyword dengan filtering dan pagination.

**Parameters:**
- `status` (string, optional): Filter berdasarkan status
- `type` (string, optional): Filter berdasarkan tipe keyword
- `page` (int, optional): Halaman (default: 1)
- `per_page` (int, optional): Item per halaman (max: 100, default: 50)

**Example:**
```bash
curl "http://localhost:8080/keywords?status=pending&type=keyword&page=1&per_page=50"
```

### POST /keywords
Membuat keyword baru (single atau bulk).

**Single Create:**
```bash
curl -X POST "http://localhost:8080/keywords" \
  -H "Content-Type: application/json" \
  -d '{"input_text": "python programming", "keyword_type": "keyword", "status": "pending"}'
```

**Bulk Create:**
```bash
curl -X POST "http://localhost:8080/keywords" \
  -H "Content-Type: application/json" \
  -d '[
    {"input_text": "python programming", "keyword_type": "keyword"},
    {"input_text": "machine learning", "keyword_type": "keyword"}
  ]'
```

### GET /keywords/{keyword_id}
Mendapatkan detail keyword tertentu.

### PUT /keywords/{keyword_id}
Update keyword tertentu.

### DELETE /keywords/{keyword_id}
Hapus keyword tertentu.

### POST /keywords/status
Update status keyword berdasarkan input_text.

**Example:**
```bash
curl -X POST "http://localhost:8080/keywords/status" \
  -H "Content-Type: application/json" \
  -d '{"input_text": "python programming", "keyword_type": "keyword", "status": "completed"}'
```

### POST /keywords/sync
Sync keyword dari sumber eksternal (Google Sheets, dll).

**Example:**
```bash
curl -X POST "http://localhost:8080/keywords/sync" \
  -H "Content-Type: application/json" \
  -d '[
    {"input_text": "new keyword 1", "keyword_type": "keyword", "status": "pending"},
    {"input_text": "new keyword 2", "keyword_type": "keyword", "status": "pending"}
  ]'
```

### POST /keywords/cleanup
Cleanup keyword yang sudah selesai diproses.

**Example:**
```bash
curl -X POST "http://localhost:8080/keywords/cleanup" \
  -H "Content-Type: application/json" \
  -d '{"delete": true}'
```

## 👤 Account Management Endpoints

### GET /accounts
Mendapatkan daftar akun dengan filtering dan pagination.

**Parameters:**
- `status` (string, optional): Filter berdasarkan status
- `page` (int, optional): Halaman (default: 1)
- `per_page` (int, optional): Item per halaman (max: 100, default: 50)

**Example:**
```bash
curl "http://localhost:8080/accounts?status=active&page=1&per_page=50"
```

### POST /accounts
Membuat akun baru (single atau bulk).

**Single Create:**
```bash
curl -X POST "http://localhost:8080/accounts" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "status": "active"}'
```

**Bulk Create:**
```bash
curl -X POST "http://localhost:8080/accounts" \
  -H "Content-Type: application/json" \
  -d '[
    {"email": "user1@example.com", "password": "pass1"},
    {"email": "user2@example.com", "password": "pass2"}
  ]'
```

### GET /accounts/{account_id}
Mendapatkan detail akun tertentu.

### PUT /accounts/{account_id}
Update akun tertentu.

### DELETE /accounts/{account_id}
Hapus akun tertentu.

### GET /accounts/available
Mendapatkan akun yang tersedia (tidak expired hari ini).

**Example:**
```bash
curl "http://localhost:8080/accounts/available"
```

**Response:**
```json
{
  "status": "success",
  "message": "Found 5 available accounts",
  "accounts": [
    {
      "id": 1,
      "email": "user@example.com",
      "password": "***",
      "last_limit_date": null,
      "status": "active"
    }
  ]
}
```

### POST /accounts/reset_limits
Reset semua limit akun (set last_limit_date = null).

**Example:**
```bash
curl -X POST "http://localhost:8080/accounts/reset_limits"
```

### POST /accounts/cleanup
Cleanup akun yang expired hari ini.

**Example:**
```bash
curl -X POST "http://localhost:8080/accounts/cleanup" \
  -H "Content-Type: application/json" \
  -d '{"delete": true}'
```

## 👥 User Management Endpoints

### GET /users
Mendapatkan daftar user dengan filtering dan pagination.

**Parameters:**
- `status` (string, optional): Filter berdasarkan status
- `role` (string, optional): Filter berdasarkan role
- `page` (int, optional): Halaman (default: 1)
- `per_page` (int, optional): Item per halaman (max: 100, default: 50)

**Example:**
```bash
curl "http://localhost:8080/users?status=active&role=user&page=1&per_page=50"
```

### POST /users
Membuat user baru.

**Example:**
```bash
curl -X POST "http://localhost:8080/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password_hash": "hashed_password_here",
    "role": "user",
    "status": "active"
  }'
```

### GET /users/{user_id}
Mendapatkan detail user tertentu.

### PUT /users/{user_id}
Update user tertentu.

### DELETE /users/{user_id}
Hapus user tertentu.

### POST /users/login
Login user dan update last_login.

**Example:**
```bash
curl -X POST "http://localhost:8080/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password_hash": "hashed_password_here"}'
```

### POST /users/cleanup
Cleanup user yang tidak aktif.

**Example:**
```bash
curl -X POST "http://localhost:8080/users/cleanup" \
  -H "Content-Type: application/json" \
  -d '{"delete": true, "days": 90}'
```

## 🗄️ Database Management Endpoints

### GET /database/stats
Mendapatkan statistik komprehensif database.

**Example:**
```bash
curl "http://localhost:8080/database/stats"
```

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-01-01T00:00:00",
  "totals": {
    "books": 1000,
    "keywords": 500,
    "accounts": 50,
    "users": 25
  },
  "book_stats": {
    "pending": 200,
    "done": 700,
    "failed": 100
  },
  "keyword_stats": {
    "pending": 300,
    "completed": 200
  },
  "account_stats": {
    "available": 40,
    "expired_today": 5,
    "expired_other": 5
  },
  "user_stats": {
    "active": 20,
    "inactive": 5
  }
}
```

### POST /database/cleanup
Melakukan operasi cleanup database.

**Parameters:**
- `operations` (array): Array operasi yang akan dilakukan
- `delete` (boolean): Jika true, hapus data. Jika false, hanya analisis

**Available Operations:**
- `incomplete_books`: Cleanup buku tidak lengkap
- `processed_keywords`: Cleanup keyword selesai
- `expired_accounts`: Cleanup akun expired
- `stuck_statuses`: Reset status stuck

**Example:**
```bash
curl -X POST "http://localhost:8080/database/cleanup" \
  -H "Content-Type: application/json" \
  -d '{
    "operations": ["incomplete_books", "processed_keywords", "expired_accounts", "stuck_statuses"],
    "delete": false
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Database cleanup completed",
  "results": {
    "incomplete_books": {"found": 10},
    "processed_keywords": {"found": 50},
    "expired_accounts": {"found": 5},
    "stuck_statuses": {"reset": 3}
  },
  "delete_mode": false
}
```

### POST /database/backup
Membuat backup database dalam format JSON.

**Example:**
```bash
curl -X POST "http://localhost:8080/database/backup"
```

**Response:**
```json
{
  "status": "success",
  "message": "Database backup created successfully",
  "backup_file": "database_backup_20240101_120000.json",
  "records_backed_up": {
    "books": 1000,
    "keywords": 500,
    "accounts": 50,
    "users": 25
  }
}
```

## 🔧 Existing Endpoints (Original)

### POST /upload_data
Upload data buku (single atau batch).

### POST /claim_books
Claim buku untuk download processing.

### POST /reset_inprogress
Reset buku in_progress menjadi pending.

### POST /reset_status
Reset status buku ke target status.

### GET /get_status_distribution
Mendapatkan distribusi status buku.

### GET /get_ready_for_upload
Mendapatkan buku siap untuk upload.

### POST /claim_upload_batch
Claim buku untuk upload processing.

### GET /search_books
Search buku dengan pagination.

### GET /stats
Statistik database (legacy).

### GET /get_direct_link/{book_id}
Mendapatkan direct link buku.

### GET /book_detail/{book_id}
Detail buku tertentu.

### GET/POST /bookmark
Management bookmark user.

### GET /health
Health check endpoint.

### GET /metrics
Server metrics.

## 📊 Rate Limiting

Semua endpoint memiliki rate limiting untuk mencegah abuse:

- **High frequency endpoints**: 100 requests/minute
- **Medium frequency endpoints**: 50 requests/minute  
- **Low frequency endpoints**: 20 requests/minute
- **Cleanup operations**: 5 requests/minute
- **Backup operations**: 2 requests/minute

## 🛡️ Error Handling

Semua endpoint mengembalikan response dalam format yang konsisten:

**Success Response:**
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {...}
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Error description",
  "error_id": "abc12345"
}
```

**HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid data)
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

## 🚀 Usage Examples

### 1. Cleanup Database Secara Rutin
```bash
# Analisis dulu
curl -X POST "http://localhost:8080/database/cleanup" \
  -H "Content-Type: application/json" \
  -d '{"operations": ["incomplete_books", "processed_keywords"], "delete": false}'

# Jika yakin, lakukan cleanup
curl -X POST "http://localhost:8080/database/cleanup" \
  -H "Content-Type: application/json" \
  -d '{"operations": ["incomplete_books", "processed_keywords"], "delete": true}'
```

### 2. Reset Account Limits Harian
```bash
curl -X POST "http://localhost:8080/accounts/reset_limits"
```

### 3. Monitor Database Health
```bash
# Cek statistik
curl "http://localhost:8080/database/stats"

# Cek health
curl "http://localhost:8080/health"
```

### 4. Bulk Operations
```bash
# Bulk update books
curl -X POST "http://localhost:8080/books/bulk_update" \
  -H "Content-Type: application/json" \
  -d '[
    {"id": "book_1", "download_status": "done"},
    {"id": "book_2", "download_status": "done"}
  ]'

# Bulk create keywords
curl -X POST "http://localhost:8080/keywords" \
  -H "Content-Type: application/json" \
  -d '[
    {"input_text": "keyword1", "keyword_type": "keyword"},
    {"input_text": "keyword2", "keyword_type": "keyword"}
  ]'
```

## 📝 Notes

1. **Password Security**: Password akun disembunyikan dalam response (`"***"`)
2. **Backup**: Backup dibuat dalam format JSON, untuk production gunakan tools backup proper
3. **Rate Limiting**: Rate limiting menggunakan in-memory storage, untuk production gunakan Redis
4. **Database**: Support SQLite dan MySQL (konfigurasi di environment variable)
5. **Logging**: Semua operasi di-log ke file `logs/flask_api.log`

---

**API Version**: 1.0.0  
**Last Updated**: January 2024  
**Base URL**: `http://localhost:8080` 