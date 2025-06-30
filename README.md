# convert_mikrotik_queue_to_env_hosts.py

**scripted by rskabc**

Skrip ini digunakan untuk mengonversi konfigurasi *simple queue* Mikrotik (file `.rsc`) menjadi dua file output:
- `.env` — berisi daftar target dalam format variabel lingkungan (environment variable)
- `hosts` — berisi daftar nama host dan alamat IP untuk keperluan SSH atau inventory Ansible

---

## 🛠️ Kebutuhan

- Python 3.x
- File konfigurasi Mikrotik hasil ekspor, misalnya: `queue_export.rsc`

---

## 🚀 Cara Penggunaan

```bash
python3 convert_mikrotik_queue_to_env_hosts.py <input_file.rsc>
