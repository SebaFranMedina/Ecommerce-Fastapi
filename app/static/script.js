console.log("JS cargado correctamente ✅");

window.addEventListener("DOMContentLoaded", () => {
    const backgrounds = [
        "/static/img/logo/asd/1.webp",
        "/static/img/logo/asd/2.webp",
        "/static/img/logo/asd/3.webp", 
        "/static/img/logo/asd/5.webp"
    ];

    // Pre-cargar y verificar qué imágenes existen
    const existingBackgrounds = [];
    
    function preloadImages() {
        const promises = backgrounds.map(url => {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(url);
                img.onerror = () => resolve(null);
                img.src = url;
            });
        });

        Promise.all(promises).then(results => {
            existingBackgrounds.push(...results.filter(url => url !== null));
            console.log(`✅ Imágenes disponibles: ${existingBackgrounds.length}`);
            
            if (existingBackgrounds.length === 0) {
                console.warn("No hay imágenes de fondo disponibles");
                useColorBackgrounds();
            } else {
                startBackgroundRotation();
            }
        });
    }

    let bgIndex = 0;
    const body = document.body;

    function startBackgroundRotation() {
        // Establecer fondo inicial
        changeToBackground(0);
        
        // Rotar cada 3 segundos
        setInterval(() => {
            bgIndex = (bgIndex + 1) % existingBackgrounds.length;
            changeToBackground(bgIndex);
        }, 3000);
    }

    function changeToBackground(index) {
        if (existingBackgrounds.length === 0) return;
        
        const imageUrl = existingBackgrounds[index];
        const angle = 120 + (index * 20);
        body.style.backgroundImage = `
            linear-gradient(${angle}deg, rgba(31,41,55,0.85), rgba(17,24,39,0.85)),
            url('${imageUrl}')
        `;
    }

    function useColorBackgrounds() {
        const colors = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
        ];

        let colorIndex = 0;
        
        function changeColor() {
            body.style.backgroundImage = colors[colorIndex];
            colorIndex = (colorIndex + 1) % colors.length;
        }

        changeColor();
        setInterval(changeColor, 3000);
    }

    // INICIAR
    body.style.transition = "background-image 1s ease-in-out";
    preloadImages();

    // -----------------------------
    // Funcionalidad de tablas (mantener igual)
    // -----------------------------
    const lista = document.getElementById("lista-desplegada");
    if (lista) {
        document.querySelectorAll(".btn-tabla").forEach(btn => {
            btn.addEventListener("click", () => {
                const tablaId = btn.getAttribute("data-tabla");

                if (lista.dataset.abierta === tablaId) {
                    lista.classList.remove("open");
                    lista.dataset.abierta = "";
                    return;
                }

                fetch(`/tabla/${tablaId}`)
                    .then(resp => resp.json())
                    .then(data => {
                        lista.innerHTML = "";
                        if (!data || data.length === 0) {
                            lista.innerHTML = "<li>No hay productos</li>";
                        } else {
                            data.forEach(i => {
                                const li = document.createElement("li");
                                li.textContent = `${i.id} - ${i.valor}`;
                                lista.appendChild(li);
                            });
                        }

                        lista.classList.add("open");
                        lista.dataset.abierta = tablaId;

                        const countSpan = btn.querySelector(".count");
                        if (countSpan) countSpan.textContent = data.length;
                    })
                    .catch(err => {
                        lista.innerHTML = "<li>Error al cargar los datos</li>";
                        lista.classList.add("open");
                        console.error(err);
                    });
            });
        }); 
    }
});