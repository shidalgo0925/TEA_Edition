// Actividades Interactivas para TEA Edition
// Este archivo contiene todas las funciones JavaScript para las actividades

console.log('🎯 Archivo actividades_interactivas.js cargado correctamente');

let actividadId = null;
let tiempoInicio = null;

function mostrarActividad(categoria) {
    console.log('🎮 Función mostrarActividad llamada con categoría:', categoria);
    if (categoria === 'lenguaje') {
        abrirActividadLenguaje();
    } else if (categoria === 'numeros') {
        abrirActividadNumeros();
    } else if (categoria === 'colores') {
        abrirActividadColores();
    } else if (categoria === 'animales') {
        abrirActividadAnimales();
    } else {
        abrirActividadGenerica();
    }
}

function abrirActividadLenguaje() {
    console.log('🗣️ Abriendo actividad de lenguaje');
    const preguntas = [
        { palabra: 'GATO', pregunta: '¿Cuál es el sonido que hace este animal?', opciones: ['miau', 'guau', 'muu'], correcta: 'miau' },
        { palabra: 'PERRO', pregunta: '¿Cuál es el sonido que hace este animal?', opciones: ['guau', 'miau', 'muu'], correcta: 'guau' },
        { palabra: 'VACA', pregunta: '¿Cuál es el sonido que hace este animal?', opciones: ['muu', 'miau', 'guau'], correcta: 'muu' }
    ];
    
    const pregunta = preguntas[Math.floor(Math.random() * preguntas.length)];
    
    // Crear HTML completo como string
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Actividad de Lenguaje</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 20px; 
                    background: #f0f8ff; 
                    margin: 0;
                }
                .actividad { 
                    text-align: center; 
                    margin-top: 50px; 
                }
                .palabra { 
                    font-size: 3rem; 
                    color: #E74C3C; 
                    margin: 20px 0; 
                    font-weight: bold;
                }
                .opciones { 
                    display: flex; 
                    gap: 20px; 
                    justify-content: center; 
                    margin: 30px 0; 
                    flex-wrap: wrap;
                }
                .opcion { 
                    padding: 15px 30px; 
                    background: #3498DB; 
                    color: white; 
                    border: none; 
                    border-radius: 10px; 
                    cursor: pointer; 
                    font-size: 1.2rem;
                    transition: background 0.3s;
                }
                .opcion:hover { 
                    background: #2980B9; 
                }
                .pregunta {
                    font-size: 1.3rem;
                    margin: 20px 0;
                    color: #2C3E50;
                }
            </style>
        </head>
        <body>
            <div class="actividad">
                <h1>🗣️ Actividad de Lenguaje</h1>
                <div class="palabra">${pregunta.palabra}</div>
                <div class="pregunta">${pregunta.pregunta}</div>
                <div class="opciones">
                    <button class="opcion" onclick="responder('${pregunta.opciones[0]}')">${pregunta.opciones[0].toUpperCase()}</button>
                    <button class="opcion" onclick="responder('${pregunta.opciones[1]}')">${pregunta.opciones[1].toUpperCase()}</button>
                    <button class="opcion" onclick="responder('${pregunta.opciones[2]}')">${pregunta.opciones[2].toUpperCase()}</button>
                </div>
            </div>
            <script>
                function responder(respuesta) {
                    console.log("Respuesta recibida:", respuesta);
                    if (respuesta === '${pregunta.correcta}') {
                        alert("¡Correcto! 🎉 ¡Muy bien!");
                        window.close();
                    } else {
                        alert("Inténtalo de nuevo 😊 ¡Piensa bien!");
                    }
                }
            </script>
        </body>
        </html>
    `;
    
    // Abrir ventana y escribir contenido
    const ventana = window.open('', '_blank', 'width=800,height=600,scrollbars=yes,resizable=yes');
    if (ventana) {
        ventana.document.open();
        ventana.document.write(htmlContent);
        ventana.document.close();
        console.log('✅ Ventana de actividad abierta correctamente');
    } else {
        alert('Por favor, permite ventanas emergentes para esta actividad');
        console.log('❌ No se pudo abrir ventana emergente');
    }
}

function abrirActividadNumeros() {
    console.log('🔢 Abriendo actividad de números');
    const preguntas = [
        { numero: 5, pregunta: '¿Cuántos dedos tienes en una mano?', opciones: [5, 3, 7], correcta: 5 },
        { numero: 10, pregunta: '¿Cuántos dedos tienes en total?', opciones: [10, 8, 12], correcta: 10 },
        { numero: 2, pregunta: '¿Cuántos ojos tienes?', opciones: [2, 1, 3], correcta: 2 }
    ];
    
    const pregunta = preguntas[Math.floor(Math.random() * preguntas.length)];
    
    // Crear HTML completo como string
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Actividad de Números</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 20px; 
                    background: #f0f8ff; 
                    margin: 0;
                }
                .actividad { 
                    text-align: center; 
                    margin-top: 50px; 
                }
                .numero { 
                    font-size: 4rem; 
                    color: #E74C3C; 
                    margin: 20px 0; 
                    font-weight: bold;
                }
                .opciones { 
                    display: flex; 
                    gap: 20px; 
                    justify-content: center; 
                    margin: 30px 0; 
                    flex-wrap: wrap;
                }
                .opcion { 
                    padding: 15px 30px; 
                    background: #3498DB; 
                    color: white; 
                    border: none; 
                    border-radius: 10px; 
                    cursor: pointer; 
                    font-size: 1.2rem;
                    transition: background 0.3s;
                }
                .opcion:hover { 
                    background: #2980B9; 
                }
                .pregunta {
                    font-size: 1.3rem;
                    margin: 20px 0;
                    color: #2C3E50;
                }
            </style>
        </head>
        <body>
            <div class="actividad">
                <h1>🔢 Actividad de Números</h1>
                <div class="numero">${pregunta.numero}</div>
                <div class="pregunta">${pregunta.pregunta}</div>
                <div class="opciones">
                    <button class="opcion" onclick="responder(${pregunta.opciones[0]})">${pregunta.opciones[0]}</button>
                    <button class="opcion" onclick="responder(${pregunta.opciones[1]})">${pregunta.opciones[1]}</button>
                    <button class="opcion" onclick="responder(${pregunta.opciones[2]})">${pregunta.opciones[2]}</button>
                </div>
            </div>
            <script>
                function responder(respuesta) {
                    console.log("Respuesta recibida:", respuesta, "Tipo:", typeof respuesta);
                    if (respuesta === ${pregunta.correcta}) {
                        alert("¡Correcto! 🎉 ¡Muy bien!");
                        window.close();
                    } else {
                        alert("Inténtalo de nuevo 😊 ¡Piensa bien!");
                    }
                }
            </script>
        </body>
        </html>
    `;
    
    // Abrir ventana y escribir contenido
    const ventana = window.open('', '_blank', 'width=800,height=600,scrollbars=yes,resizable=yes');
    if (ventana) {
        ventana.document.open();
        ventana.document.write(htmlContent);
        ventana.document.close();
        console.log('✅ Ventana de actividad de números abierta correctamente');
    } else {
        alert('Por favor, permite ventanas emergentes para esta actividad');
        console.log('❌ No se pudo abrir ventana emergente');
    }
}

function abrirActividadColores() {
    console.log('🎨 Abriendo actividad de colores');
    const preguntas = [
        { color: 'red', pregunta: '¿De qué color es este cuadrado?', opciones: ['rojo', 'azul', 'verde'], correcta: 'rojo' },
        { color: 'blue', pregunta: '¿De qué color es este cuadrado?', opciones: ['azul', 'rojo', 'verde'], correcta: 'azul' },
        { color: 'green', pregunta: '¿De qué color es este cuadrado?', opciones: ['verde', 'rojo', 'azul'], correcta: 'verde' }
    ];
    
    const pregunta = preguntas[Math.floor(Math.random() * preguntas.length)];
    
    // Crear HTML completo como string
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Actividad de Colores</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 20px; 
                    background: #f0f8ff; 
                    margin: 0;
                }
                .actividad { 
                    text-align: center; 
                    margin-top: 50px; 
                }
                .color-cuadrado { 
                    width: 150px; 
                    height: 150px; 
                    background-color: ${pregunta.color}; 
                    margin: 20px auto; 
                    border: 3px solid #2C3E50;
                    border-radius: 10px;
                }
                .opciones { 
                    display: flex; 
                    gap: 20px; 
                    justify-content: center; 
                    margin: 30px 0; 
                    flex-wrap: wrap;
                }
                .opcion { 
                    padding: 15px 30px; 
                    background: #3498DB; 
                    color: white; 
                    border: none; 
                    border-radius: 10px; 
                    cursor: pointer; 
                    font-size: 1.2rem;
                    transition: background 0.3s;
                }
                .opcion:hover { 
                    background: #2980B9; 
                }
                .pregunta {
                    font-size: 1.3rem;
                    margin: 20px 0;
                    color: #2C3E50;
                }
            </style>
        </head>
        <body>
            <div class="actividad">
                <h1>🎨 Actividad de Colores</h1>
                <div class="color-cuadrado"></div>
                <div class="pregunta">${pregunta.pregunta}</div>
                <div class="opciones">
                    <button class="opcion" onclick="responder('${pregunta.opciones[0]}')">${pregunta.opciones[0].toUpperCase()}</button>
                    <button class="opcion" onclick="responder('${pregunta.opciones[1]}')">${pregunta.opciones[1].toUpperCase()}</button>
                    <button class="opcion" onclick="responder('${pregunta.opciones[2]}')">${pregunta.opciones[2].toUpperCase()}</button>
                </div>
            </div>
            <script>
                function responder(respuesta) {
                    console.log("Respuesta recibida:", respuesta);
                    if (respuesta === '${pregunta.correcta}') {
                        alert("¡Correcto! 🎉 ¡Muy bien!");
                        window.close();
                    } else {
                        alert("Inténtalo de nuevo 😊 ¡Piensa bien!");
                    }
                }
            </script>
        </body>
        </html>
    `;
    
    // Abrir ventana y escribir contenido
    const ventana = window.open('', '_blank', 'width=800,height=600,scrollbars=yes,resizable=yes');
    if (ventana) {
        ventana.document.open();
        ventana.document.write(htmlContent);
        ventana.document.close();
        console.log('✅ Ventana de actividad de colores abierta correctamente');
    } else {
        alert('Por favor, permite ventanas emergentes para esta actividad');
        console.log('❌ No se pudo abrir ventana emergente');
    }
}

function abrirActividadAnimales() {
    console.log('🐶 Abriendo actividad de animales');
    const preguntas = [
        { emoji: '🐕', pregunta: '¿Qué animal es este?', opciones: ['perro', 'gato', 'pájaro'], correcta: 'perro' },
        { emoji: '🐱', pregunta: '¿Qué animal es este?', opciones: ['gato', 'perro', 'conejo'], correcta: 'gato' },
        { emoji: '🐰', pregunta: '¿Qué animal es este?', opciones: ['conejo', 'ratón', 'gato'], correcta: 'conejo' }
    ];
    
    const pregunta = preguntas[Math.floor(Math.random() * preguntas.length)];
    
    // Crear HTML completo como string
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Actividad de Animales</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 20px; 
                    background: #f0f8ff; 
                    margin: 0;
                }
                .actividad { 
                    text-align: center; 
                    margin-top: 50px; 
                }
                .animal-emoji { 
                    font-size: 6rem; 
                    margin: 20px 0; 
                }
                .opciones { 
                    display: flex; 
                    gap: 20px; 
                    justify-content: center; 
                    margin: 30px 0; 
                    flex-wrap: wrap;
                }
                .opcion { 
                    padding: 15px 30px; 
                    background: #3498DB; 
                    color: white; 
                    border: none; 
                    border-radius: 10px; 
                    cursor: pointer; 
                    font-size: 1.2rem;
                    transition: background 0.3s;
                }
                .opcion:hover { 
                    background: #2980B9; 
                }
                .pregunta {
                    font-size: 1.3rem;
                    margin: 20px 0;
                    color: #2C3E50;
                }
            </style>
        </head>
        <body>
            <div class="actividad">
                <h1>🐶 Actividad de Animales</h1>
                <div class="animal-emoji">${pregunta.emoji}</div>
                <div class="pregunta">${pregunta.pregunta}</div>
                <div class="opciones">
                    <button class="opcion" onclick="responder('${pregunta.opciones[0]}')">${pregunta.opciones[0].toUpperCase()}</button>
                    <button class="opcion" onclick="responder('${pregunta.opciones[1]}')">${pregunta.opciones[1].toUpperCase()}</button>
                    <button class="opcion" onclick="responder('${pregunta.opciones[2]}')">${pregunta.opciones[2].toUpperCase()}</button>
                </div>
            </div>
            <script>
                function responder(respuesta) {
                    console.log("Respuesta recibida:", respuesta);
                    if (respuesta === '${pregunta.correcta}') {
                        alert("¡Correcto! 🎉 ¡Muy bien!");
                        window.close();
                    } else {
                        alert("Inténtalo de nuevo 😊 ¡Piensa bien!");
                    }
                }
            </script>
        </body>
        </html>
    `;
    
    // Abrir ventana y escribir contenido
    const ventana = window.open('', '_blank', 'width=800,height=600,scrollbars=yes,resizable=yes');
    if (ventana) {
        ventana.document.open();
        ventana.document.write(htmlContent);
        ventana.document.close();
        console.log('✅ Ventana de actividad de animales abierta correctamente');
    } else {
        alert('Por favor, permite ventanas emergentes para esta actividad');
        console.log('❌ No se pudo abrir ventana emergente');
    }
}

function abrirActividadGenerica() {
    console.log('🎯 Abriendo actividad genérica');
    // Crear HTML completo como string
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Actividad de Aprendizaje</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 20px; 
                    background: #f0f8ff; 
                    margin: 0;
                }
                .actividad { 
                    text-align: center; 
                    margin-top: 50px; 
                }
                .mensaje {
                    font-size: 1.5rem;
                    color: #2C3E50;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="actividad">
                <h1>🎯 Actividad de Aprendizaje</h1>
                <div class="mensaje">¡Próximamente más actividades divertidas!</div>
            </div>
        </body>
        </html>
    `;
    
    // Abrir ventana y escribir contenido
    const ventana = window.open('', '_blank', 'width=800,height=600,scrollbars=yes,resizable=yes');
    if (ventana) {
        ventana.document.open();
        ventana.document.write(htmlContent);
        ventana.document.close();
        console.log('✅ Ventana de actividad genérica abierta correctamente');
    } else {
        alert('Por favor, permite ventanas emergentes para esta actividad');
        console.log('❌ No se pudo abrir ventana emergente');
    }
}

function verInstrucciones() {
    alert('Instrucciones:\n\n1. Lee la pregunta o instrucción\n2. Selecciona la respuesta correcta\n3. ¡Diviértete aprendiendo!');
}

// Función para inicializar la actividad
function inicializarActividad(id, categoria) {
    console.log('🚀 Inicializando actividad:', id, 'categoría:', categoria);
    actividadId = id;
    tiempoInicio = new Date();
    mostrarActividad(categoria);
}

// Verificar que el archivo se cargó correctamente
console.log('✅ Todas las funciones de actividades cargadas correctamente');