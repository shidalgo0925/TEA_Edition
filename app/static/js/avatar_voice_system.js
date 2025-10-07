/**
 * Sistema de Voz del Avatar - TEA Edition
 * Maneja el Text-to-Speech y la interacción vocal del avatar
 */

class AvatarVoiceSystem {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.voices = [];
        this.currentVoice = null;
        this.isEnabled = true;
        this.volume = 0.8;
        this.rate = 0.8;
        this.pitch = 1.0;
        this.language = 'es-ES';
        
        this.initializeVoices();
        this.loadPreferences();
    }
    
    /**
     * Inicializa las voces disponibles
     */
    initializeVoices() {
        // Cargar voces disponibles
        this.loadVoices();
        
        // Si las voces no están cargadas, esperar a que se carguen
        if (this.voices.length === 0) {
            this.synthesis.onvoiceschanged = () => {
                this.loadVoices();
            };
        }
    }
    
    /**
     * Carga las voces disponibles
     */
    loadVoices() {
        this.voices = this.synthesis.getVoices();
        
        // Buscar voz en español preferida
        const spanishVoices = this.voices.filter(voice => 
            voice.lang.startsWith('es') || 
            voice.name.toLowerCase().includes('spanish') ||
            voice.name.toLowerCase().includes('español')
        );
        
        if (spanishVoices.length > 0) {
            // Preferir voces femeninas para el avatar
            const femaleVoices = spanishVoices.filter(voice => 
                voice.name.toLowerCase().includes('female') ||
                voice.name.toLowerCase().includes('mujer') ||
                voice.name.toLowerCase().includes('woman')
            );
            
            this.currentVoice = femaleVoices.length > 0 ? femaleVoices[0] : spanishVoices[0];
        } else {
            // Fallback a la primera voz disponible
            this.currentVoice = this.voices[0] || null;
        }
    }
    
    /**
     * Habla el texto proporcionado
     */
    speak(text, options = {}) {
        if (!this.isEnabled || !text) return;
        
        // Detener cualquier síntesis en curso
        this.stop();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Configurar voz
        if (this.currentVoice) {
            utterance.voice = this.currentVoice;
        }
        
        // Configurar parámetros
        utterance.volume = options.volume || this.volume;
        utterance.rate = options.rate || this.rate;
        utterance.pitch = options.pitch || this.pitch;
        utterance.lang = options.lang || this.language;
        
        // Eventos
        utterance.onstart = () => {
            this.onSpeechStart && this.onSpeechStart();
        };
        
        utterance.onend = () => {
            this.onSpeechEnd && this.onSpeechEnd();
        };
        
        utterance.onerror = (event) => {
            console.error('Error en síntesis de voz:', event.error);
            this.onSpeechError && this.onSpeechError(event.error);
        };
        
        // Hablar
        this.synthesis.speak(utterance);
    }
    
    /**
     * Habla con pausas para mejor comprensión
     */
    speakWithPauses(text, pauseDuration = 1000) {
        if (!this.isEnabled || !text) return;
        
        const sentences = text.split(/[.!?]+/).filter(s => s.trim());
        let currentIndex = 0;
        
        const speakNext = () => {
            if (currentIndex < sentences.length) {
                const sentence = sentences[currentIndex].trim();
                if (sentence) {
                    this.speak(sentence);
                    
                    // Programar siguiente oración
                    setTimeout(() => {
                        currentIndex++;
                        speakNext();
                    }, pauseDuration);
                }
            }
        };
        
        speakNext();
    }
    
    /**
     * Habla con efectos especiales
     */
    speakWithEffects(text, effect = 'normal') {
        const effects = {
            'normal': { rate: 0.8, pitch: 1.0 },
            'slow': { rate: 0.6, pitch: 1.0 },
            'fast': { rate: 1.0, pitch: 1.0 },
            'high': { rate: 0.8, pitch: 1.2 },
            'low': { rate: 0.8, pitch: 0.8 },
            'excited': { rate: 1.0, pitch: 1.1 },
            'calm': { rate: 0.7, pitch: 0.9 }
        };
        
        const effectConfig = effects[effect] || effects['normal'];
        this.speak(text, effectConfig);
    }
    
    /**
     * Detiene la síntesis actual
     */
    stop() {
        this.synthesis.cancel();
    }
    
    /**
     * Pausa la síntesis
     */
    pause() {
        this.synthesis.pause();
    }
    
    /**
     * Reanuda la síntesis
     */
    resume() {
        this.synthesis.resume();
    }
    
    /**
     * Verifica si está hablando
     */
    isSpeaking() {
        return this.synthesis.speaking;
    }
    
    /**
     * Configura la voz
     */
    setVoice(voiceName) {
        const voice = this.voices.find(v => v.name === voiceName);
        if (voice) {
            this.currentVoice = voice;
            this.savePreferences();
        }
    }
    
    /**
     * Configura el volumen
     */
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        this.savePreferences();
    }
    
    /**
     * Configura la velocidad
     */
    setRate(rate) {
        this.rate = Math.max(0.1, Math.min(10, rate));
        this.savePreferences();
    }
    
    /**
     * Configura el tono
     */
    setPitch(pitch) {
        this.pitch = Math.max(0, Math.min(2, pitch));
        this.savePreferences();
    }
    
    /**
     * Habilita o deshabilita el sistema de voz
     */
    setEnabled(enabled) {
        this.isEnabled = enabled;
        this.savePreferences();
        
        if (!enabled) {
            this.stop();
        }
    }
    
    /**
     * Obtiene las voces disponibles
     */
    getAvailableVoices() {
        return this.voices.map(voice => ({
            name: voice.name,
            lang: voice.lang,
            gender: voice.name.toLowerCase().includes('female') ? 'female' : 'male'
        }));
    }
    
    /**
     * Carga las preferencias guardadas
     */
    loadPreferences() {
        try {
            const prefs = JSON.parse(localStorage.getItem('avatar_voice_preferences') || '{}');
            
            this.isEnabled = prefs.enabled !== false;
            this.volume = prefs.volume || 0.8;
            this.rate = prefs.rate || 0.8;
            this.pitch = prefs.pitch || 1.0;
            this.language = prefs.language || 'es-ES';
            
            if (prefs.voiceName) {
                this.setVoice(prefs.voiceName);
            }
        } catch (error) {
            console.error('Error cargando preferencias de voz:', error);
        }
    }
    
    /**
     * Guarda las preferencias
     */
    savePreferences() {
        try {
            const prefs = {
                enabled: this.isEnabled,
                volume: this.volume,
                rate: this.rate,
                pitch: this.pitch,
                language: this.language,
                voiceName: this.currentVoice ? this.currentVoice.name : null
            };
            
            localStorage.setItem('avatar_voice_preferences', JSON.stringify(prefs));
        } catch (error) {
            console.error('Error guardando preferencias de voz:', error);
        }
    }
    
    /**
     * Habla una frase contextual del avatar
     */
    speakContextual(context, ninoId = null) {
        fetch('/tea/nino/api/avatar/frase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contexto: context,
                nino_id: ninoId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.frase) {
                this.speakWithEffects(data.frase, 'excited');
            }
        })
        .catch(error => {
            console.error('Error obteniendo frase del avatar:', error);
        });
    }
    
    /**
     * Habla el mensaje diario del avatar
     */
    speakDailyMessage(ninoId) {
        fetch('/tea/nino/api/avatar/mensaje-diario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nino_id: ninoId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                this.speakWithPauses(data.mensaje, 1500);
            }
        })
        .catch(error => {
            console.error('Error obteniendo mensaje diario:', error);
        });
    }
    
    /**
     * Habla una recomendación de actividad
     */
    speakActivityRecommendation(ninoId) {
        fetch('/tea/nino/api/avatar/recomendacion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nino_id: ninoId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.frase) {
                this.speakWithEffects(data.frase, 'excited');
            }
        })
        .catch(error => {
            console.error('Error obteniendo recomendación:', error);
        });
    }
}

// Instancia global del sistema de voz
let avatarVoiceSystem = null;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    avatarVoiceSystem = new AvatarVoiceSystem();
    
    // Configurar eventos globales
    setupAvatarVoiceEvents();
});

/**
 * Configura los eventos del sistema de voz
 */
function setupAvatarVoiceEvents() {
    // Hablar al cargar la página
    setTimeout(() => {
        if (avatarVoiceSystem) {
            avatarVoiceSystem.speakContextual('saludo');
        }
    }, 1000);
    
    // Hablar al completar actividades
    document.addEventListener('activityCompleted', function(event) {
        if (avatarVoiceSystem) {
            avatarVoiceSystem.speakContextual('felicitacion');
        }
    });
    
    // Hablar al seleccionar categorías
    document.addEventListener('categorySelected', function(event) {
        if (avatarVoiceSystem) {
            const categoria = event.detail.categoria;
            avatarVoiceSystem.speakContextual(`categoria_${categoria}`);
        }
    });
}

/**
 * Funciones de utilidad para usar desde otros scripts
 */
function speakAvatarText(text, effect = 'normal') {
    if (avatarVoiceSystem) {
        avatarVoiceSystem.speakWithEffects(text, effect);
    }
}

function speakAvatarContextual(context, ninoId = null) {
    if (avatarVoiceSystem) {
        avatarVoiceSystem.speakContextual(context, ninoId);
    }
}

function toggleAvatarVoice() {
    if (avatarVoiceSystem) {
        avatarVoiceSystem.setEnabled(!avatarVoiceSystem.isEnabled);
        return avatarVoiceSystem.isEnabled;
    }
    return false;
}

function setAvatarVoiceVolume(volume) {
    if (avatarVoiceSystem) {
        avatarVoiceSystem.setVolume(volume);
    }
}

function setAvatarVoiceRate(rate) {
    if (avatarVoiceSystem) {
        avatarVoiceSystem.setRate(rate);
    }
}




