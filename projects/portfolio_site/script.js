// =====================
// Обработка мобильного меню
// =====================

// Получаем элементы меню и кнопки
const menuToggle = document.getElementById('menuToggle');
const navMenu = document.getElementById('navMenu');
const navLinks = document.querySelectorAll('.nav-link');

// Функция для открытия/закрытия меню
function toggleMenu() {
    menuToggle.classList.toggle('active');
    navMenu.classList.toggle('active');
}

// Обработчик клика на кнопку меню
menuToggle.addEventListener('click', toggleMenu);

// Закрытие меню при клике на ссылку навигации
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Закрытие меню при клике вне его
document.addEventListener('click', (e) => {
    const isClickInsideMenu = navMenu.contains(e.target);
    const isClickOnToggle = menuToggle.contains(e.target);
    
    if (!isClickInsideMenu && !isClickOnToggle && navMenu.classList.contains('active')) {
        toggleMenu();
    }
});

// =====================
// Плавная прокрутка к якорям
// =====================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        // Получаем целевой элемент
        const targetId = this.getAttribute('href');
        
        // Не обрабатываем, если это просто #
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            e.preventDefault();
            
            // Плавно скроллим к элементу
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// =====================
// Эффект активной навигации при скролле
// =====================

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section');
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        // Если мы находимся в этой секции
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    // Обновляем подчёркивание активной ссылки
    navLinks.forEach(link => {
        link.style.color = '';
        link.style.borderBottomColor = '';
        
        if (link.getAttribute('href') === `#${current}`) {
            link.style.color = 'var(--color-accent)';
        }
    });
}

// Вызываем функцию при скролле
window.addEventListener('scroll', updateActiveNavLink);

// =====================
// Анимация счётчика при скролле (опционально)
// =====================

function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
    );
}

// =====================
// Инициализация при загрузке страницы
// =====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('✨ Портфолио загружено успешно!');
    
    // Можно добавить дополнительные инициализации здесь
});

// =====================
// Обработка изменения размера окна
// =====================

let lastWidth = window.innerWidth;

window.addEventListener('resize', () => {
    const currentWidth = window.innerWidth;
    
    // Если изменился размер экрана (переход между мобильным и десктопом)
    if ((lastWidth <= 640 && currentWidth > 640) || 
        (lastWidth > 640 && currentWidth <= 640)) {
        // Закрываем мобильное меню
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
    }
    
    lastWidth = currentWidth;
});

// =====================
// Мягкая загрузка изображений (если будут добавлены)
// =====================

// Для будущих изображений - добавляем эффект появления
const images = document.querySelectorAll('img');
images.forEach(img => {
    img.addEventListener('load', () => {
        img.style.opacity = '1';
    });
});

// =====================
// Отладка и логи
// =====================

// Функция для вывода информации в консоль
function logPageInfo() {
    console.log('📄 Страница портфолио');
    console.log('📱 Разрешение экрана:', window.innerWidth, 'x', window.innerHeight);
    console.log('🌙 Текущая тема: Тёмная');
}

// Раскомментируй эту строку для отладки:
// logPageInfo();
