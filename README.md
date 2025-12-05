
# Discord Bot Template for Render.com

## Files
- bot.py — mã bot
- requirements.txt — thư viện Python
- Procfile — Render worker định nghĩa lệnh chạy

## Deploy lên Render
1. Upload toàn bộ project lên GitHub
2. Vào https://dashboard.render.com
3. New → Worker
4. Chọn repo
5. Build command: pip install -r requirements.txt
6. Add Environment Variable:
   DISCORD_TOKEN = <token bot của bạn>
7. Deploy
8. Xem Logs để kiểm tra bot online
