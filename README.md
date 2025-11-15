# Tugas Besar IF2224 Teori Bahasa Formal dan Otomata 2025/2026
Tugas ini mengeksplorasi implementasi dari compiler bahasa pemrograman Pascal-S. Pascal-S adalah varian subset dari bahasa pemrograman Pascal yang disederhanakan untuk tujuan edukasi dalam pembuatan sistem kompilasi. Tujuan utama dari proyek ini adalah untuk membangun sebuah compiler fungsional yang dapat menerjemahkan kode sumber Pascal-S. Proses pengembangan kompilator ini dibagi menjadi beberapa tahapan utama yang akan dikerjakan secara bertahap
1. Lexical Analysis (Lexer): Tahap awal yang berfungsi mengubah kumpulan karakter mentah dari kode sumber menjadi unit-unit bermakna yang disebut token. Tahap ini diimplementasikan menggunakan Deterministic Finite Automaton (DFA) untuk mengenali pola leksikal bahasa.
2. Syntax Analysis (Parser): Memeriksa rangkaian token untuk memastikan kesesuaiannya dengan struktur dan tata bahasa (aturan gramatikal) dari bahasa Pascal-S.
3. Semantic Analysis: Melakukan pemeriksaan semantik untuk memastikan konsistensi makna dan aturan dalam program.
4. Intermediate Code Generation: Menghasilkan representasi kode tingkat rendah yang independen dari mesin.
5. Interpreter: Mengeksekusi kode perantara yang telah dihasilkan.

# Identitas Kelompok
### Kelompok LPH K-01
| NIM        | Nama |
|------------|-------|
| 13523023   | Muhammad Aufa Farabi |
| 13523025   | Joel Hotlan Haris Siahaan |
| 13523051   | Ferdinand Gabe Tua Sinaga |
| 13523111   | Muhammad Iqbal Haidar |

# Requirements
1. Perangkat telah terinstall python
2. File yang berisi kode program Pascal-S

# Cara Instalasi dan Penggunaan Program
1. Clone repository ini ke perangkat lokal
```
git clone https://github.com/jhotlann/LPH-Tubes-IF2224.git
```
2. Arahkan ke direktori proyek
  ```
cd path/to/folder
```
3. Jalankan dengan command
```
python3 {path/to/src/compiler.py} {path/to/source_code.pas}
```
Contoh:
```
python3 src/compiler.py test/milestone-2/test1.pas
```

# Pembagian Tugas
| NIM        | Milestone 1 | Milestone 2 | Milestone 3 | Milestone 4 | Milestone 5 |
|------------|-------------|-------------|-------------|-------------|-------------|
| 13523023   | 25% | 25% |  |  |  |
| 13523025   | 25% | 25% |  |  |  |
| 13523051   | 25% | 25% |  |  |  |
| 13523111   | 25% | 25% |  |  |  |
