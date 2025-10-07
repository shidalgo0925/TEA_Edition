/**
 * Sistema de Actividades de Descanso y Relajación
 * Para niños con TEA - TEA Edition
 */

class RestActivities {
    constructor() {
        this.currentActivity = null;
        this.audioContext = null;
        this.isPlaying = false;
        this.init();
    }
    
    init() {
        this.setupAudioContext();
        this.createRestOverlay();
    }
    
    setupAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (error) {
            console.log('Audio context no disponible');
        }
    }
    
    createRestOverlay() {
        // Crear overlay para actividades de descanso
        const overlay = document.createElement('div');
        overlay.id = 'restOverlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 3000;
            display: none;
            align-items: center;
            justify-content: center;
            color: white;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        `;
        
        overlay.innerHTML = `
            <div style="text-align: center; padding: 30px; max-width: 500px;">
                <div id="restContent">
                    <!-- Contenido dinámico -->
                </div>
                <div style="margin-top: 30px;">
                    <button id="closeRest" style="
                        background: #E74C3C;
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 25px;
                        font-size: 1.2rem;
                        cursor: pointer;
                        margin: 10px;
                    ">Cerrar</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        // Event listeners
        document.getElementById('closeRest').addEventListener('click', () => {
            this.closeRestActivity();
        });
        
        // Cerrar con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && overlay.style.display === 'flex') {
                this.closeRestActivity();
            }
        });
    }
    
    startBreathingExercise() {
        this.currentActivity = 'breathing';
        this.showRestOverlay();
        
        const content = document.getElementById('restContent');
        content.innerHTML = `
            <h2 style="font-size: 2rem; margin-bottom: 20px; color: #FFD700;">🫁 Ejercicio de Respiración</h2>
            <p style="font-size: 1.2rem; margin-bottom: 30px;">
                Vamos a respirar juntos. Sigue el círculo con tu respiración.
            </p>
            <div id="breathingCircle" style="
                width: 200px;
                height: 200px;
                border: 5px solid #FFD700;
                border-radius: 50%;
                margin: 0 auto 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                font-weight: bold;
                transition: all 4s ease-in-out;
            ">Inhala</div>
            <div id="breathingInstructions" style="font-size: 1.1rem;">
                Inhala lentamente por 4 segundos...
            </div>
        `;
        
        this.startBreathingCycle();
        this.speakText('Vamos a hacer un ejercicio de respiración. Inhala cuando el círculo crezca, exhala cuando se encoja.');
    }
    
    startBreathingCycle() {
        const circle = document.getElementById('breathingCircle');
        const instructions = document.getElementById('breathingInstructions');
        let phase = 'inhale'; // inhale, hold, exhale, pause
        let count = 0;
        
        const cycle = () => {
            switch(phase) {
                case 'inhale':
                    circle.style.transform = 'scale(1.3)';
                    circle.style.backgroundColor = '#3498DB';
                    circle.textContent = 'Inhala';
                    instructions.textContent = 'Inhala lentamente por 4 segundos...';
                    this.speakText('Inhala');
                    setTimeout(() => { phase = 'hold'; cycle(); }, 4000);
                    break;
                    
                case 'hold':
                    circle.style.transform = 'scale(1.3)';
                    circle.style.backgroundColor = '#2ECC71';
                    circle.textContent = 'Mantén';
                    instructions.textContent = 'Mantén la respiración por 4 segundos...';
                    this.speakText('Mantén');
                    setTimeout(() => { phase = 'exhale'; cycle(); }, 4000);
                    break;
                    
                case 'exhale':
                    circle.style.transform = 'scale(1)';
                    circle.style.backgroundColor = '#E74C3C';
                    circle.textContent = 'Exhala';
                    instructions.textContent = 'Exhala lentamente por 4 segundos...';
                    this.speakText('Exhala');
                    setTimeout(() => { phase = 'pause'; cycle(); }, 4000);
                    break;
                    
                case 'pause':
                    circle.style.transform = 'scale(1)';
                    circle.style.backgroundColor = '#9B59B6';
                    circle.textContent = 'Pausa';
                    instructions.textContent = 'Descansa por 2 segundos...';
                    setTimeout(() => { 
                        count++;
                        if (count < 3) {
                            phase = 'inhale'; 
                            cycle(); 
                        } else {
                            this.finishBreathingExercise();
                        }
                    }, 2000);
                    break;
            }
        };
        
        cycle();
    }
    
    finishBreathingExercise() {
        const content = document.getElementById('restContent');
        content.innerHTML = `
            <h2 style="font-size: 2rem; margin-bottom: 20px; color: #2ECC71;">✨ ¡Muy bien!</h2>
            <p style="font-size: 1.2rem; margin-bottom: 20px;">
                Has completado el ejercicio de respiración. ¿Te sientes más relajado?
            </p>
            <div style="font-size: 3rem; margin: 20px 0;">🌟</div>
            <p style="font-size: 1rem; color: #BDC3C7;">
                Puedes repetir este ejercicio cuando te sientas estresado o ansioso.
            </p>
        `;
        
        this.speakText('¡Excelente! Has completado el ejercicio de respiración. Te sientes más relajado ahora.');
        
        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            this.closeRestActivity();
        }, 5000);
    }
    
    playRelaxingMusic() {
        this.currentActivity = 'music';
        this.showRestOverlay();
        
        const content = document.getElementById('restContent');
        content.innerHTML = `
            <h2 style="font-size: 2rem; margin-bottom: 20px; color: #FFD700;">🎵 Música Relajante</h2>
            <p style="font-size: 1.2rem; margin-bottom: 30px;">
                Escucha esta música suave y relajante.
            </p>
            <div id="musicVisualizer" style="
                width: 300px;
                height: 100px;
                margin: 0 auto 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(45deg, #3498DB, #2ECC71, #9B59B6);
                border-radius: 15px;
                position: relative;
                overflow: hidden;
            ">
                <div style="font-size: 2rem;">🎶</div>
                <div id="musicBars" style="
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    height: 20px;
                    display: flex;
                    align-items: end;
                    justify-content: space-around;
                    padding: 0 20px;
                ">
                    ${Array.from({length: 10}, () => 
                        `<div style="
                            width: 4px;
                            background: rgba(255,255,255,0.8);
                            border-radius: 2px;
                            animation: musicBar 1s ease-in-out infinite;
                        "></div>`
                    ).join('')}
                </div>
            </div>
            <div id="musicControls" style="margin-top: 20px;">
                <button id="playPauseMusic" style="
                    background: #27AE60;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 25px;
                    font-size: 1.1rem;
                    cursor: pointer;
                    margin: 5px;
                ">▶️ Reproducir</button>
                <button id="stopMusic" style="
                    background: #E74C3C;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 25px;
                    font-size: 1.1rem;
                    cursor: pointer;
                    margin: 5px;
                ">⏹️ Detener</button>
            </div>
        `;
        
        // Agregar CSS para animación
        const style = document.createElement('style');
        style.textContent = `
            @keyframes musicBar {
                0%, 100% { height: 5px; }
                50% { height: 20px; }
            }
        `;
        document.head.appendChild(style);
        
        // Event listeners para controles de música
        document.getElementById('playPauseMusic').addEventListener('click', () => {
            this.toggleMusic();
        });
        
        document.getElementById('stopMusic').addEventListener('click', () => {
            this.stopMusic();
        });
        
        this.speakText('Aquí tienes música relajante. Puedes reproducirla o detenerla cuando quieras.');
    }
    
    toggleMusic() {
        const button = document.getElementById('playPauseMusic');
        if (this.isPlaying) {
            this.pauseMusic();
            button.textContent = '▶️ Reproducir';
        } else {
            this.playMusic();
            button.textContent = '⏸️ Pausar';
        }
    }
    
    playMusic() {
        this.isPlaying = true;
        this.speakText('Reproduciendo música relajante.');
        // Aquí se podría integrar con un servicio de música real
        console.log('Reproduciendo música relajante...');
    }
    
    pauseMusic() {
        this.isPlaying = false;
        this.speakText('Música pausada.');
        console.log('Música pausada...');
    }
    
    stopMusic() {
        this.isPlaying = false;
        const button = document.getElementById('playPauseMusic');
        button.textContent = '▶️ Reproducir';
        this.speakText('Música detenida.');
        console.log('Música detenida...');
    }
    
    startStretchingExercise() {
        this.currentActivity = 'stretching';
        this.showRestOverlay();
        
        const content = document.getElementById('restContent');
        content.innerHTML = `
            <h2 style="font-size: 2rem; margin-bottom: 20px; color: #FFD700;">🤸 Ejercicios de Estiramiento</h2>
            <p style="font-size: 1.2rem; margin-bottom: 30px;">
                Vamos a hacer algunos estiramientos suaves.
            </p>
            <div id="stretchingExercise" style="
                width: 300px;
                height: 200px;
                margin: 0 auto 30px;
                background: linear-gradient(135deg, #3498DB, #2ECC71);
                border-radius: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
                color: white;
                transition: all 2s ease;
            ">🤸</div>
            <div id="stretchingInstructions" style="font-size: 1.1rem; margin-bottom: 20px;">
                Estiramiento 1: Estira los brazos hacia arriba
            </div>
            <div id="stretchingProgress" style="
                width: 100%;
                height: 10px;
                background: #34495E;
                border-radius: 5px;
                overflow: hidden;
                margin-bottom: 20px;
            ">
                <div id="stretchingProgressBar" style="
                    height: 100%;
                    background: #2ECC71;
                    width: 0%;
                    transition: width 0.5s ease;
                "></div>
            </div>
            <div id="stretchingCounter" style="font-size: 1.2rem; font-weight: bold;">
                1 de 5 ejercicios
            </div>
        `;
        
        this.startStretchingSequence();
        this.speakText('Vamos a hacer ejercicios de estiramiento. Sigue las instrucciones y haz los movimientos suavemente.');
    }
    
    startStretchingSequence() {
        const exercises = [
            { emoji: '🤸', instruction: 'Estira los brazos hacia arriba y mantén por 5 segundos', duration: 5000 },
            { emoji: '🙆', instruction: 'Toca los dedos de los pies manteniendo las piernas rectas', duration: 5000 },
            { emoji: '🤲', instruction: 'Abre los brazos en cruz y respira profundo', duration: 5000 },
            { emoji: '🔄', instruction: 'Gira suavemente el cuello hacia la derecha e izquierda', duration: 5000 },
            { emoji: '🧘', instruction: 'Siéntate y relaja todo el cuerpo', duration: 5000 }
        ];
        
        let currentExercise = 0;
        
        const showExercise = () => {
            if (currentExercise >= exercises.length) {
                this.finishStretchingExercise();
                return;
            }
            
            const exercise = exercises[currentExercise];
            const exerciseDiv = document.getElementById('stretchingExercise');
            const instructions = document.getElementById('stretchingInstructions');
            const progressBar = document.getElementById('stretchingProgressBar');
            const counter = document.getElementById('stretchingCounter');
            
            exerciseDiv.textContent = exercise.emoji;
            instructions.textContent = exercise.instruction;
            counter.textContent = `${currentExercise + 1} de ${exercises.length} ejercicios`;
            
            // Animar progreso
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 2;
                progressBar.style.width = `${progress}%`;
                if (progress >= 100) {
                    clearInterval(progressInterval);
                }
            }, exercise.duration / 50);
            
            this.speakText(exercise.instruction);
            
            setTimeout(() => {
                currentExercise++;
                showExercise();
            }, exercise.duration);
        };
        
        showExercise();
    }
    
    finishStretchingExercise() {
        const content = document.getElementById('restContent');
        content.innerHTML = `
            <h2 style="font-size: 2rem; margin-bottom: 20px; color: #2ECC71;">✨ ¡Excelente!</h2>
            <p style="font-size: 1.2rem; margin-bottom: 20px;">
                Has completado todos los ejercicios de estiramiento. ¡Tu cuerpo se siente más relajado!
            </p>
            <div style="font-size: 3rem; margin: 20px 0;">🌟</div>
            <p style="font-size: 1rem; color: #BDC3C7;">
                Recuerda hacer estiramientos cuando te sientas tenso o después de estar sentado mucho tiempo.
            </p>
        `;
        
        this.speakText('¡Muy bien! Has completado todos los ejercicios de estiramiento. Tu cuerpo se siente más relajado ahora.');
        
        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            this.closeRestActivity();
        }, 5000);
    }
    
    showRestOverlay() {
        const overlay = document.getElementById('restOverlay');
        overlay.style.display = 'flex';
        overlay.focus();
    }
    
    closeRestActivity() {
        const overlay = document.getElementById('restOverlay');
        overlay.style.display = 'none';
        
        // Limpiar actividad actual
        if (this.currentActivity === 'music') {
            this.stopMusic();
        }
        
        this.currentActivity = null;
        this.speakText('Actividad de descanso terminada. Puedes continuar con tus actividades de aprendizaje.');
    }
    
    speakText(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-ES';
            utterance.rate = 0.8;
            utterance.pitch = 1.0;
            speechSynthesis.speak(utterance);
        }
    }
}

// Funciones globales para compatibilidad
function startBreathingExercise() {
    if (!window.restActivities) {
        window.restActivities = new RestActivities();
    }
    window.restActivities.startBreathingExercise();
}

function playRelaxingMusic() {
    if (!window.restActivities) {
        window.restActivities = new RestActivities();
    }
    window.restActivities.playRelaxingMusic();
}

function startStretchingExercise() {
    if (!window.restActivities) {
        window.restActivities = new RestActivities();
    }
    window.restActivities.startStretchingExercise();
}

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    window.restActivities = new RestActivities();
});





