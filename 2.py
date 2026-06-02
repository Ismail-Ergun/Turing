class TuringMakinesi:
    def __init__(self, plaka):
        # Girdiyi banda yerleştir ve sonuna boşluk sembolü ekle
        self.bant = list(plaka) + ['_']
        self.kafa = 0
        self.durum = 'q0'
        self.gecis_tablosu = self._gecis_tablosunu_olustur()
        
    def _gecis_tablosunu_olustur(self):
        tablo = {}
        rakamlar = [str(i) for i in range(10)]
        harfler = [chr(i) for i in range(65, 91)]
        
        # q0 -> ilk rakam
        for r in rakamlar: tablo[('q0', r)] = ('q1', r, 'R')
        # q1 -> ikinci rakam
        for r in rakamlar: tablo[('q1', r)] = ('q2', r, 'R')
        # q2 -> ilk harf
        for h in harfler: tablo[('q2', h)] = ('q3', h, 'R')
        # q3 -> ikinci harf
        for h in harfler: tablo[('q3', h)] = ('q4', h, 'R')
        # q4 -> ilk rakam
        for r in rakamlar: tablo[('q4', r)] = ('q5', r, 'R')
        # q5 -> ikinci rakam
        for r in rakamlar: tablo[('q5', r)] = ('q6', r, 'R')
        # q6 -> üçüncü rakam
        for r in rakamlar: tablo[('q6', r)] = ('q7', r, 'R')
        
        # q7 -> kabul durumu (7 karakterden sonra boşluk gelmeli)
        tablo[('q7', '_')] = ('q_kabul', '_', 'R')
        
        return tablo

    def calistir(self):
        print(f"\n--- İncelenen Plaka: {''.join(self.bant[:-1])} ---")
        
        while self.durum not in ['q_kabul', 'q_red']:
            okunan_sembol = self.bant[self.kafa]
            mevcut_durum = self.durum
            
            anahtar = (mevcut_durum, okunan_sembol)
            
            if anahtar in self.gecis_tablosu:
                yeni_durum, yazilan_sembol, yon = self.gecis_tablosu[anahtar]
                self.bant[self.kafa] = yazilan_sembol
                self.durum = yeni_durum
                
                # Kafa hareketi
                if yon == 'R':
                    self.kafa += 1
                elif yon == 'L':
                    self.kafa -= 1
                    
                print(f"Mevcut Durum: {mevcut_durum} | Okunan: {okunan_sembol} | Yeni Durum: {yeni_durum} | Hareket: {yon} | Bant: {''.join(self.bant)}")
            else:
                self.durum = 'q_red'
                print(f"Mevcut Durum: {mevcut_durum} | Okunan: {okunan_sembol} -> HATA (Bilinmeyen Geçiş)")
                
        if self.durum == 'q_kabul':
            print("Sonuç: KABUL")
        else:
            print("Sonuç: RED")

# Kullanıcıdan plaka bilgisini alma
if __name__ == "__main__":
    girdi = input("Lütfen plaka bilgisini giriniz: ")
    tm = TuringMakinesi(girdi)
    tm.calistir()