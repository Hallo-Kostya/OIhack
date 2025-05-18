document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;

        try {
            const response = await fetch(`/api/auth/find-employee?email=${encodeURIComponent(email)}`, {
                method: 'GET'
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('userId', data.id);
                localStorage.setItem('userName', `${data.first_name} ${data.last_name}`);
                localStorage.setItem('userEmail', data.email);

                // Перенаправляем на календарь
                window.location.href = '/static/calendar.html';
            } else {
                alert(data.detail || 'Пользователь не найден');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при входе');
        }
    });
}); 