import json
import os
from datetime import datetime, timedelta
import cv2
import numpy as np
import qrcode
from PIL import Image
import streamlit as st

# Sayfa Yapılandırması (Mobil uyumlu genişlik)
st.set_page_config(
    page_title="SKT & Envanter Takip", page_icon="📦", layout="centered"
)

# --- VERİ YÖNETİMİ (Kalıcılık için JSON Dosyası) ---
DATA_FILE = "envanter_data.json"


def veri_yukle():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
  return []


def veri_kaydet(veri):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=4)


# Kapsamlı ve Zengin Akıllı İkon Belirleme Fonksiyonu
def akilli_ikon_bul(urun_adi):
  adi = urun_adi.lower()

  # Süt ve Süt Ürünleri
  if any(x in adi for x in ["süt", "ayran", "kefir"]):
    return "🥛"
  elif any(x in adi for x in ["peynir", "kaşar", "lor", "labne", "mörver"]):
    return "🧀"
  elif any(x in adi for x in ["tereyağ", "margarin"]):
    return "🧈"
  elif any(x in adi for x in ["yoğurt", "süzme"]):
    return "🥣"
  elif any(x in adi for x in ["krema", "kaymak"]):
    return "🍦"

  # Et, Tavuk ve Deniz Ürünleri
  elif any(
      x in adi for x in ["et", "kırmızı et", "kıyma", "biftek", "pirzola", "kuşbaşı"]
  ):
    return "🥩"
  elif any(x in adi for x in ["tavuk", "piliç", "göğüs", "but", "kanat"]):
    return "🍗"
  elif any(x in adi for x in ["balık", "somon", "levrek", "ton balığı", "hamsi"]):
    return "🐟"
  elif any(x in adi for x in ["sucuk", "salam", "sosis", "pastırma", "jambon"]):
    return "🥓"

  # Meyveler
  elif any(x in adi for x in ["elma"]):
    return "🍎"
  elif any(x in adi for x in ["muz"]):
    return "🍌"
  elif any(x in adi for x in ["portakal", "mandalina", "greyfurt"]):
    return "🍊"
  elif any(x in adi for x in ["limon"]):
    return "🍋"
  elif any(x in adi for x in ["çilek"]):
    return "🍓"
  elif any(x in adi for x in ["karpuz"]):
    return "🍉"
  elif any(x in adi for x in ["kavun"]):
    return "🍈"
  elif any(x in adi for x in ["üzüm"]):
    return "🍇"
  elif any(x in adi for x in ["şeftali", "kayısı", "erik"]):
    return "🍑"
  elif any(x in adi for x in ["kiraz", "vişne"]):
    return "🍒"
  elif any(x in adi for x in ["ananas"]):
    return "🍍"
  elif any(x in adi for x in ["kivi"]):
    return "🥝"
  elif any(x in adi for x in ["avokado"]):
    return "🥑"

  # Sebzeler ve Yeşillikler
  elif any(x in adi for x in ["domates"]):
    return "🍅"
  elif any(x in adi for x in ["patates"]):
    return "🥔"
  elif any(x in adi for x in ["biber"]):
    return "🫑"
  elif any(x in adi for x in ["soğan", "sarımsak"]):
    return "🧅"
  elif any(x in adi for x in ["salatalık"]):
    return "🥒"
  elif any(x in adi for x in ["havuç"]):
    return "🥕"
  elif any(x in adi for x in ["marul", "salata", "yeşillik", "maydanoz", "dereotu", "roka"]):
    return "🥬"
  elif any(x in adi for x in ["lahana", "brokoli", "karnabahar"]):
    return "🥦"
  elif any(x in adi for x in ["patlıcan"]):
    return "🍆"
  elif any(x in adi for x in ["mantar"]):
    return "🍄"
  elif any(x in adi for x in ["mısır"]):
    return "🌽"
  elif any(x in adi for x in ["bezelye", "fasulye", "mercimek", "nohut", "bakliyat"]):
    return "🫘"

  # Fırın ve Unlu Mamuller
  elif any(x in adi for x in ["ekmek", "somun", "tost ekmeği"]):
    return "🍞"
  elif any(x in adi for x in ["simit", "açma", "poğaça", "börek", "çörek"]):
    return "🥐"
  elif any(x in adi for x in ["pasta", "kek", "kurabiye", "tatlı"]):
    return "🎂"
  elif any(x in adi for x in ["un", "nişasta", "irmik"]):
    return "🌾"
  elif any(x in adi for x in ["makarna", "erişte", "şehriye"]):
    return "🍝"
  elif any(x in adi for x in ["pirinç", "bulgur", "pirinç"]):
    return "🍚"

  # Kahvaltılık ve Diğer Gıdalar
  elif any(x in adi for x in ["yumurta"]):
    return "🥚"
  elif any(x in adi for x in ["zeytin"]):
    return "🫒"
  elif any(x in adi for x in ["reçel", "bal", "çikolata kreması", "nutella", "fıstık ezmesi"]):
    return "🍯"
  elif any(x in adi for x in ["yağ", "zeytinyağı", "ayçiçek yağı"]):
    return "🍾"
  elif any(x in adi for x in ["tuz", "şeker", "baharat", "karabiber", "pul biber"]):
    return "🧂"
  elif any(x in adi for x in ["salça", "sos", "ketçap", "mayonez", "hardal"]):
    return "🥫"

  # İçecekler
  elif any(x in adi for x in ["su", "maden suyu", "soda"]):
    return "💧"
  elif any(x in adi for x in ["kola", "fanta", "gazoz", "ice tea", "enerji içeceği"]):
    return "🥤"
  elif any(x in adi for x in ["meyve suyu", "nektar"]):
    return "🧃"
  elif any(x in adi for x in ["çay", "kahve", "türkkahvesi", "nescafe"]):
    return "☕"
  elif any(x in adi for x in ["bira", "şarap", "rakı", "alkol"]):
    return "🍺"

  # Atıştırmalıklar
  elif any(x in adi for x in ["çikolata", "gofret", "bar"]):
    return "🍫"
  elif any(x in adi for x in ["cips", "kraker", "patlamış mısır"]):
    return "🍿"
  elif any(x in adi for x in ["sakız", "şekerleme", "bonibon"]):
    return "🍬"
  elif any(x in adi for x in ["fındık", "fıstık", "ceviz", "badem", "kuru yemiş"]):
    return "🥜"

  # Temizlik ve Ev İhtiyaçları
  elif any(x in adi for x in ["deterjan", "çamaşır suyu", "yumuşatıcı", "temizlik"]):
    return "🧼"
  elif any(x in adi for x in ["tuvalet kağıdı", "peçete", "havlu kağıt"]):
    return "🧻"
  elif any(x in adi for x in ["şampuan", "sabun", "duş jeli", "diş macunu"]):
    return "🧴"
  elif any(x in adi for x in ["çöp torbası", "poşet", "folyo", "streç"]):
    return "🛍️"

  else:
    return "📦"


# Session State Başlatma
if "envanter" not in st.session_state:
  st.session_state.envanter = veri_yukle()

if "dolaplar" not in st.session_state:
  st.session_state.dolaplar = ["Ana Buzdolabı", "Kiler", "Derin Dondurucu"]

# --- ÖZEL CSS (Tasarımdaki Renk Paleti ve Modern Kartlar) ---
st.markdown(
    """
    <style>
    .main { background-color: #f4f7f6; }
    .product-card {
        background-color: white;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-left: 5px solid #2b8a3e;
    }
    .badge-critical { background-color: #ffe3e3; color: #c92a2a; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 12px;}
    .badge-warning { background-color: #fff3bf; color: #f08c00; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 12px;}
    .badge-safe { background-color: #ebfbee; color: #2b8a3e; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 12px;}
    .badge-estimated { background-color: #e7f5ff; color: #1864ab; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- ÜST BAŞLIK & DURUM ÖZETİ ---
st.markdown("### 🏠 SKT & Envanter Takip")

# İstatistikler
toplam_urun = len(st.session_state.envanter)
bugun = datetime.now().date()
kritik_sayisi = 0

for item in st.session_state.envanter:
  skt_tarihi = datetime.strptime(item["skt"], "%Y-%m-%d").date()
  kalan_gun = (skt_tarihi - bugun).days
  if kalan_gun <= 2:
    kritik_sayisi += 1

col1, col2 = st.columns(2)
with col1:
  st.metric(label="📦 Toplam Ürün", value=toplam_urun)
with col2:
  st.metric(
      label="⚠️ Kritik / Yaklaşan",
      value=kritik_sayisi,
      delta_color="inverse",
  )

st.divider()

# --- MENÜ YAPISI ---
menu = st.selectbox(
    "Menü Seçimi",
    [
        "📦 Stok Listesi",
        "➕ Ürün Ekle",
        "📷 QR Oku / Üret",
        "🧊 Dolaplarım",
        "⚙️ Ayarlar",
    ],
    label_visibility="collapsed",
)

# ================= 1. STOK LİSTESİ =================
if menu == "📦 Stok Listesi":
  st.subheader("📋 Ürün Listesi")

  arama = st.text_input("🔍 Ürün Ara...", placeholder="Ürün adı yazın...")

  if not st.session_state.envanter:
    st.info(
        "Henüz eklenmiş bir ürün yok. 'Ürün Ekle' sekmesinden ekleyebilirsin."
    )
  else:
    for i, item in enumerate(st.session_state.envanter):
      if arama and arama.lower() not in item["ad"].lower():
        continue

      skt_tarihi = datetime.strptime(item["skt"], "%Y-%m-%d").date()
      kalan_gun = (skt_tarihi - bugun).days

      if item.get("paketsiz", False):
        badge = (
            f'<span class="badge-estimated">Tahmini: {kalan_gun} Gün</span>'
        )
      else:
        if kalan_gun < 0:
          badge = '<span class="badge-critical">SÜRESİ GEÇTİ!</span>'
        elif kalan_gun <= 2:
          badge = (
              f'<span class="badge-critical">Kritik: {kalan_gun} Gün</span>'
          )
        elif kalan_gun <= 5:
          badge = (
              f'<span class="badge-warning">Yaklaşıyor: {kalan_gun} Gün</span>'
          )
        else:
          badge = f'<span class="badge-safe">Taze: {kalan_gun} Gün</span>'

      tahmini_etiket = (
          " <i style='font-size:11px; color:#1864ab;'>(Açık Ürün)</i>"
          if item.get("paketsiz", False)
          else ""
      )

      st.markdown(
          f"""
            <div class="product-card">
                <div>
                    <h4 style="margin:0; color:#333;">{item.get('ikon', '📦')} {item['ad']} {tahmini_etiket}</h4>
                    <p style="margin:4px 0 0 0; color: #666; font-size: 13px;">Dolap: <b>{item.get('dolap', 'Genel')}</b> | Miktar: <b>{item.get('miktar', '1 Adet')}</b></p>
                    <p style="margin:2px 0 0 0; color: #444; font-size: 12px;">SKT: {item['skt']}</p>
                </div>
                <div>
                    {badge}
                </div>
            </div>
            """,
          unsafe_allow_html=True,
      )

      if st.button("🗑️ Sil", key=f"sil_{i}2"):
        st.session_state.envanter.pop(i)
        veri_kaydet(st.session_state.envanter)
        st.rerun()

# ================= 2. ÜRÜN EKLE =================
elif menu == "➕ Ürün Ekle":
  st.subheader("➕ Yeni Ürün Ekle")

  with st.form("urun_ekle_form", clear_on_submit=True):
    urun_adi = st.text_input("Ürün Adı (Örn: Muz, Süt, Deterjan)")
    secilen_dolap = st.selectbox(
        "Hangi Dolaba Eklenecek?", st.session_state.dolaplar
    )
    miktar = st.text_input("Miktar (Örn: 1 Kilo, 1 Litre, 3 Adet)")

    paketsiz_mi = st.checkbox(
        "Paketsiz / Açık Ürün (Akıllı Tahmini SKT Uygula)"
    )

    kategori = st.selectbox(
        "Gıda Kategorisi (Tahmin için)",
        [
            "Sebze / Meyve (Ort. 5 gün)",
            "Et / Tavuk / Balık (Ort. 3 gün)",
            "Süt Ürünü / Açık Peynir (Ort. 7 gün)",
            "Fırın / Unlu Mamul (Ort. 4 gün)",
            "Diğer / Genel",
        ],
    )

    varsayilan_gun = 7
    if paketsiz_mi:
      if "Sebze" in kategori:
        varsayilan_gun = 5
      elif "Et" in kategori:
        varsayilan_gun = 3
      elif "Süt" in kategori:
        varsayilan_gun = 7
      elif "Fırın" in kategori:
        varsayilan_gun = 4

      tahmini_skt = bugun + timedelta(days=varsayilan_gun)
      skt_tarihi = st.date_input("Son Tüketim Tarihi", value=tahmini_skt)
    else:
      skt_tarihi = st.date_input(
          "Son Tüketim Tarihi", value=bugun + timedelta(days=30)
      )

    submit = st.form_submit_button("Ürünü Kaydet")

    if submit and urun_adi:
      otomatik_ikon = akilli_ikon_bul(urun_adi)
      yeni_urun = {
          "ad": urun_adi,
          "dolap": secilen_dolap,
          "miktar": miktar if miktar else "1 Adet",
          "skt": str(skt_tarihi),
          "paketsiz": paketsiz_mi,
          "ikon": otomatik_ikon,
      }
      st.session_state.envanter.append(yeni_urun)
      veri_kaydet(st.session_state.envanter)
      st.success(
          f"🎉 '{urun_adi}' ({otomatik_ikon}) başarıyla stoğa eklendi!"
      )

# ================= 3. QR OKU / ÜRET =================
elif menu == "📷 QR Oku / Üret":
  st.subheader("📷 QR İşlemleri & Miktar Girişi")

  tab_okur, tab_uret = st.tabs(["QR Oku (Arka Kamera)", "QR Oluştur"])

  with tab_okur:
    st.write(
        "Kamerayı ürüne tutarak hızlı tarama yapabilirsiniz (Arka kamera"
        " aktif)."
    )
    kamera_resmi = st.camera_input(
        "Kamera Görüntüsü Al", label_visibility="collapsed"
    )

    if kamera_resmi is not None:
      bytes_data = kamera_resmi.getvalue()
      np_arr = np.frombuffer(bytes_data, np.uint8)
      img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

      detector = cv2.QRCodeDetector()
      data, bbox, _ = detector.detectAndDecode(img)

      if data:
        st.success(f"🎉 QR Kod Okundu: **{data}**")
        q_ekle = st.text_input("Miktar Belirle", value="1 Adet", key="qr_miktar")
        if st.button("Okunan Ürünü Stoğa Ekle"):
          otomatik_ikon = akilli_ikon_bul(data)
          st.session_state.envanter.append({
              "ad": data,
              "dolap": "Ana Buzdolabı",
              "miktar": q_ekle,
              "skt": str(bugun + timedelta(days=10)),
              "paketsiz": False,
              "ikon": otomatik_ikon,
          })
          veri_kaydet(st.session_state.envanter)
          st.success("Stoka eklendi!")
      else:
        st.warning(
            "Fotoğrafta net bir QR kod algılanamadı. Lütfen tekrar deneyin."
        )

  with tab_uret:
    st.write("Ürünleriniz için hızlıca QR kod oluşturun.")
    qr_metin = st.text_input("QR Kod İçin Ürün Bilgisi / Adı")
    qr_miktar = st.text_input(
        "Miktar Bilgisi (QR içine eklenecek)", value="1 Adet"
    )

    if qr_metin:
      tam_veri = f"{qr_metin} - Miktar: {qr_miktar}"
      img = qrcode.make(tam_veri)
      img.save("qr_temp.png")
      st.image("qr_temp.png", caption=f"QR Kod: {tam_veri}", width=200)

# ================= 4. DOLAPLARIM =================
elif menu == "🧊 Dolaplarım":
  st.subheader("🧊 Dolap Yönetimi")

  st.write("Kayıtlı Dolaplarınız:")
  for dolap in st.session_state.dolaplar:
    st.markdown(f"- 🗄️ **{dolap}**")

  st.divider()
  st.write("➕ **Yeni Dolap Ekle**")

  if "yeni_dolap_input" not in st.session_state:
    st.session_state.yeni_dolap_input = ""

  yeni_dolap_adi = st.text_input(
      "Dolap Adı",
      value=st.session_state.yeni_dolap_input,
      placeholder="Örn: Ofis Buzdolabı",
      key="dolap_input_field",
  )

  if st.button("Dolabı Kaydet"):
    if yeni_dolap_adi and yeni_dolap_adi not in st.session_state.dolaplar:
      st.session_state.dolaplar.append(yeni_dolap_adi)
      st.success(f"'{yeni_dolap_adi}' başarıyla eklendi!")
      st.session_state.yeni_dolap_input = ""
      st.rerun()

# ================= 5. AYARLAR =================
elif menu == "⚙️ Ayarlar":
  st.subheader("⚙️ Uygulama Ayarları")
  st.write("Veri yönetimi ve sıfırlama seçenekleri:")

  if st.button("🗑️ Tüm Verileri Sıfırla"):
    st.session_state.envanter = []
    if os.path.exists(DATA_FILE):
      os.remove(DATA_FILE)
    st.success("Tüm veriler temizlendi.")
    st.rerun()