document.addEventListener('DOMContentLoaded', function() {
    // Плавний скрол до секцій
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const section = document.querySelector(this.getAttribute('href'));
            const headerOffset = 80;
            const elementPosition = section.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });

            // Додаємо активний клас для навігації
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Підсвічування активної секції при скролі
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section');
        const navLinks = document.querySelectorAll('.nav-btn');
        
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - 150) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    });

    let currentSlide = 1;
    const totalSlides = 5;
    let slideInterval;

    // Функція для перемикання слайдів
    function switchSlide(slideNumber) {
        document.getElementById(`switch${slideNumber}`).checked = true;
        currentSlide = slideNumber;
    }

    // Функція для автоматичного перемикання
    function startSlideshow() {
        slideInterval = setInterval(() => {
            currentSlide = currentSlide >= totalSlides ? 1 : currentSlide + 1;
            switchSlide(currentSlide);
        }, 4000); // Перемикає кожні 4 секунди
    }

    // Додаємо обробники подій для кнопок
    document.querySelectorAll('#controls label').forEach(label => {
        label.addEventListener('click', function() {
            // Отримуємо номер слайду з атрибута for (switch1 -> 1)
            const slideNumber = parseInt(this.getAttribute('for').replace('switch', ''));
            switchSlide(slideNumber);
            
            // Перезапускаємо автоматичне перемикання
            clearInterval(slideInterval);
            startSlideshow();
        });
    });

    // Запускаємо автоматичне перемикання при завантаженні
    startSlideshow();
}); 