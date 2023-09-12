# Emotion 


## How to install

* Step 1: Create env 

```sh
python3 -m venv venv
```

* Step 2: Install requirements.tx 

```sh
pip3 install -r requirements.txt
```

* Step 3: Create file .env 

Content file 

BE_HOST=aicontest.ptit.edu.vn
BE_PORT=12004

Chạy local thì đổi sang IP và PORT của máy local

* Step 4: Run AI service in a terminal 

```sh
python3 emotion_service_main.py
```

* Step 5: Run stream main 

```sh

python3 stream_main.py
```

Note:

- Tạo ra một class trên web với địa chỉ mac tương tự máy chay code
- Lấy địa chỉ mac có thể dùng thư viện getmac trong python
- Set số lượng cam là 1
- Nhớ set IP Address cho Cam
