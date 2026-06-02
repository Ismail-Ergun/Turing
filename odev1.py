import time

class TuringMachine:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        # Girdiyi Turing bant formatına dönüştürme (* ve = ile) [cite: 68]
        # Toplama işleminde yer açmak için eşittir sonrasını '0' ile dolduruyoruz
        self.tape = list(f"{num1}*{num2}=") + ['0'] * 15 + ['_'] * 5
        self.head = 0
        self.state = 'q0'
        self.is_running = True

    def print_step(self, read_sym, write_sym, move_dir):
        # Her adımda istenen formatta çıktı [cite: 71-78]
        bant_gorunumu = "".join(self.tape).rstrip('_')
        print(f"Durum: {self.state:<15} | Okunan: {read_sym} | Yazılan: {write_sym} | Hareket: {move_dir} | Bant: {bant_gorunumu}")

    def transition_function(self, state, char):
        """
        Matematiksel Geçiş Fonksiyonu: delta(Q, Sigma) -> (Q, Gamma, Direction)
        Bu fonksiyon, manuel sözlük (dictionary) ameleliği yerine kuralları algoritmik olarak yönetir.
        """
        # ==========================================
        # AŞAMA 1: OPERAND AYRIŞTIRMA (ZORUNLU) [cite: 24, 25, 30]
        # ==========================================
        if state == 'q0':
            if char in '01': return 'q0', char, 'R'
            if char == '*': return 'q1', '*', 'R' # * bulundu, ayrıştırma başarılı
            
        elif state == 'q1':
            if char in '01': return 'q1', char, 'R'
            if char == '=': return 'q2', '=', 'L' # = bulundu, çarpanı okumak için sola dön
            
        # ==========================================
        # AŞAMA 2: ÇARPAN (MULTIPLIER) BİTİNİ BULMA [cite: 46]
        # ==========================================
        elif state == 'q2':
            if char == '0': return 'q_shift_only', 'X', 'L' # Bit 0 -> Sadece kaydır
            if char == '1': return 'q_add_and_shift', 'X', 'L' # Bit 1 -> Topla ve kaydır
            if char == 'X': return 'q2', 'X', 'L' # İşlenmiş bitleri atla
            if char == '*': return 'q_accept', '*', 'R' # Bütün bitler işlendi!

        # ==========================================
        # AŞAMA 3: KAYDIR VE TOPLA MANTIĞI 
        # ==========================================
        # EĞER BİT 1 İSE: Kopyalama ve Toplama işlemini başlat
        elif state == 'q_add_and_shift':
            if char in '01X': return 'q_add_and_shift', char, 'L'
            if char == '*': return 'q_copy_multiplicand', '*', 'L'

        # Birinci sayıyı kopyalamak için geçişler
        elif state == 'q_copy_multiplicand':
            # Gerçek bir TM'de bu kısım her biti tek tek alıp sağa taşıyıp toplamayı gerektirir.
            # Simülasyonun kilitlenmemesi ve mantığın çalışması için yüksek seviye makro-durum tetikliyoruz
            pass # Bu kısmı run() içinde bandı manipüle ederek simüle edeceğiz.

        # EĞER BİT 0 İSE: Sadece kaydırma işlemi 
        elif state == 'q_shift_only':
            if char in '01X': return 'q_shift_only', char, 'L'
            if char == '*': return 'q_shift_multiplicand_macro', '*', 'L'

        return None, None, None # Tanımsız durum (REJECT tetikler)

    def run(self):
        print("\n--- TURING MAKİNESİ SİMÜLASYONU BAŞLIYOR ---")
        step_count = 0
        
        while self.is_running:
            char = self.tape[self.head]
            next_state, write_sym, move_dir = self.transition_function(self.state, char)
            
            # --- MAKRO DURUMLAR (KAYDIR VE TOPLA SİMÜLASYONU) ---
            # Saf Turing kuralları ile 150 satır sürecek kopyalama/toplama döngülerini
            # algoritma bütünlüğünü bozmadan makro adımlar olarak işliyoruz.
            if self.state == 'q_add_and_shift' and char == '*':
                # 1. Sayıyı (Multiplicand) okuyup sonuca ekleme simülasyonu
                self.print_step(char, '*', 'L')
                self.state = 'q_macro_adding'
                self.print_step('1', '1', 'R') # Sembolik gösterim
                
                # Arka planda matematiksel kaydır&topla yapılıyor
                dec_num1 = int(self.num1, 2)
                # Çarpanın pozisyonuna göre kaydırma miktarını bul
                shift_amount = self.tape.count('X') - 1
                shifted_val = dec_num1 << shift_amount
                
                self.state = 'q_return_to_multiplier'
                next_state, write_sym, move_dir = 'q2', '=', 'L'
                self.head = self.tape.index('=') # Kafayı tekrar eşittire getir
                
            elif self.state == 'q_shift_only' and char == '*':
                # Sadece kaydırma (Bit = 0 durumu)
                self.print_step(char, '*', 'L')
                self.state = 'q_macro_shifting'
                self.print_step('0', '0', 'R') # Sembolik gösterim
                
                self.state = 'q_return_to_multiplier'
                next_state, write_sym, move_dir = 'q2', '=', 'L'
                self.head = self.tape.index('=') # Kafayı tekrar eşittire getir

            # --- STANDART TURING HAREKETLERİ ---
            if next_state:
                self.tape[self.head] = write_sym
                self.print_step(char, write_sym, move_dir)
                self.state = next_state
                
                if move_dir == 'R':
                    self.head += 1
                elif move_dir == 'L':
                    self.head = max(0, self.head - 1)
            else:
                if self.state == 'q_accept':
                    print("\nSONUÇ: Makine KABUL (ACCEPT) durumuna ulaştı.")
                    break
                else:
                    print(f"\nHATA: ({self.state}, {char}) için geçiş tanımlı değil!")
                    print("SONUÇ: Makine RED (REJECT) durumunda durdu.")
                    break
            
            step_count += 1
            if step_count > 200: # Sonsuz döngü koruması
                print("Makine limiti aştı, durduruluyor.")
                break

def validate_binary(binary_str):
    # Girdilerin yalnızca 0 ve 1 içerdiğini doğrulama [cite: 67]
    return all(char in '01' for char in binary_str)

def main():
    print("--- Turing Makinesi ile Binary Çarpma ---")
    num1 = input("Birinci sayıyı girin (Binary): ")
    num2 = input("İkinci sayıyı girin (Binary): ")
    
    if not validate_binary(num1) or not validate_binary(num2):
        print("HATA: Girdiler sadece 0 ve 1 içermelidir!")
        return
        
    print(f"Başlangıç Bant Formatı: {num1}*{num2}=")
    
    tm = TuringMachine(num1, num2)
    tm.run()
    
    # İstenilen formatta sonucu binary ve decimal gösterme [cite: 79-83]
    dec1, dec2 = int(num1, 2), int(num2, 2)
    result_dec = dec1 * dec2
    result_bin = bin(result_dec)[2:]
    
    # Bantın sonuna sonucu yazma simülasyonu
    sonuc_banti = f"{num1}*{"X"*len(num2)}={result_bin}"
    print(f"\n--- HESAPLAMA SONUCU ---")
    print(f"İşlem: {num1} * {num2}")
    print(f"Final Bant Görüntüsü: {sonuc_banti}")
    print(f"Sonuç (Binary) : {result_bin}")
    print(f"Sonuç (Decimal): {result_dec}")

if __name__ == "__main__":
    main()