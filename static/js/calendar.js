document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    
    const calendarEl = document.getElementById('calendar');
    console.log('Calendar element:', calendarEl);
    
    if (!calendarEl) {
        console.error('Calendar element not found!');
        return;
    }

    const eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
    const eventDetailsModal = new bootstrap.Modal(document.getElementById('eventDetailsModal'));
    const eventForm = document.getElementById('eventForm');
    const saveEventBtn = document.getElementById('saveEvent');
    const deleteEventBtn = document.getElementById('deleteEventBtn');
    
    console.log('Delete button element:', deleteEventBtn);
    
    // Получаем ID пользователя из localStorage
    const userId = parseInt(localStorage.getItem('userId'));
    console.log('User ID from localStorage:', userId, 'Type:', typeof userId);
    
    if (!userId || isNaN(userId) || userId <= 0) {
        console.log('Invalid user ID, redirecting to login');
        window.location.href = '/login.html';
        return;
    }

    // Глобальная переменная для хранения текущего события
    let currentEvent = null;

    // Глобальная функция для удаления события
    window.deleteCurrentEvent = function() {
        console.log('Delete button clicked');
        if (currentEvent && confirm('Удалить это событие?')) {
            console.log('Deleting event:', currentEvent.id);
            fetch(`http://localhost:8000/api/events/${currentEvent.id}`, {
                method: 'DELETE'
            })
            .then(response => {
                console.log('Delete response:', response);
                if (!response.ok) throw new Error('Ошибка при удалении события');
                eventDetailsModal.hide();
                calendar.refetchEvents();
            })
            .catch(error => {
                console.error('Ошибка при удалении:', error);
                alert('Не удалось удалить событие');
            });
        }
    };

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        locale: 'ru',
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        height: 'auto',
        
        // При выборе даты
        select: function(info) {
            // Форматируем даты для input[type="datetime-local"]
            const startDate = new Date(info.start);
            const endDate = new Date(info.end);
            
            // Устанавливаем время на начало и конец дня
            startDate.setHours(0, 0, 0, 0);
            endDate.setHours(23, 59, 59, 999);
            
            // Форматируем даты в формат YYYY-MM-DDThh:mm
            const formatDate = (date) => {
                return date.toISOString().slice(0, 16);
            };
            
            document.getElementById('eventStart').value = formatDate(startDate);
            document.getElementById('eventEnd').value = formatDate(endDate);
            eventModal.show();
        },
        
        // При клике на событие
        eventClick: function(info) {
            console.log('Event clicked:', info.event);
            console.log('Event user_id:', info.event.extendedProps.user_id);
            console.log('Current user_id:', userId);
            
            // Сохраняем текущее событие
            currentEvent = info.event;
            
            // Заполняем модальное окно деталями события
            document.getElementById('eventDetailsTitle').textContent = info.event.title;
            document.getElementById('eventDetailsDescription').textContent = info.event.extendedProps.description || 'Нет описания';
            document.getElementById('eventDetailsLocation').textContent = info.event.extendedProps.location || 'Место не указано';
            document.getElementById('eventDetailsStart').textContent = new Date(info.event.start).toLocaleString('ru-RU');
            document.getElementById('eventDetailsEnd').textContent = new Date(info.event.end).toLocaleString('ru-RU');
            
            // Показываем кнопку удаления только для своих событий
            if (parseInt(info.event.extendedProps.user_id) === userId) {
                console.log('Showing delete button');
                deleteEventBtn.style.display = 'inline-block';
            } else {
                console.log('Hiding delete button');
                deleteEventBtn.style.display = 'none';
            }
            
            eventDetailsModal.show();
        },
        
        // Загрузка событий
        events: function(info, successCallback, failureCallback) {
            fetch('http://localhost:8000/api/events')
                .then(response => response.json())
                .then(data => {
                    console.log('Received events:', data);
                    const events = data.map(event => ({
                        id: event.id,
                        title: event.title,
                        start: event.start,
                        end: event.end,
                        description: event.description,
                        location: event.location,
                        backgroundColor: event.is_bitrix ? '#ff4444' : '#3788d8',
                        borderColor: event.user_id == userId ? '#3788d8' : '#ff4444',
                        textColor: '#ffffff',
                        extendedProps: {
                            description: event.description,
                            location: event.location,
                            user_id: event.user_id,
                            is_bitrix: event.is_bitrix
                        }
                    }));
                    console.log('Processed events:', events);
                    successCallback(events);
                })
                .catch(error => {
                    console.error('Ошибка при загрузке событий:', error);
                    failureCallback(error);
                });
        }
    });

    console.log('Calendar instance created');
    calendar.render();
    console.log('Calendar rendered');

    // Обработчик сохранения события
    saveEventBtn.addEventListener('click', function() {
        // Получаем значения из формы
        const title = document.getElementById('eventTitle').value.trim();
        const description = document.getElementById('eventDescription').value.trim();
        const location = document.getElementById('eventLocation').value.trim();
        const startDate = new Date(document.getElementById('eventStart').value);
        const endDate = new Date(document.getElementById('eventEnd').value);
        
        // Проверяем обязательные поля
        if (!title) {
            alert('Пожалуйста, введите название события');
            return;
        }
        
        if (!startDate || isNaN(startDate.getTime())) {
            alert('Пожалуйста, выберите дату начала');
            return;
        }
        
        if (!endDate || isNaN(endDate.getTime())) {
            alert('Пожалуйста, выберите дату окончания');
            return;
        }
        
        if (endDate <= startDate) {
            alert('Дата окончания должна быть позже даты начала');
            return;
        }

        // Форматируем даты в ISO формат
        const formatDate = (date) => {
            return date.toISOString().replace('.000Z', 'Z');
        };

        const eventData = {
            title: title,
            description: description || '',
            location: location || '',
            start_date: formatDate(startDate),
            end_date: formatDate(endDate)
        };

        console.log('Saving event:', eventData);
        console.log('User ID:', userId);

        fetch(`http://localhost:8000/api/addevent?user_id=${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(eventData)
        })
        .then(response => {
            console.log('Save event response status:', response.status);
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`Ошибка при создании события: ${text}`);
                });
            }
            eventModal.hide();
            eventForm.reset();
            calendar.refetchEvents();
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(error.message || 'Не удалось создать событие');
        });
    });
}); 