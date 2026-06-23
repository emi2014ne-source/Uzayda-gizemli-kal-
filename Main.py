import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🚀 3D Uzay Simülasyonu")
st.write("Kaptan, hoş geldin! Fareyle (mouse) ekranı döndürebilir, tekerlekle yakınlaşabilirsin.")

# HTML ve Three.js ile 3D Uzay Sahnesi Oluşturma
three_js_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; }
        canvas { width: 100vw; height: 70vh; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <script>
        // 1. Sahne, Kamera ve Render Ayarları
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // 2. Işıklandırma
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(10, 10, 10);
        scene.add(pointLight);

        // 3. Uzay Gemisi (Ortadaki Büyük Küp)
        const shipGeometry = new THREE.BoxGeometry(2, 1, 3);
        const shipMaterial = new THREE.MeshStandardMaterial({ color: 0x00ffcc, wireframe: false });
        const ship = new THREE.Mesh(shipGeometry, shipMaterial);
        scene.add(ship);

        // 4. Meteorlar (Etraftaki Rastgele Küçük Küpler)
        const asteroids = [];
        for(let i = 0; i < 50; i++) {
            const size = Math.random() * 0.5 + 0.1;
            const astGeometry = new THREE.BoxGeometry(size, size, size);
            const astMaterial = new THREE.MeshStandardMaterial({ color: 0x888888 });
            const asteroid = new THREE.Mesh(astGeometry, astMaterial);
            
            // Rastgele pozisyonlar
            asteroid.position.set(
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 40
            );
            scene.add(asteroid);
            asteroids.push(asteroid);
        }

        camera.position.z = 10;
        camera.position.y = 5;
        camera.lookAt(ship.position);

        // 5. Klavye Kontrolleri (Gemi Hareketi)
        document.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowUp') ship.position.z -= 0.5;
            if (event.key === 'ArrowDown') ship.position.z += 0.5;
            if (event.key === 'ArrowLeft') ship.position.x -= 0.5;
            if (event.key === 'ArrowRight') ship.position.x += 0.5;
        });

        // 6. Animasyon Döngüsü (Sürekli Çalışır)
        function animate() {
            requestAnimationFrame(animate);

            // Gemi kendi etrafında hafifçe dönsün
            ship.rotation.y += 0.01;

            // Meteorları hareket ettir
            asteroids.forEach(ast => {
                ast.rotation.x += 0.01;
                ast.rotation.y += 0.02;
            });

            renderer.render(scene, camera);
        }
        animate();

        // Pencere boyutu değiştiğinde ekranı ayarla
        window.addEventListener('resize', onWindowResize, false);
        function onWindowResize(){
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }
    </script>
</body>
</html>
"""

# HTML kodunu Streamlit sayfasına gömüyoruz
components.html(three_js_code, height=600)

st.info("💡 İpucu: Bilgisayardan giriyorsan yön tuşlarıyla ortadaki gemiyi hareket ettirebilirsin!")

