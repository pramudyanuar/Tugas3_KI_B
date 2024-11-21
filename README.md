# **TUGAS 3 KEAMANAN INFORMASI B**

## **Anggota Kelompok**

| **Anggota**               | **Tugas Utama**                                                                                      |
|---------------------------|-----------------------------------------------------------------------------------------------------|
| **Yanuar Eka Pramudya ( 5025221049 ) ** | 🔐 **Pengelolaan Kunci RSA dan PKA**<br>• Mengimplementasikan logika registrasi dan pengambilan kunci publik dari PKA.<br>• Mengembangkan fungsi RSA untuk enkripsi dan dekripsi kunci sementara.<br>• Memastikan keamanan komunikasi melalui integrasi RSA dengan PKA. |
| **Abiyu Ramadhan Kiesly ( 5025221123 ) **   | 💻 **Pengembangan Sistem Client-Server**<br>• Menerapkan komunikasi client-server menggunakan socket programming.<br>• Menangani logika pengiriman dan penerimaan pesan terenkripsi melalui server.<br>• Mengintegrasikan algoritma enkripsi DES dan RSA dalam proses client-server. |


Proyek ini adalah sistem komunikasi aman yang menggabungkan algoritma **RSA** dan **DES** untuk memastikan privasi dan integritas pesan. Sistem dirancang untuk mengenkripsi pesan antara pengguna dengan mekanisme yang menggabungkan keunggulan enkripsi **asimetris** dan **simetris**.

---

## **1. Public Key dan Private Key (RSA)**

### **Deskripsi**
- RSA adalah algoritma **enkripsi asimetris** yang menggunakan pasangan kunci:
  - **Public Key**: Dapat dibagikan secara publik dan digunakan untuk **mengenkripsi** data.
  - **Private Key**: Dirahasiakan dan digunakan untuk **mendekripsi** data.
- RSA digunakan untuk mengenkripsi **kunci sementara** (DES Key) agar aman selama pengiriman.

### **Proses**
1. **Pembuatan Kunci**:
   - Kunci RSA dibuat untuk setiap pengguna dengan menggunakan fungsi `generate_rsa_keys()`:
     ```python
     public_key, private_key = generate_rsa_keys()
     ```
   - Hasilnya adalah:
     - **Public Key**: \( (e, n) \)
     - **Private Key**: \( (d, n) \)

2. **Registrasi ke Public Key Authority (PKA)**:
   - Public key pengguna didaftarkan ke PKA untuk memungkinkan pengguna lain mengaksesnya.
   - Format pendaftaran:
     ```text
     REGISTER:username;kunci_publik
     ```

3. **Penggunaan**:
   - Ketika pengirim ingin mengirim pesan, kunci publik penerima diambil dari PKA.
   - Kunci publik digunakan untuk mengenkripsi kunci sementara.

---

## **2. Kunci Sementara (DES Key)**

### **Deskripsi**
- Kunci sementara adalah **kunci simetris** yang dibuat secara acak untuk mengenkripsi pesan menggunakan algoritma DES.
- Panjang kunci: **8 karakter** (huruf acak).

### **Proses**
1. **Pembuatan Kunci**:
   - Kunci sementara dibuat setiap kali pengirim ingin mengirim pesan.
   - Contoh pembuatan kunci:
     ```python
     des_key = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))
     ```

2. **Enkripsi Kunci Sementara**:
   - Sebelum dikirim, kunci sementara dienkripsi menggunakan RSA dengan public key penerima:
     ```python
     encrypted_key = rsa_encrypt(recipient_public_key, des_key)
     ```

3. **Penggunaan**:
   - Kunci sementara ini digunakan oleh algoritma DES untuk mengenkripsi pesan:
     ```python
     encrypted_message = des_encrypt(message, des_key)
     ```

4. **Dekripsi**:
   - Penerima mendekripsi kunci sementara menggunakan private key RSA miliknya:
     ```python
     des_key = rsa_decrypt(private_key, encrypted_key)
     ```

---

## **3. Proses Komunikasi Lengkap**

### **Pengiriman Pesan**
1. Pengirim membuat **kunci sementara** (DES Key).
2. Kunci sementara dienkripsi menggunakan RSA dengan public key penerima.
3. Pesan dienkripsi menggunakan DES dengan kunci sementara.
4. Pesan (dan kunci sementara yang telah dienkripsi) dikirim ke server.

### **Penerimaan Pesan**
1. Penerima menerima pesan dari server.
2. Penerima mendekripsi kunci sementara menggunakan private key RSA miliknya.
3. Pesan dienkripsi dengan DES menggunakan kunci sementara.

---

## **4. Teknologi yang Digunakan**
- **RSA (Asimetris)**:
  - Enkripsi dan dekripsi menggunakan fungsi:
    - `rsa_encrypt(public_key, plaintext)`
    - `rsa_decrypt(private_key, ciphertext)`
  - Implementasi ada di file `rsa.py`.

- **DES (Simetris)**:
  - Enkripsi dan dekripsi menggunakan fungsi:
    - `des_encrypt(plaintext, des_key)`
    - `des_decrypt(ciphertext, des_key)`
  - Implementasi sederhana ada di file `des/des.py`.

- **Public Key Authority (PKA)**:
  - Penyimpanan kunci publik RSA untuk setiap pengguna.
  - Implementasi ada di file `pka.py`.

- **Server**:
  - Mengelola komunikasi antar pengguna.
  - Implementasi ada di file `server.py`.

- **Client**:
  - Mengirim dan menerima pesan aman.
  - Implementasi ada di file `client.py`.

---

## **5. Diagram Alur**
```plaintext
+--------+           +---------+            +---------+           +--------+
| Sender |  --RSA--> |   PKA   |   --RSA--> | Receiver | <--DES--- | Sender |
+--------+           +---------+            +---------+           +--------+
```
1. Pengirim meminta kunci publik penerima dari PKA.
2. Pengirim mengenkripsi kunci sementara dengan RSA menggunakan kunci publik penerima.
3. Pesan dienkripsi menggunakan DES dengan kunci sementara.
4. Penerima mendekripsi kunci sementara dengan private key RSA miliknya.
5. Penerima mendekripsi pesan dengan kunci sementara.
