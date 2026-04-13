// ===== Таймер обратного отсчёта на JavaScript =====

class CountdownTimer {
    constructor() {
        // DOM-элементы
        this.minutesInput = document.getElementById('minutes');
        this.secondsInput = document.getElementById('seconds');
        this.timerDisplay = document.getElementById('timerDisplay');
        this.statusMessage = document.getElementById('statusMessage');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.themeToggle = document.getElementById('themeToggle');

        // Переменные состояния
        this.timeLeft = 0; // Оставшееся время в секундах
        this.totalTime = 0; // Исходное время в секундах
        this.isRunning = false; // Запущен ли таймер
        this.intervalId = null; // ID интервала

        // Инициализация
        this.init();
    }

    // ===== Инициализация =====
    init() {
        // Обработчики событий кнопок
        this.startBtn.addEventListener('click', () => this.start());
        this.pauseBtn.addEventListener('click', () => this.pause());
        this.resetBtn.addEventListener('click', () => this.reset());

        // Обработчики для полей ввода
        this.minutesInput.addEventListener('change', () => this.onInputChange());
        this.secondsInput.addEventListener('change', () => this.onInputChange());
        this.minutesInput.addEventListener('input', () => this.validateAndUpdateDisplay());
        this.secondsInput.addEventListener('input', () => this.validateAndUpdateDisplay());

        // Тумблер темы
        this.themeToggle.addEventListener('change', () => this.toggleTheme());

        // Восстановление темы из localStorage
        this.restoreTheme();

        // Инициализация отображения
        this.updateDisplay();
    }

    // ===== Валидация и обработка ввода =====
    validateInput(input, maxValue) {
        let value = parseInt(input.value) || 0;

        // Проверка на отрицательные числа
        if (value < 0) {
            value = 0;
        }

        // Проверка на превышение максимума
        if (value > maxValue) {
            value = maxValue;
        }

        // Обновление значения с нулевым заполнением
        input.value = String(value).padStart(2, '0');
        return value;
    }

    validateAndUpdateDisplay() {
        // Валидация обоих полей
        const minutes = this.validateInput(this.minutesInput, 59);
        const seconds = this.validateInput(this.secondsInput, 59);

        // Обновление отображения
        this.timeLeft = minutes * 60 + seconds;
        this.updateDisplay();
    }

    // ===== Обработка изменения входных данных во время работы =====
    onInputChange() {
        // Если таймер работает, игнорируем изменения и выводим сообщение
        if (this.isRunning) {
            this.showStatus('⚠️ Сброс при изменении времени', 'warning');
            this.reset();
        } else {
            // Если таймер не работает, просто валидируем
            this.validateAndUpdateDisplay();
        }
    }

    // ===== Запуск таймера =====
    start() {
        // Валидация перед стартом
        this.validateAndUpdateDisplay();

        // Если таймер уже запущен или время = 0
        if (this.isRunning || this.timeLeft <= 0) {
            return;
        }

        // Запоминаем исходное время
        this.totalTime = this.timeLeft;

        // Запускаем интервал
        this.isRunning = true;
        this.updateButtonStates();
        this.clearStatusMessage();

        this.intervalId = setInterval(() => {
            this.timeLeft--;

            // Обновляем отображение
            this.updateDisplay();

            // Проверяем, закончилось ли время
            if (this.timeLeft <= 0) {
                this.timerFinished();
            }
        }, 1000); // Обновление каждую секунду
    }

    // ===== Пауза таймера =====
    pause() {
        if (!this.isRunning) {
            return;
        }

        // Останавливаем интервал
        clearInterval(this.intervalId);
        this.isRunning = false;

        this.updateButtonStates();
        this.showStatus('⏸️ Таймер на паузе', 'warning');
    }

    // ===== Сброс таймера =====
    reset() {
        // Останавливаем интервал если работает
        if (this.isRunning) {
            clearInterval(this.intervalId);
            this.isRunning = false;
        }

        // Валидируем входные данные
        this.validateAndUpdateDisplay();

        // Сбрасываем состояние
        this.clearStatusMessage();
        this.updateButtonStates();
    }

    // ===== Таймер закончился =====
    timerFinished() {
        // Останавливаем интервал
        clearInterval(this.intervalId);
        this.isRunning = false;

        // Убеждаемся, что отображаем 00:00
        this.timeLeft = 0;
        this.updateDisplay();

        // Выводим сообщение о завершении
        this.showStatus('🎉 Время вышло!', 'alert');

        // Воспроизводим звуковой сигнал
        this.playAlertSound();

        // Обновляем состояние кнопок
        this.updateButtonStates();
    }

    // ===== Звуковой сигнал =====
    playAlertSound() {
        try {
            // Используем Web Audio API для создания звука
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            // Параметры звука
            oscillator.frequency.value = 800; // Частота в Hz
            oscillator.type = 'sine'; // Волна

            // Громкость и длительность
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (error) {
            // Fallback на alert если Web Audio недоступен
            console.log('Web Audio API недоступен, используем alert');
        }
    }

    // ===== Обновление отображения таймера =====
    updateDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;

        // Форматируем с ведущими нулями
        const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        this.timerDisplay.textContent = formattedTime;
    }

    // ===== Обновление состояния кнопок =====
    updateButtonStates() {
        this.startBtn.disabled = this.isRunning || this.timeLeft <= 0;
        this.pauseBtn.disabled = !this.isRunning;
    }

    // ===== Показать сообщение о состоянии =====
    showStatus(message, className = '') {
        this.statusMessage.textContent = message;
        this.statusMessage.className = `status-message ${className}`;
    }

    // ===== Очистить сообщение о состоянии =====
    clearStatusMessage() {
        this.statusMessage.textContent = '';
        this.statusMessage.className = 'status-message';
    }

    // ===== Переключить тему =====
    toggleTheme() {
        const isDarkTheme = this.themeToggle.checked;
        const body = document.body;

        if (isDarkTheme) {
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        }
    }

    // ===== Восстановить тему из localStorage =====
    restoreTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        const isDarkTheme = savedTheme === 'dark';

        this.themeToggle.checked = isDarkTheme;

        if (isDarkTheme) {
            document.body.classList.add('dark-theme');
        }
    }
}

// ===== Инициализация при загрузке DOM =====
document.addEventListener('DOMContentLoaded', () => {
    new CountdownTimer();
});
