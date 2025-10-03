// -*- coding: utf-8 -*-
/**
 * Sistema de Reconocimiento de Voz para TEA Edition
 * Permite al avatar escuchar y responder al niño
 */

class VoiceRecognition {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.isSupported = false;
        this.language = 'es-ES';
        this.continuous = false;
        this.interimResults = true;
        this.maxAlternatives = 1;
        
        // Configuraciones
        this.config = {
            enabled: true,
            autoStart: false,
            timeout: 5000, // 5 segundos de silencio antes de parar
            confidence: 0.7, // Confianza mínima para aceptar resultado
            language: 'es-ES'
        };
        
        // Callbacks
        this.onResult = null;
        this.onError = null;
        this.onStart = null;
        this.onEnd = null;
        
        this.init();
    }
    
    init() {
        // Verificar soporte del navegador
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.isSupported = true;
        } else if ('SpeechRecognition' in window) {
            this.recognition = new SpeechRecognition();
            this.isSupported = true;
        } else {
            console.warn('❌ Reconocimiento de voz no soportado en este navegador');
            this.isSupported = false;
            return;
        }
        
        // Configurar reconocimiento
        this.setupRecognition();
        
        // Cargar configuración guardada
        this.loadConfig();
        
        console.log('🎤 Sistema de Reconocimiento de Voz inicializado');
    }
    
    setupRecognition() {
        if (!this.recognition) return;
        
        // Configuración básica
        this.recognition.continuous = this.continuous;
        this.recognition.interimResults = this.interimResults;
        this.recognition.lang = this.language;
        this.recognition.maxAlternatives = this.maxAlternatives;
        
        // Eventos
        this.recognition.onstart = () => {
            this.isListening = true;
            console.log('🎤 Escuchando...');
            this.onStart?.();
        };
        
        this.recognition.onresult = (event) => {
            this.handleResult(event);
        };
        
        this.recognition.onerror = (event) => {
            console.error('❌ Error de reconocimiento:', event.error);
            this.isListening = false;
            this.onError?.(event);
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            console.log('🔇 Dejó de escuchar');
            this.onEnd?.();
        };
        
        this.recognition.onspeechstart = () => {
            console.log('🗣️ Detectado inicio de habla');
        };
        
        this.recognition.onspeechend = () => {
            console.log('🔇 Detectado fin de habla');
        };
        
        this.recognition.onsoundstart = () => {
            console.log('🔊 Detectado sonido');
        };
        
        this.recognition.onsoundend = () => {
            console.log('🔇 Fin de sonido');
        };
    }
    
    handleResult(event) {
        let finalTranscript = '';
        let interimTranscript = '';
        
        // Procesar resultados
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            const confidence = event.results[i][0].confidence;
            
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
                console.log('✅ Resultado final:', transcript, 'Confianza:', confidence);
                
                // Solo procesar si la confianza es suficiente
                if (confidence >= this.config.confidence) {
                    this.onResult?.(transcript, confidence, 'final');
                }
            } else {
                interimTranscript += transcript;
                console.log('⏳ Resultado temporal:', transcript);
                this.onResult?.(transcript, confidence, 'interim');
            }
        }
    }
    
    // Métodos públicos
    startListening() {
        if (!this.isSupported) {
            console.error('❌ Reconocimiento de voz no soportado');
            return false;
        }
        
        if (this.isListening) {
            console.log('⚠️ Ya está escuchando');
            return false;
        }
        
        try {
            this.recognition.start();
            return true;
        } catch (error) {
            console.error('❌ Error iniciando reconocimiento:', error);
            return false;
        }
    }
    
    stopListening() {
        if (!this.isListening) {
            console.log('⚠️ No está escuchando');
            return false;
        }
        
        try {
            this.recognition.stop();
            return true;
        } catch (error) {
            console.error('❌ Error deteniendo reconocimiento:', error);
            return false;
        }
    }
    
    toggleListening() {
        if (this.isListening) {
            return this.stopListening();
        } else {
            return this.startListening();
        }
    }
    
    // Configuración
    setLanguage(language) {
        this.language = language;
        this.config.language = language;
        if (this.recognition) {
            this.recognition.lang = language;
        }
        this.saveConfig();
        console.log('🌍 Idioma de reconocimiento configurado:', language);
    }
    
    setConfidence(confidence) {
        this.config.confidence = Math.max(0.1, Math.min(1.0, confidence));
        this.saveConfig();
        console.log('🎯 Confianza mínima configurada:', this.config.confidence);
    }
    
    setContinuous(continuous) {
        this.continuous = continuous;
        if (this.recognition) {
            this.recognition.continuous = continuous;
        }
        console.log('🔄 Modo continuo:', continuous ? 'activado' : 'desactivado');
    }
    
    // Configuración persistente
    loadConfig() {
        const savedConfig = localStorage.getItem('tea_voice_recognition_config');
        if (savedConfig) {
            try {
                const config = JSON.parse(savedConfig);
                this.config = { ...this.config, ...config };
                
                // Aplicar configuración
                this.setLanguage(this.config.language);
                this.setConfidence(this.config.confidence);
                
                console.log('🔧 Configuración de reconocimiento cargada:', this.config);
            } catch (error) {
                console.error('❌ Error cargando configuración de reconocimiento:', error);
            }
        }
    }
    
    saveConfig() {
        try {
            localStorage.setItem('tea_voice_recognition_config', JSON.stringify(this.config));
            console.log('💾 Configuración de reconocimiento guardada:', this.config);
        } catch (error) {
            console.error('❌ Error guardando configuración de reconocimiento:', error);
        }
    }
    
    // Estado
    isSupported() {
        return this.isSupported;
    }
    
    isCurrentlyListening() {
        return this.isListening;
    }
    
    getConfig() {
        return { ...this.config };
    }
    
    // Métodos de conveniencia para actividades
    startListeningForActivity(activityType, onResult) {
        this.onResult = onResult;
        
        // Configurar según el tipo de actividad
        switch(activityType) {
            case 'colores':
                this.setLanguage('es-ES');
                this.setConfidence(0.6); // Más permisivo para niños
                break;
            case 'numeros':
                this.setLanguage('es-ES');
                this.setConfidence(0.7);
                break;
            case 'lenguaje':
                this.setLanguage('es-ES');
                this.setConfidence(0.8); // Más estricto para pronunciación
                break;
            default:
                this.setLanguage('es-ES');
                this.setConfidence(0.7);
        }
        
        return this.startListening();
    }
    
    // Procesar respuestas específicas
    processColorResponse(transcript) {
        const colors = {
            'rojo': 'rojo',
            'azul': 'azul', 
            'verde': 'verde',
            'amarillo': 'amarillo',
            'naranja': 'naranja',
            'morado': 'morado',
            'rosa': 'rosa',
            'marrón': 'marrón',
            'café': 'marrón',
            'negro': 'negro',
            'blanco': 'blanco'
        };
        
        const lowerTranscript = transcript.toLowerCase().trim();
        
        for (const [key, value] of Object.entries(colors)) {
            if (lowerTranscript.includes(key)) {
                return value;
            }
        }
        
        return null;
    }
    
    processNumberResponse(transcript) {
        const numbers = {
            'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5,
            'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10,
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9, '10': 10
        };
        
        const lowerTranscript = transcript.toLowerCase().trim();
        
        for (const [key, value] of Object.entries(numbers)) {
            if (lowerTranscript.includes(key)) {
                return value;
            }
        }
        
        return null;
    }
    
    processWordResponse(transcript, targetWord) {
        const lowerTranscript = transcript.toLowerCase().trim();
        const lowerTarget = targetWord.toLowerCase().trim();
        
        // Verificar coincidencia exacta
        if (lowerTranscript === lowerTarget) {
            return true;
        }
        
        // Verificar si contiene la palabra objetivo
        if (lowerTranscript.includes(lowerTarget)) {
            return true;
        }
        
        // Verificar palabras similares (para errores de pronunciación)
        const similarity = this.calculateSimilarity(lowerTranscript, lowerTarget);
        return similarity > 0.7; // 70% de similitud
    }
    
    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) {
            return 1.0;
        }
        
        const distance = this.levenshteinDistance(longer, shorter);
        return (longer.length - distance) / longer.length;
    }
    
    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }
}

// Instancia global del sistema de reconocimiento de voz
window.voiceRecognition = new VoiceRecognition();

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceRecognition;
}



