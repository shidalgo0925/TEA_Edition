// -*- coding: utf-8 -*-
/**
 * Sistema de Audio para TEA Edition
 * Proporciona voces y sonidos para el avatar virtual
 */

class AudioSystem {
    constructor() {
        this.synth = window.speechSynthesis;
        this.voices = [];
        this.currentVoice = null;
        this.isEnabled = true;
        this.volume = 0.8;
        
        // Configuraciones de voz
        this.voiceConfig = {
            gender: 'female', // 'female', 'male', 'any'
            language: 'es',   // 'es', 'en', 'any'
            speed: 0.9,       // 0.1 - 2.0
            pitch: 1.1,       // 0.0 - 2.0
            volume: 0.8       // 0.0 - 1.0
        };
        
        this.init();
    }
    
    init() {
        // Cargar voces disponibles
        this.loadVoices();
        
        // Si las voces no están listas, esperar
        if (this.synth.onvoiceschanged !== undefined) {
            this.synth.onvoiceschanged = () => this.loadVoices();
        }
        
        console.log('🎵 Sistema de Audio inicializado');
    }
    
    loadVoices() {
        this.voices = this.synth.getVoices();
        
        // Cargar configuración desde localStorage si existe
        this.loadVoiceConfig();
        
        // Buscar voz según configuración
        this.currentVoice = this.findVoiceByConfig();
        
        if (this.currentVoice) {
            console.log('🎤 Voz seleccionada:', this.currentVoice.name, '| Config:', this.voiceConfig.gender, this.voiceConfig.language);
        } else {
            console.log('❌ No se encontró voz con la configuración actual');
        }
    }
    
    findVoiceByConfig() {
        const { gender, language } = this.voiceConfig;
        
        // Lista de nombres femeninos comunes
        const femaleNames = [
            'female', 'mujer', 'woman', 'maria', 'carmen', 'lucia', 'sofia', 'ana',
            'elena', 'isabel', 'paula', 'laura', 'andrea', 'monica', 'patricia',
            'sandra', 'natalia', 'beatriz', 'cristina', 'raquel', 'marta', 'silvia',
            'alicia', 'claudia', 'diana', 'fernanda', 'gabriela', 'helena', 'irene',
            'julia', 'karen', 'lorena', 'miriam', 'nuria', 'olga', 'pilar', 'rosa',
            'sara', 'teresa', 'ursula', 'valeria', 'wendy', 'ximena', 'yolanda', 'zoe'
        ];
        
        // Lista de nombres masculinos comunes
        const maleNames = [
            'male', 'hombre', 'man', 'carlos', 'juan', 'pedro', 'luis', 'miguel',
            'antonio', 'francisco', 'david', 'jose', 'manuel', 'rafael', 'daniel',
            'alejandro', 'fernando', 'sergio', 'roberto', 'javier', 'alberto',
            'eduardo', 'victor', 'pablo', 'oscar', 'ruben', 'adrian', 'raul',
            'enrique', 'ignacio', 'arturo', 'ricardo', 'sebastian', 'gonzalo'
        ];
        
        // Filtrar por idioma
        let languageVoices = this.voices;
        if (language !== 'any') {
            languageVoices = this.voices.filter(voice => 
                voice.lang.includes(language) || 
                voice.name.toLowerCase().includes(language === 'es' ? 'spanish' : language) ||
                voice.name.toLowerCase().includes(language === 'es' ? 'español' : language)
            );
        }
        
        // Si no hay voces en el idioma especificado, usar todas
        if (languageVoices.length === 0) {
            languageVoices = this.voices;
        }
        
        // Filtrar por género
        if (gender === 'female') {
            const femaleVoices = languageVoices.filter(voice => 
                femaleNames.some(name => voice.name.toLowerCase().includes(name))
            );
            if (femaleVoices.length > 0) {
                return femaleVoices[0];
            }
        } else if (gender === 'male') {
            const maleVoices = languageVoices.filter(voice => 
                maleNames.some(name => voice.name.toLowerCase().includes(name))
            );
            if (maleVoices.length > 0) {
                return maleVoices[0];
            }
        }
        
        // Si no se encuentra voz con el género especificado, usar la primera disponible
        if (languageVoices.length > 0) {
            return languageVoices[0];
        }
        
        // Último recurso: cualquier voz disponible
        return this.voices[0] || null;
    }
    
    loadVoiceConfig() {
        // Cargar configuración desde localStorage
        const savedConfig = localStorage.getItem('tea_voice_config');
        if (savedConfig) {
            try {
                const config = JSON.parse(savedConfig);
                this.voiceConfig = { ...this.voiceConfig, ...config };
                console.log('🔧 Configuración de voz cargada:', this.voiceConfig);
            } catch (error) {
                console.error('❌ Error cargando configuración de voz:', error);
            }
        }
    }
    
    saveVoiceConfig() {
        // Guardar configuración en localStorage
        try {
            localStorage.setItem('tea_voice_config', JSON.stringify(this.voiceConfig));
            console.log('💾 Configuración de voz guardada:', this.voiceConfig);
        } catch (error) {
            console.error('❌ Error guardando configuración de voz:', error);
        }
    }
    
    speak(text, options = {}) {
        if (!this.isEnabled || !this.synth) {
            console.log('🔇 Audio deshabilitado');
            return;
        }
        
        // Cancelar cualquier audio anterior
        this.synth.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Configurar voz
        if (this.currentVoice) {
            utterance.voice = this.currentVoice;
        }
        
        // Configurar opciones usando la configuración guardada
        utterance.rate = options.rate || this.voiceConfig.speed;
        utterance.pitch = options.pitch || this.voiceConfig.pitch;
        utterance.volume = options.volume || this.voiceConfig.volume;
        utterance.lang = this.voiceConfig.language === 'es' ? 'es-ES' : 'en-US';
        
        // Eventos
        utterance.onstart = () => {
            console.log('🎤 Hablando:', text);
            this.onSpeakingStart?.(text);
        };
        
        utterance.onend = () => {
            console.log('✅ Terminó de hablar');
            this.onSpeakingEnd?.(text);
        };
        
        utterance.onerror = (event) => {
            console.error('❌ Error de audio:', event.error);
        };
        
        // Hablar
        this.synth.speak(utterance);
    }
    
    // Mensajes predefinidos para el avatar
    greetings = [
        "¡Hola! Soy tu maestra virtual. ¿Cómo estás hoy?",
        "¡Buenos días! ¿Estás listo para aprender?",
        "¡Hola! Me da mucho gusto verte. ¿Qué vamos a hacer hoy?",
        "¡Hola! ¿Cómo te sientes? ¿Listo para divertirnos aprendiendo?"
    ];
    
    encouragements = [
        "¡Muy bien! ¡Lo estás haciendo excelente!",
        "¡Perfecto! ¡Eres muy inteligente!",
        "¡Excelente trabajo! ¡Sigue así!",
        "¡Fantástico! ¡Estoy muy orgullosa de ti!",
        "¡Increíble! ¡Lo hiciste muy bien!"
    ];
    
    corrections = [
        "No te preocupes, vamos a intentarlo de nuevo. ¡Tú puedes!",
        "Casi lo tienes. Vamos a practicar un poquito más.",
        "Está bien, todos aprendemos a nuestro ritmo. ¡Sigamos intentando!",
        "No pasa nada, vamos a intentarlo otra vez. ¡Confío en ti!"
    ];
    
    activityInstructions = {
        colores: [
            "Vamos a aprender los colores. ¿Puedes decirme qué color es este?",
            "¡Excelente! Ahora vamos a identificar colores. ¿Qué color ves aquí?",
            "Los colores son muy divertidos. ¿Puedes nombrar este color?"
        ],
        numeros: [
            "Vamos a contar números. ¿Puedes contar conmigo?",
            "¡Perfecto! Ahora vamos a aprender números. ¿Cuántos hay aquí?",
            "Los números son importantes. ¿Puedes decirme qué número es este?"
        ],
        lenguaje: [
            "Vamos a practicar palabras. ¿Puedes repetir después de mí?",
            "¡Muy bien! Ahora vamos a aprender nuevas palabras. ¿Puedes decir...?",
            "Las palabras son divertidas. ¿Puedes pronunciar esta palabra?"
        ]
    };
    
    // Métodos de conveniencia
    greet() {
        const greeting = this.greetings[Math.floor(Math.random() * this.greetings.length)];
        this.speak(greeting);
    }
    
    encourage() {
        const encouragement = this.encouragements[Math.floor(Math.random() * this.encouragements.length)];
        this.speak(encouragement);
    }
    
    correct() {
        const correction = this.corrections[Math.floor(Math.random() * this.corrections.length)];
        this.speak(correction);
    }
    
    giveInstruction(activityType) {
        const instructions = this.activityInstructions[activityType] || this.activityInstructions.lenguaje;
        const instruction = instructions[Math.floor(Math.random() * instructions.length)];
        this.speak(instruction);
    }
    
    // Control de audio
    enable() {
        this.isEnabled = true;
        console.log('🔊 Audio habilitado');
    }
    
    disable() {
        this.isEnabled = false;
        this.synth.cancel();
        console.log('🔇 Audio deshabilitado');
    }
    
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        this.voiceConfig.volume = this.volume;
        this.saveVoiceConfig();
        console.log('🔊 Volumen:', this.volume);
    }
    
    // Métodos de configuración de voz
    setVoiceGender(gender) {
        this.voiceConfig.gender = gender;
        this.saveVoiceConfig();
        this.loadVoices(); // Recargar voces con nueva configuración
        console.log('👤 Género de voz configurado:', gender);
    }
    
    setVoiceLanguage(language) {
        this.voiceConfig.language = language;
        this.saveVoiceConfig();
        this.loadVoices(); // Recargar voces con nueva configuración
        console.log('🌍 Idioma de voz configurado:', language);
    }
    
    setVoiceSpeed(speed) {
        this.voiceConfig.speed = Math.max(0.1, Math.min(2.0, speed));
        this.saveVoiceConfig();
        console.log('⚡ Velocidad de voz configurada:', this.voiceConfig.speed);
    }
    
    setVoicePitch(pitch) {
        this.voiceConfig.pitch = Math.max(0.0, Math.min(2.0, pitch));
        this.saveVoiceConfig();
        console.log('🎵 Tono de voz configurado:', this.voiceConfig.pitch);
    }
    
    getVoiceConfig() {
        return { ...this.voiceConfig };
    }
    
    getAvailableVoices() {
        return this.voices.map(voice => ({
            name: voice.name,
            lang: voice.lang,
            gender: this.detectVoiceGender(voice.name),
            isCurrent: voice === this.currentVoice
        }));
    }
    
    detectVoiceGender(voiceName) {
        const name = voiceName.toLowerCase();
        const femaleNames = ['female', 'mujer', 'woman', 'maria', 'carmen', 'lucia', 'sofia', 'ana'];
        const maleNames = ['male', 'hombre', 'man', 'carlos', 'juan', 'pedro', 'luis', 'miguel'];
        
        if (femaleNames.some(female => name.includes(female))) return 'female';
        if (maleNames.some(male => name.includes(male))) return 'male';
        return 'unknown';
    }
    
    // Sonidos de efectos
    playSuccessSound() {
        // Crear un sonido de éxito simple
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime); // Do
        oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime + 0.1); // Mi
        oscillator.frequency.setValueAtTime(783.99, audioContext.currentTime + 0.2); // Sol
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    }
    
    playErrorSound() {
        // Sonido de error suave
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(200, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(150, audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
    }
}

// Instancia global del sistema de audio
window.audioSystem = new AudioSystem();

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AudioSystem;
}
