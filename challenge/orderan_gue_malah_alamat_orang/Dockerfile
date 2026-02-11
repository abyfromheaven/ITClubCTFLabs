# 1. Gunakan image Python yang ringan
FROM python:3.9-slim

# 2. Tentukan direktori kerja di dalam kontainer
WORKDIR /app

# 3. Copy file requirements dan install library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy seluruh kode lab ke dalam kontainer
COPY . .

# 5. Jalankan Flask (gunakan Gunicorn agar lebih stabil untuk CTF)
RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
