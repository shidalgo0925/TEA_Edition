// -*- coding: utf-8 -*-
/**
 * Sistema de Actividades Interactivas para TEA Edition
 * Proporciona actividades reales con feedback inmediato
 */

class InteractiveActivities {
    constructor() {
        this.currentActivity = null;
        this.score = 0;
        this.streak = 0;
        this.isActive = false;
        
        this.init();
    }
    
    init() {
        console.log('🎮 Sistema de Actividades Interactivas inicializado');
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Escuchar clics en botones de actividades
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('activity-button')) {
                this.handleActivityClick(e.target);
            }
            
            if (e.target.classList.contains('answer-option')) {
                this.handleAnswerClick(e.target);
            }
            
            if (e.target.classList.contains('color-option')) {
                this.handleColorClick(e.target);
            }
            
            if (e.target.classList.contains('number-option')) {
                this.handleNumberClick(e.target);
            }
        });
    }
    
    // Actividad de Colores
    startColorActivity() {
        this.currentActivity = 'colores';
        this.isActive = true;
        
        // Generar colores aleatorios
        const colors = ['rojo', 'azul', 'verde', 'amarillo', 'naranja', 'morado', 'rosa', 'marrón'];
        const targetColor = colors[Math.floor(Math.random() * colors.length)];
        
        // Crear interfaz de actividad
        const activityHTML = `
            <div class="activity-container" id="color-activity">
                <div class="activity-header">
                    <h3>🎨 Actividad de Colores</h3>
                    <div class="score-display">Puntos: ${this.score} | Racha: ${this.streak}</div>
                </div>
                
                <div class="activity-content">
                    <div class="target-color" style="background-color: ${this.getColorValue(targetColor)}; width: 100px; height: 100px; border-radius: 50%; margin: 20px auto; border: 3px solid #333;"></div>
                    
                    <div class="instruction">
                        <p>¿Qué color es este?</p>
                        <p style="font-size: 0.9rem; color: #7F8C8D; margin-top: 10px;">
                            Puedes decirlo en voz alta o hacer clic en el botón
                        </p>
                    </div>
                    
                    <!-- Botón de reconocimiento de voz -->
                    <div style="text-align: center; margin: 20px 0;">
                        <button id="voice-button" onclick="interactiveActivities.toggleVoiceInput()" 
                                style="padding: 15px 30px; border: none; border-radius: 50px; background: linear-gradient(135deg, #1D63FF, #4A90E2); color: white; font-size: 1.1rem; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(29, 99, 255, 0.3);">
                            🎤 Decir en voz alta
                        </button>
                        <div id="voice-status" style="margin-top: 10px; font-size: 0.9rem; color: #7F8C8D;"></div>
                    </div>
                    
                    <div class="color-options">
                        ${colors.map(color => `
                            <button class="color-option" data-color="${color}" style="background-color: ${this.getColorValue(color)}; color: white; padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer;">
                                ${color.toUpperCase()}
                            </button>
                        `).join('')}
                    </div>
                    
                    <div class="feedback" id="color-feedback"></div>
                </div>
                
                <div class="activity-controls">
                    <button onclick="interactiveActivities.endActivity()" class="btn btn-secondary">Terminar</button>
                </div>
            </div>
        `;
        
        // Mostrar actividad
        const container = document.getElementById('activity-content') || document.body;
        container.innerHTML = activityHTML;
        
        // Guardar color objetivo
        this.targetColor = targetColor;
        
        // Configurar reconocimiento de voz
        this.setupVoiceRecognition();
        
        // Dar instrucción de voz
        if (window.audioSystem) {
            window.audioSystem.giveInstruction('colores');
        }
        
        console.log('🎨 Actividad de colores iniciada. Color objetivo:', targetColor);
    }
    
    handleColorClick(button) {
        if (!this.isActive || this.currentActivity !== 'colores') return;
        
        const selectedColor = button.dataset.color;
        const feedback = document.getElementById('color-feedback');
        
        if (selectedColor === this.targetColor) {
            // Correcto
            this.score += 10;
            this.streak++;
            feedback.innerHTML = '<div class="success">¡Correcto! ¡Muy bien!</div>';
            feedback.className = 'feedback success';
            
            if (window.audioSystem) {
                window.audioSystem.encourage();
                window.audioSystem.playSuccessSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
            
            // Continuar con siguiente color después de un momento
            setTimeout(() => {
                this.startColorActivity();
            }, 2000);
            
        } else {
            // Incorrecto
            this.streak = 0;
            feedback.innerHTML = '<div class="error">No es correcto. ¡Inténtalo de nuevo!</div>';
            feedback.className = 'feedback error';
            
            if (window.audioSystem) {
                window.audioSystem.correct();
                window.audioSystem.playErrorSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
        }
    }
    
    // Actividad de Números
    startNumberActivity() {
        this.currentActivity = 'numeros';
        this.isActive = true;
        
        // Generar número aleatorio
        const targetNumber = Math.floor(Math.random() * 10) + 1;
        
        // Crear interfaz de actividad
        const activityHTML = `
            <div class="activity-container" id="number-activity">
                <div class="activity-header">
                    <h3>🔢 Actividad de Números</h3>
                    <div class="score-display">Puntos: ${this.score} | Racha: ${this.streak}</div>
                </div>
                
                <div class="activity-content">
                    <div class="number-display" style="font-size: 4em; font-weight: bold; color: #1D63FF; margin: 20px 0;">
                        ${targetNumber}
                    </div>
                    
                    <div class="instruction">
                        <p>¿Cuántos objetos hay aquí?</p>
                    </div>
                    
                    <div class="object-display" style="margin: 20px 0;">
                        ${'🍎'.repeat(targetNumber)}
                    </div>
                    
                    <div class="number-options">
                        ${Array.from({length: 10}, (_, i) => i + 1).map(num => `
                            <button class="number-option" data-number="${num}" style="padding: 15px 25px; margin: 5px; border: 2px solid #1D63FF; background: white; color: #1D63FF; border-radius: 50%; cursor: pointer; font-size: 1.2em; font-weight: bold;">
                                ${num}
                            </button>
                        `).join('')}
                    </div>
                    
                    <div class="feedback" id="number-feedback"></div>
                </div>
                
                <div class="activity-controls">
                    <button onclick="interactiveActivities.endActivity()" class="btn btn-secondary">Terminar</button>
                </div>
            </div>
        `;
        
        // Mostrar actividad
        const container = document.getElementById('activity-content') || document.body;
        container.innerHTML = activityHTML;
        
        // Guardar número objetivo
        this.targetNumber = targetNumber;
        
        // Dar instrucción de voz
        if (window.audioSystem) {
            window.audioSystem.giveInstruction('numeros');
        }
        
        console.log('🔢 Actividad de números iniciada. Número objetivo:', targetNumber);
    }
    
    handleNumberClick(button) {
        if (!this.isActive || this.currentActivity !== 'numeros') return;
        
        const selectedNumber = parseInt(button.dataset.number);
        const feedback = document.getElementById('number-feedback');
        
        if (selectedNumber === this.targetNumber) {
            // Correcto
            this.score += 15;
            this.streak++;
            feedback.innerHTML = '<div class="success">¡Excelente! ¡Contaste perfectamente!</div>';
            feedback.className = 'feedback success';
            
            if (window.audioSystem) {
                window.audioSystem.encourage();
                window.audioSystem.playSuccessSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
            
            // Continuar con siguiente número después de un momento
            setTimeout(() => {
                this.startNumberActivity();
            }, 2000);
            
        } else {
            // Incorrecto
            this.streak = 0;
            feedback.innerHTML = '<div class="error">No es correcto. ¡Cuenta de nuevo!</div>';
            feedback.className = 'feedback error';
            
            if (window.audioSystem) {
                window.audioSystem.correct();
                window.audioSystem.playErrorSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
        }
    }
    
    // Actividad de Lenguaje
    startLanguageActivity() {
        this.currentActivity = 'lenguaje';
        this.isActive = true;
        
        // Palabras para practicar
        const words = [
            { word: 'casa', image: '🏠' },
            { word: 'perro', image: '🐕' },
            { word: 'gato', image: '🐱' },
            { word: 'sol', image: '☀️' },
            { word: 'luna', image: '🌙' },
            { word: 'agua', image: '💧' },
            { word: 'árbol', image: '🌳' },
            { word: 'flor', image: '🌸' }
        ];
        
        const targetWord = words[Math.floor(Math.random() * words.length)];
        
        // Crear interfaz de actividad
        const activityHTML = `
            <div class="activity-container" id="language-activity">
                <div class="activity-header">
                    <h3>🗣️ Actividad de Lenguaje</h3>
                    <div class="score-display">Puntos: ${this.score} | Racha: ${this.streak}</div>
                </div>
                
                <div class="activity-content">
                    <div class="word-display" style="font-size: 3em; margin: 20px 0;">
                        ${targetWord.image}
                    </div>
                    
                    <div class="instruction">
                        <p>¿Puedes decir la palabra?</p>
                        <button onclick="interactiveActivities.speakWord('${targetWord.word}')" class="btn btn-primary" style="margin: 10px;">
                            🔊 Escuchar
                        </button>
                    </div>
                    
                    <div class="word-options">
                        ${words.map(w => `
                            <button class="word-option" data-word="${w.word}" style="padding: 10px 20px; margin: 5px; border: 2px solid #FFCE32; background: white; color: #1D63FF; border-radius: 5px; cursor: pointer; font-size: 1.1em;">
                                ${w.word.toUpperCase()}
                            </button>
                        `).join('')}
                    </div>
                    
                    <div class="feedback" id="language-feedback"></div>
                </div>
                
                <div class="activity-controls">
                    <button onclick="interactiveActivities.endActivity()" class="btn btn-secondary">Terminar</button>
                </div>
            </div>
        `;
        
        // Mostrar actividad
        const container = document.getElementById('activity-content') || document.body;
        container.innerHTML = activityHTML;
        
        // Guardar palabra objetivo
        this.targetWord = targetWord.word;
        
        // Dar instrucción de voz
        if (window.audioSystem) {
            window.audioSystem.giveInstruction('lenguaje');
        }
        
        console.log('🗣️ Actividad de lenguaje iniciada. Palabra objetivo:', targetWord.word);
    }
    
    speakWord(word) {
        if (window.audioSystem) {
            window.audioSystem.speak(`La palabra es: ${word}`, { rate: 0.7 });
        }
    }
    
    handleWordClick(button) {
        if (!this.isActive || this.currentActivity !== 'lenguaje') return;
        
        const selectedWord = button.dataset.word;
        const feedback = document.getElementById('language-feedback');
        
        if (selectedWord === this.targetWord) {
            // Correcto
            this.score += 20;
            this.streak++;
            feedback.innerHTML = '<div class="success">¡Perfecto! ¡Dijiste la palabra correctamente!</div>';
            feedback.className = 'feedback success';
            
            if (window.audioSystem) {
                window.audioSystem.encourage();
                window.audioSystem.playSuccessSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
            
            // Continuar con siguiente palabra después de un momento
            setTimeout(() => {
                this.startLanguageActivity();
            }, 2000);
            
        } else {
            // Incorrecto
            this.streak = 0;
            feedback.innerHTML = '<div class="error">No es correcto. ¡Inténtalo de nuevo!</div>';
            feedback.className = 'feedback error';
            
            if (window.audioSystem) {
                window.audioSystem.correct();
                window.audioSystem.playErrorSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
        }
    }
    
    // Métodos auxiliares
    getColorValue(colorName) {
        const colors = {
            'rojo': '#FF0000',
            'azul': '#0000FF',
            'verde': '#00FF00',
            'amarillo': '#FFFF00',
            'naranja': '#FFA500',
            'morado': '#800080',
            'rosa': '#FFC0CB',
            'marrón': '#A52A2A'
        };
        return colors[colorName] || '#000000';
    }
    
    handleActivityClick(button) {
        const activityType = button.dataset.activity;
        
        switch(activityType) {
            case 'colores':
                this.startColorActivity();
                break;
            case 'numeros':
                this.startNumberActivity();
                break;
            case 'lenguaje':
                this.startLanguageActivity();
                break;
            default:
                console.log('Actividad no reconocida:', activityType);
        }
    }
    
    endActivity() {
        this.isActive = false;
        this.currentActivity = null;
        
        // Mostrar resumen de la sesión
        const summaryHTML = `
            <div class="activity-summary">
                <h3>🎉 ¡Sesión Completada!</h3>
                <div class="summary-stats">
                    <p>Puntos obtenidos: <strong>${this.score}</strong></p>
                    <p>Racha máxima: <strong>${this.streak}</strong></p>
                </div>
                <div class="summary-actions">
                    <button onclick="interactiveActivities.resetScore()" class="btn btn-primary">Nueva Sesión</button>
                    <button onclick="location.reload()" class="btn btn-secondary">Volver al Menú</button>
                </div>
            </div>
        `;
        
        const container = document.getElementById('activity-content') || document.body;
        container.innerHTML = summaryHTML;
        
        // Felicitar con voz
        if (window.audioSystem) {
            window.audioSystem.speak(`¡Excelente trabajo! Obtuviste ${this.score} puntos. ¡Estoy muy orgullosa de ti!`);
        }
        
        console.log('🎮 Actividad terminada. Puntuación final:', this.score);
    }
    
    resetScore() {
        this.score = 0;
        this.streak = 0;
        console.log('🔄 Puntuación reiniciada');
    }
    
    getScore() {
        return {
            score: this.score,
            streak: this.streak,
            isActive: this.isActive
        };
    }
    
    // Métodos de reconocimiento de voz
    setupVoiceRecognition() {
        if (!window.voiceRecognition || !window.voiceRecognition.isSupported()) {
            console.warn('⚠️ Reconocimiento de voz no disponible');
            return;
        }
        
        // Configurar callbacks
        window.voiceRecognition.onResult = (transcript, confidence, type) => {
            this.handleVoiceResult(transcript, confidence, type);
        };
        
        window.voiceRecognition.onStart = () => {
            this.updateVoiceStatus('🎤 Escuchando...', '#1D63FF');
        };
        
        window.voiceRecognition.onEnd = () => {
            this.updateVoiceStatus('🔇 Haz clic para hablar', '#7F8C8D');
        };
        
        window.voiceRecognition.onError = (error) => {
            this.updateVoiceStatus('❌ Error: ' + error.error, '#E74C3C');
        };
    }
    
    toggleVoiceInput() {
        if (!window.voiceRecognition || !window.voiceRecognition.isSupported()) {
            this.updateVoiceStatus('❌ Reconocimiento de voz no disponible', '#E74C3C');
            return;
        }
        
        if (window.voiceRecognition.isCurrentlyListening()) {
            window.voiceRecognition.stopListening();
        } else {
            window.voiceRecognition.startListeningForActivity(this.currentActivity, (transcript, confidence, type) => {
                this.handleVoiceResult(transcript, confidence, type);
            });
        }
    }
    
    handleVoiceResult(transcript, confidence, type) {
        console.log('🎤 Resultado de voz:', transcript, 'Confianza:', confidence, 'Tipo:', type);
        
        if (type === 'interim') {
            this.updateVoiceStatus('🎤 Escuchando: "' + transcript + '"', '#FFCE32');
            return;
        }
        
        if (type === 'final') {
            this.updateVoiceStatus('✅ Escuché: "' + transcript + '"', '#2ECC71');
            
            // Procesar según el tipo de actividad
            let isCorrect = false;
            
            switch(this.currentActivity) {
                case 'colores':
                    isCorrect = this.processColorVoiceInput(transcript);
                    break;
                case 'numeros':
                    isCorrect = this.processNumberVoiceInput(transcript);
                    break;
                case 'lenguaje':
                    isCorrect = this.processLanguageVoiceInput(transcript);
                    break;
            }
            
            if (isCorrect !== null) {
                // Simular clic en el botón correcto
                setTimeout(() => {
                    this.processVoiceAnswer(isCorrect);
                }, 1000);
            } else {
                // Respuesta no reconocida
                setTimeout(() => {
                    this.updateVoiceStatus('❓ No entendí. Inténtalo de nuevo', '#E74C3C');
                    if (window.audioSystem) {
                        window.audioSystem.speak('No entendí lo que dijiste. ¿Puedes repetirlo?');
                    }
                }, 1000);
            }
        }
    }
    
    processColorVoiceInput(transcript) {
        const recognizedColor = window.voiceRecognition.processColorResponse(transcript);
        if (recognizedColor) {
            return recognizedColor === this.targetColor;
        }
        return null;
    }
    
    processNumberVoiceInput(transcript) {
        const recognizedNumber = window.voiceRecognition.processNumberResponse(transcript);
        if (recognizedNumber !== null) {
            return recognizedNumber === this.targetNumber;
        }
        return null;
    }
    
    processLanguageVoiceInput(transcript) {
        if (this.targetWord) {
            return window.voiceRecognition.processWordResponse(transcript, this.targetWord);
        }
        return null;
    }
    
    processVoiceAnswer(isCorrect) {
        const feedback = document.getElementById(this.currentActivity + '-feedback');
        
        if (isCorrect) {
            // Correcto
            this.score += this.currentActivity === 'colores' ? 10 : this.currentActivity === 'numeros' ? 15 : 20;
            this.streak++;
            feedback.innerHTML = '<div class="success">¡Correcto! ¡Muy bien!</div>';
            feedback.className = 'feedback success';
            
            if (window.audioSystem) {
                window.audioSystem.encourage();
                window.audioSystem.playSuccessSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
            
            // Continuar con siguiente actividad después de un momento
            setTimeout(() => {
                if (this.currentActivity === 'colores') {
                    this.startColorActivity();
                } else if (this.currentActivity === 'numeros') {
                    this.startNumberActivity();
                } else if (this.currentActivity === 'lenguaje') {
                    this.startLanguageActivity();
                }
            }, 2000);
            
        } else {
            // Incorrecto
            this.streak = 0;
            feedback.innerHTML = '<div class="error">No es correcto. ¡Inténtalo de nuevo!</div>';
            feedback.className = 'feedback error';
            
            if (window.audioSystem) {
                window.audioSystem.correct();
                window.audioSystem.playErrorSound();
            }
            
            // Actualizar puntuación
            document.querySelector('.score-display').textContent = `Puntos: ${this.score} | Racha: ${this.streak}`;
        }
        
        // Limpiar estado de voz
        this.updateVoiceStatus('🔇 Haz clic para hablar', '#7F8C8D');
    }
    
    updateVoiceStatus(message, color) {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.style.color = color;
        }
    }
}

// Instancia global del sistema de actividades
window.interactiveActivities = new InteractiveActivities();

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InteractiveActivities;
}
