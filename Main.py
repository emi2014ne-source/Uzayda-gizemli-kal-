import streamlit as st
import streamlit.components.v1 as components

# --- 🌍 WEB SAYFASI AYARLARI ---
st.set_page_config(page_title="Uzayda Gizemli Kalış", page_icon="🚀", layout="wide")

# --- 🎨 MODERN BİLİM KURGU / MODERN WAR TEMALI TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #e2e8f0; }
    div.stButton > button:first-child {
        background-color: #ff4b4b; color: white; font-size: 22px;
        font-weight: bold; border-radius: 12px; width: 100%; height: 55px;
        box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4);
    }
    .status-box {
        padding: 20px; border-radius: 12px; background-color: #1e293b;
        border: 2px solid #38bdf8; margin-bottom: 20px;
        box-shadow: 0px 4px 20px rgba(56, 189, 248, 0.15);
    }
    .battle-box {
        padding: 20px; border-radius: 12px; background-color: #1c1917;
        border: 2px solid #ef4444; margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 💾 TARAYICI HAFIZASI (OYUN DURUMLARI) ---
if "oyun_basladi" not in st.session_state:
    st.session_state.oyun_basladi = False
if "oyuncu_adi" not in st.session_state:
    st.session_state.oyuncu_adi = ""
if "oyuncu_kodu" not in st.session_state:
    st.session_state.oyuncu_kodu = ""
if "is_yapimci" not in st.session_state:
    st.session_state.is_yapimci = False

if "lobi_takim" not in st.session_state:
    st.session_state.lobi_takim = {} 
if "altin" not in st.session_state:
    st.session_state.altin = 1500
if "zaman" not in st.session_state:
    st.session_state.zaman = "GÜNDÜZ"
if "aktif_oda" not in st.session_state:
    st.session_state.aktif_oda = "KOKPİT"
if "ust_mesaj" not in st.session_state:
    st.session_state.ust_mesaj = ""

if "aktif_zirh" not in st.session_state:
    st.session_state.aktif_zirh = "Başlangıç Üniforması"
if "defans_orani" not in st.session_state:
    st.session_state.defans_orani = 0.0
if "kiralik_adamlar" not in st.session_state:
    st.session_state.kiralik_adamlar = [] 

if "fusuy_can" not in st.session_state:
    st.session_state.fusuy_can = 150
if "buyucu_can" not in st.session_state:
    st.session_state.buyucu_can = 200
if "puyye_can" not in st.session_state:
    st.session_state.puyye_can = 100
if "minyon_sayisi" not in st.session_state:
    st.session_state.minyon_sayisi = 0

# --- 🚪 1. EKRAN: GİRİŞ & "BAŞLA" EKRANI ---
if not st.session_state.oyun_basladi:
    st.title("🚀 UZAYDA GİZEMLİ KALIŞ")
    st.subheader("Modern Çok Oyunculu Strateji & Hayatta Kalma Oyunu")
    st.image("https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800", caption="Uzay istasyonunda gizemli bir mahsur kalış hikayesi...")
    
    st.markdown("### 🧑‍🚀 Karakter Kayıt Paneli")
    ad_input = st.text_input("Kullanıcı Adınız:", key="g_ad")
    kod_input = st.text_input("Kendinize Özel Arkadaş Kodu Belirleyin (Örn: Efe123):", key="g_kod")
    
    st.markdown("---")
    if st.button("🎮 OYUNA BAŞLA"):
        if ad_input.strip() and kod_input.strip():
            st.session_state.oyuncu_adi = ad_input.strip()
            st.session_state.oyuncu_kodu = kod_input.strip()
            st.session_state.lobi_takim[kod_input.strip()] = ad_input.strip()
            st.session_state.oyun_basladi = True
            
            if ad_input.upper() in ["YAPIMCI", "KAPTAN", "GELİSTİRİCİ"] or kod_input.upper() == "YAPIMCI":
                st.session_state.is_yapimci = True
            st.rerun()
        else:
            st.error("Lütfen Kullanıcı Adı ve Arkadaş Kodu alanlarını boş bırakmayın!")

# --- 🎮 2. EKRAN: ANA OYUN WEB PANELİ ---
else:
    takim_sayisi = len(st.session_state.lobi_takim)
    takim_maks_can = takim_sayisi * 100
    if "takim_can" not in st.session_state or st.session_state.takim_can > takim_maks_can:
        st.session_state.takim_can = takim_maks_can

    rütbe = "👑 YAPIMCI" if st.session_state.is_yapimci else "🧑‍🚀 OYUNCU"
    st.title("🚀 Uzayda Gizemli Kalış")
    
    st.markdown(f"**❤️ TAKIM HP BEKASI: {st.session_state.takim_can} / {takim_maks_can}**")
    st.progress(max(0, min(1.0, st.session_state.takim_can / takim_maks_can)))

    takim_isimleri = ", ".join(list(st.session_state.lobi_takim.values()))
    zaman_sembol = "☀️ GÜNDÜZ" if st.session_state.zaman == "GÜNDÜZ" else "🌙 GECE SAVAŞI"
    
    st.markdown(f"""
    <div class="status-box">
        <h4 style='color: #38bdf8;'>📍 Mevcut Oda: {st.session_state.aktif_oda} | 🕒 Döngü: {zaman_sembol}</h4>
        <p><b>Mevcut Rol:</b> {rütbe} ({st.session_state.oyuncu_adi}) | 🔑 <b>Kodun:</b> {st.session_state.oyuncu_kodu}</p>
        <p>💰 <b>KASA ALTIN:</b> {st.session_state.altin} Gold | 🛡️ <b>Zırh Defansı:</b> %{int(st.session_state.defans_orani * 100)}</p>
        <p style='color: #a78bfa;'>👥 <b>TAKIM LOBİSİ ({takim_sayisi}/5):</b> [{takim_isimleri}]</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.ust_mesaj:
        st.info(st.session_state.ust_mesaj)

    # 👑 YAPIMCI GÜÇLERİ PANELİ
    if st.session_state.is_yapimci:
        with st.expander("✨ YAPIMCI ÖZEL PANELİ (DEVELOPER MODU)", expanded=True):
            col_yap1, col_yap2 = st.columns(2)
            with col_yap1:
                if st.button("🔮 Sınırsız Hile: +50K Altın & Canı Fulle"):
                    st.session_state.altin += 50000
                    st.session_state.takim_can = takim_maks_can
                    st.session_state.ust_mesaj = "⚡ YAPIMCI GÜCÜ: Hesap bütçesi uçuruldu, can fullendi!"
                    st.rerun()
            with col_yap2:
                if st.session_state.zaman == "GECE":
                    if st.button("🔥 YAPIMCI ÖFKESİ (Kötülere -100 Hasar)"):
                        st.session_state.fusuy_can -= 100
                        st.session_state.buyucu_can -= 100
                        st.session_state.puyye_can -= 100
                        st.session_state.ust_mesaj = "⚡ YAPIMCI ETKİSİ: Gece ekibi çökertildi!"
                        st.rerun()

    # --- ⚔️ GECE SAVAŞI DÖNGÜSÜ (3D AKSİYONLU) ---
    if st.session_state.zaman == "GECE":
        if st.session_state.takim_can <= 0:
            st.error("💀 TAKIMINIZ ELENDİ! Gece ortaya çıkan kötülere karşı koyamadınız.")
            if st.button("Yeniden Başla (Lobiyi Sıfırla)"):
                st.session_state.clear()
                st.rerun()
        
        elif st.session_state.fusuy_can <= 0 and st.session_state.buyucu_can <= 0 and st.session_state.puyye_can <= 0:
            st.balloons()
            st.success("🏆 MUHTEŞEM ZAFER! Takımınız Fusuy, Büyücü ve Püyye'yi bozguna uğrattı! (+1500 Altın Ödül)")
            st.session_state.altin += 1500
            st.session_state.zaman = "GÜNDÜZ"
            st.session_state.aktif_oda = "KOKPİT"
            st.session_state.fusuy_can = 150
            st.session_state.buyucu_can = 200
            st.session_state.puyye_can = 100
            st.session_state.minyon_sayisi = 0
            st.session_state.ust_mesaj = "☀️ Sabah oldu, yaratıklar temizlendi."
            st.rerun()
            
        else:
            st.markdown("<div class='battle-box'><h3>🌙 GECE EKİBİ SALDIRIDA!</h3>", unsafe_allow_html=True)
            col_hp1, col_hp2, col_hp3 = st.columns(3)
            with col_hp1: st.metric("👑 FUSUY CAN", f"{max(0, st.session_state.fusuy_can)} HP")
            with col_hp2: st.metric("🔮 BÜYÜCÜ CAN", f"{max(0, st.session_state.buyucu_can)} HP", f"Minyon: {st.session_state.minyon_sayisi}")
            with col_hp3: st.metric("🏹 PÜYYE CAN", f"{max(0, st.session_state.puyye_can)} HP")
            st.markdown("</div>", unsafe_allow_html=True)
            
            temel_hasar = 20 * takim_sayisi
            for adam in st.session_state.kiralik_adamlar:
                temel_hasar += 15 if adam == "Eyüki" else 40

            st.markdown("### 🎮 3D SAVAŞ ARENASI (Düşman Gemilerini Avla!)")
            defans_katpayi = max(1, int(15 * (1 - st.session_state.defans_orani) / takim_sayisi))

            # --- DÜŞMANLI THREE.JS SAVAŞ ARENASI KODU ---
            war_js = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { margin: 0; overflow: hidden; background: #000; font-family: sans-serif; }
                    canvas { width: 100vw; height: 45vh; display: block; }
                    .controls { display: flex; gap: 15px; justify-content: center; padding: 15px; background: #111; }
                    .btn { background: #222; color: #fff; border: 2px solid #444; padding: 15px 25px; font-size: 18px; font-weight: bold; border-radius: 10px; }
                    .btn-fire { background: #ff4b4b; border-color: #ff0000; }
                </style>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            </head>
            <body>
                <div id="game"></div>
                <div class="controls">
                    <button class="btn" id="l">◀ SOL</button>
                    <button class="btn btn-fire" id="f">🔥 ATEŞ</button>
                    <button class="btn" id="r">SAĞ ▶</button>
                </div>
                <script>
                    const scene = new THREE.Scene();
                    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / (window.innerHeight * 0.45), 0.1, 1000);
                    const renderer = new THREE.WebGLRenderer({ antialias: true });
                    renderer.setSize(window.innerWidth, window.innerHeight * 0.45);
                    document.getElementById('game').appendChild(renderer.domElement);

                    scene.add(new THREE.AmbientLight(0xffffff, 0.8));

                    // Oyuncu Gemisi (Turkuaz)
                    const ship = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.4, 1.8), new THREE.MeshStandardMaterial({ color: 0x00ffcc }));
                    ship.position.set(0, 0, 4); scene.add(ship);

                    // KÖTÜLER (Fusuy, Büyücü, Püyye)
                    const fusuy = new THREE.Mesh(new THREE.ConeGeometry(0.8, 1.6, 4), new THREE.MeshStandardMaterial({ color: 0xffd700 }));
                    fusuy.position.set(-3, 0, -6); fusuy.rotation.x = Math.PI; scene.add(fusuy);
                    
                    const buyucu = new THREE.Mesh(new THREE.SphereGeometry(0.7, 8, 8), new THREE.MeshStandardMaterial({ color: 0x9400d3 }));
                    buyucu.position.set(0, 0, -7); scene.add(buyucu);

                    const puyye = new THREE.Mesh(new THREE.ConeGeometry(0.6, 1.4, 4), new THREE.MeshStandardMaterial({ color: 0x1e90ff }));
                    puyye.position.set(3, 0, -6); puyye.rotation.x = Math.PI; scene.add(puyye);

                    camera.position.set(0, 4, 8); camera.lookAt(0, 0, -1);

                    const lasers = [];
                    function fire() {
                        const laser = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.9), new THREE.MeshBasicMaterial({ color: 0xff0000 }));
                        laser.rotation.x = Math.PI / 2;
                        laser.position.set(ship.position.x, 0, ship.position.z - 1);
                        scene.add(laser); lasers.push(laser);
                    }

                    document.getElementById('l').onclick = () => { if(ship.position.x > -5) ship.position.x -= 1; };
                    document.getElementById('r').onclick = () => { if(ship.position.x < 5) ship.position.x += 1; };
                    document.getElementById('f').onclick = fire;

                    function animate() {
                        requestAnimationFrame(animate);
                        fusuy.rotation.y += 0.02;
                        buyucu.position.y = Math.sin(Date.now() * 0.004) * 0.4;
                        puyye.rotation.y -= 0.02;

                        for(let i=lasers.length-1; i>=0; i--) {
                            lasers[i].position.z -= 0.5;
                            if(lasers[i].position.z < -15) { scene.remove(lasers[i]); lasers.splice(i,1); }
                        }
                        renderer.render(scene, camera);
                    }
                    animate();
                </script>
            </body>
            </html>
            """
            components.html(war_js, height=400)

            # --- Manuel Tıklama ve Senkronizasyon Butonları ---
            st.markdown("### ⚔️ Savaş Komutları")
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.session_state.fusuy_can > 0 and st.button("🗡️ Fusuy'a Atak Yap"):
                    st.session_state.fusuy_can -= temel_hasar
                    st.session_state.takim_can -= defans_katpayi
                    st.session_state.ust_mesaj = f"Fusuy'a vuruldu! Takım {defans_katpayi} hasar aldı."
                    st.rerun()
            with col_b2:
                if st.session_state.buyucu_can > 0 and st.button("🔮 Büyücü'ye Atak Yap"):
                    st.session_state.buyucu_can -= temel_hasar
                    st.session_state.minyon_sayisi += 1
                    st.session_state.takim_can -= (defans_katpayi + 2)
                    st.session_state.ust_mesaj = f"Büyücü alan patlaması yaptı ve minyon çıkardı!"
                    st.rerun()
            with col_b3:
                if st.session_state.puyye_can > 0 and st.button("🏹 Püyye'ye Atak Yap"):
                    st.session_state.puyye_can -= temel_hasar
                    st.session_state.takim_can -= max(1, defans_katpayi - 2)
                    st.session_state.ust_mesaj = "Püyye uzaktan ok yağdırdı!"
                    st.rerun()
                    
            if st.session_state.minyon_sayisi > 0:
                if st.button(f"🧹 Sahadaki Minyonları Temizle ({st.session_state.minyon_sayisi})"):
                    st.session_state.minyon_sayisi = 0
                    st.session_state.ust_mesaj = "Minyonlar temizlendi!"
                    st.rerun()
                    
            if st.button("☀️ Savunmaya Geç ve Sabahı Bekle"):
                st.session_state.zaman = "GÜNDÜZ"
                st.session_state.aktif_oda = "KOKPİT"
                st.session_state.fusuy_can = 150
                st.session_state.buyucu_can = 200
                st.session_state.puyye_can = 100
                st.session_state.minyon_sayisi = 0
                st.session_state.ust_mesaj = "Güneş doğdu! Canavarlar çekildi."
                st.rerun()

    # --- ☀️ GÜNDÜZ OPERASYONLARI (KOKPİT & MARKETLER) ---
    else:
        if st.session_state.aktif_oda == "KOKPİT":
            st.markdown("### 🗺️ Gemi Operasyon Paneli")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                if st.button("🛒 Zırh Marketine Giriş Yap"):
                    st.session_state.aktif_oda = "ZIRH_MARKET"
                    st.rerun()
                if st.button("🤝 Tüccar Marketi (Savaşçı Kirala)"):
                    st.session_state.aktif_oda = "TUCCAR_MARKET"
                    st.rerun()
                    
            with col_m2:
                st.markdown("**👥 Çoklu Oyuncu Lobi Daveti**")
                ark_kod_girdi = st.text_input("Arkadaşının Kodunu Yaz:", placeholder="Örn: Ahmet456")
                if st.button("➕ Takıma Davet Et"):
                    if ark_kod_girdi.strip():
                        if len(st.session_state.lobi_takim) < 5:
                            kod_temiz = ark_kod_girdi.strip()
                            st.session_state.lobi_takim[kod_temiz] = f"Oyuncu_{kod_temiz}"
                            st.session_state.ust_mesaj = f"✅ {kod_temiz} kodlu arkadaş lobiye eklendi!"
                            st.rerun()
                        else:
                            st.error("Takım dolu!")

            st.markdown("---")
            if st.button("🌙 ZAMANI İLERLET (GECEYİ BAŞLAT)"):
                st.session_state.zaman = "GECE"
                st.session_state.ust_mesaj = "⚠️ Dikkat! İstasyon karardı, gece yaratıkları sahaya indi!"
                st.rerun()

        # Zırh Marketi
        elif st.session_state.aktif_oda == "ZIRH_MARKET":
            st.markdown("### 🛒 Gemi Teknoloji ve Zırh Marketi")
            zirhlar = {
                "Büyücü Zırhı": (500, 0.10),
                "Metal Zırh": (1000, 0.20),
                "Çelik Zırh": (1500, 0.35),
                "Adamantin Zırh": (2500, 0.50),
                "Yuso Zırhı": (3500, 0.90)
            }
            for isim, (fiyat, koruma) in zirhlar.items():
                if st.button(f"🛡️ {isim} (%{int(koruma*100)} Koruma) - [{fiyat} Altın]"):
                    if st.session_state.altin >= fiyat:
                        st.session_state.altin -= fiyat
                        st.session_state.aktif_zirh = isim
                        st.session_state.defans_orani = koruma
                        st.session_state.ust_mesaj = f"Başarıyla {isim} kuşanıldı!"
                        st.rerun()
                    else:
                        st.error("Yetersiz altın bütçesi!")
                        
            if st.button("↩️ Kokpite Geri Dön"):
                st.session_state.aktif_oda = "KOKPİT"
                st.rerun()

        # Tüccar Marketi
        elif st.session_state.aktif_oda == "TUCCAR_MARKET":
            st.markdown("### 🤝 Tüccar Güvenlik Teşkilatı (Kiralık Savaşçılar)")
            st.write(f"**Aktif Ordunuzun Mevcudu:** {len(st.session_state.kiralik_adamlar)} / 3")
            
            if st.button("👥 Eyüki Kirala (Metal Kılıçlı, +15 Hasar Desteği) [-2000 Altın]"):
                if len(st.session_state.kiralik_adamlar) < 3:
                    if st.session_state.altin >= 2000:
                        st.session_state.altin -= 2000
                        st.session_state.kiralik_adamlar.append("Eyüki")
                        st.session_state.ust_mesaj = "Eyüki orduya katıldı!"
                        st.rerun()
                    else:
                        st.error("Yetersiz altın!")
                else:
                    st.error("Maksimum 3 koruma kiralayabilirsin!")
                    
            if st.button("👑 Yusfi Kirala (Fusuy Setli, +40 Ağır Hasar Desteği) [-5900 Altın]"):
                if len(st.session_state.kiralik_adamlar) < 3:
                    if st.session_state.altin >= 5900:
                        st.session_state.altin -= 5900
                        st.session_state.kiralik_adamlar.append("Yusfi")
                        st.session_state.ust_mesaj = "Efsanevi Yusfi saflara katıldı!"
                        st.rerun()
                    else:
                        st.error("Yetersiz altın!")
                else:
                    st.error("Maksimum 3 koruma kiralayabilirsin!")
                    
            if st.button("↩️ Kokpite Geri Dön"):
                st.session_state.aktif_oda = "KOKPİT"
                st.rerun()

    st.markdown("---")
    if st.button("🚨 Oturumu Kapat / Ana Menüye Dön"):
        st.session_state.clear()
        st.rerun()



