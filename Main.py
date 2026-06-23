import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🚀 3D Uzay Savaşı - Mobil Sürüm")
st.write("Kaptan, ekranın altındaki butonları kullanarak gemiyi yönet ve meteorları vur!")

# HTML, Three.js ve Dokunmatik Kontroller
three_js_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: sans-serif; }
        canvas { width: 100vw; height: 60vh; display: block; }
        
        /* Mobil Kontrol Butonları Alanı */
        .controls {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
            width: 90%;
            max-width: 400px;
            justify-content: center;
            z-index: 100;
        }
        .btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid #fff;
            color: #fff;
            padding: 15px 25px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
        }
        .btn:active {
            background: rgba(255, 255, 255, 0.5);
        }
        .btn-fire {
            background: rgba(255, 0, 0, 0.6);
            border-color: #ff0000;
            flex-grow: 1;
        }
        .btn-fire:active {
            background: rgba(255, 0, 0, 0.9);
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div class="controls">
        <button class="btn" id="leftBtn">◀ SOL</button>
        <button class="btn btn-fire" id="fireBtn">🔥 ATEŞ</button>
        <button class="btn" id="rightBtn">SAĞ ▶</button>
    </div>

    <script>
        // Sahne Kurulumu
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / (window.innerHeight * 0.6), 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight * 0.6);
        document.body.appendChild(renderer.domElement);

        // Işıklar
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(10, 10, 10);
        scene.add(pointLight);

        // Uzay Gemisi
        const shipGeometry = new THREE.BoxGeometry(1.5, 0.5, 2.5);
        const shipMaterial = new THREE.MeshStandardMaterial({ color: 0x00ffcc });
        const ship = new THREE.Mesh(shipGeometry, shipMaterial);
        scene.add(ship);

        // Lazerler ve Meteor Dizileri
        const lasers = [];
        const asteroids = [];

        // Meteor Oluşturma
        for(let i = 0; i < 30; i++) {
            const size = Math.random() * 0.6 + 0.2;
            const astGeometry = new THREE.BoxGeometry(size, size, size);
            const astMaterial = new THREE.MeshStandardMaterial({ color: 0x888888 });
            const asteroid = new THREE.Mesh(astGeometry, astMaterial);
            
            asteroid.position.set(
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 5,
                -Math.random() * 40 - 5 // Geminin ilerisine koyuyoruz
            );
            scene.add(asteroid);
            asteroids.push(asteroid);
        }

        camera.position.set(0, 4, 7);
        camera.lookAt(0, 0, -5);

        // Ateş Etme Fonksiyonu
        function fireLaser() {
            const laserGeometry = new THREE.CylinderGeometry(0.05, 0.05, 1, 8);
            const laserMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
            const laser = new THREE.Mesh(laserGeometry, laserMaterial);
            
            // Lazeri yatay yapıp geminin önüne koyuyoruz
            laser.rotation.x = Math.PI / 2;
            laser.position.set(ship.position.x, ship.position.y, ship.position.z - 1.5);
            
            scene.add(laser);
            lasers.push(laser);
        }

        // Dokunmatik Buton Dinleyicileri
        document.getElementById('leftBtn').addEventListener('touchstart', (e) => { e.preventDefault(); ship.position.x -= 0.6; });
        document.getElementById('rightBtn').addEventListener('touchstart', (e) => { e.preventDefault(); ship.position.x += 0.6; });
        document.getElementById('fireBtn').addEventListener('touchstart', (e) => { e.preventDefault(); fireLaser(); });
        
        // Tıklama desteği (Bilgisayar testi için)
        document.getElementById('leftBtn').addEventListener('click', () => ship.position.x -= 0.6);
        document.getElementById('rightBtn').addEventListener('click', () => ship.position.x += 0.6);
        document.getElementById('fireBtn').addEventListener('click', fireLaser);

        // Oyun Döngüsü
        function animate() {
            requestAnimationFrame(animate);

            // Lazerleri İleri Yürüt ve Çarpışma Kontrolü Yap
            for(let i = lasers.length - 1; i >= 0; i--) {
                lasers[i].position.z -= 0.5;

                // Ekrandan çıkan lazeri sil
                if(lasers[i].position.z < -50) {
                    scene.remove(lasers[i]);
                    lasers.splice(i, 1);
                    continue;
                }

                // Meteorlarla çarpışma testi
                for(let j = asteroids.length - 1; j >= 0; j--) {
                    if(lasers[i] && lasers[i].position.distanceTo(asteroids[j].position) < 1.2) {
                        // Çarpışma var! Meteoru patlat (rastgele yere ışınla)
                        asteroids[j].position.set(
                            (Math.random() - 0.5) * 20,
                            (Math.random() - 0.5) * 5,
                            -Math.random() * 40 - 5
                        );
                        scene.remove(lasers[i]);
                        lasers.splice(i, 1);
                        break;
                    }
                }
            }

            // Meteorları hafifçe döndür ve gemiye doğru yaklaştır
            asteroids.forEach(ast => {
                ast.rotation.x += 0.01;
                ast.rotation.y += 0.01;
                ast.position.z += 0.05; // Meteorlar gemiye doğru akıyor
                
                // Gemi arkasına geçen meteoru tekrar öne at
                if(ast.position.z > 10) {
                    ast.position.z = -40;
                }
            });

            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / (window.innerHeight * 0.6);
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight * 0.6);
        });
    </script>
</body>
</html>
"""

components.html(three_js_code, height=650)


