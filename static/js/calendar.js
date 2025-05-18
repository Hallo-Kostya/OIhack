class Calendar {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentDate = new Date();
        this.events = [];
        this.userId = 1; // Здесь нужно установить реальный ID пользователя
        this.init();
    }

    init() {
        this.renderCalendar();
        this.loadEvents();
    }

    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        
        const calendarHTML = `
            <div class="calendar-header">
                <button class="nav-btn" id="prevMonth">←</button>
                <h2>${this.getMonthName(month)} ${year}</h2>
                <button class="nav-btn" id="nextMonth">→</button>
            </div>
            <div class="calendar-grid">
                <div class="weekday">Пн</div>
                <div class="weekday">Вт</div>
                <div class="weekday">Ср</div>
                <div class="weekday">Чт</div>
                <div class="weekday">Пт</div>
                <div class="weekday">Сб</div>
                <div class="weekday">Вс</div>
                ${this.generateDaysHTML(firstDay, lastDay)}
            </div>
            <div id="eventModal" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h3>События на <span id="selectedDate"></span></h3>
                    <div id="eventsList"></div>
                    <button class="add-event-btn" onclick="calendar.showAddEventForm()">Добавить событие</button>
                </div>
            </div>
            <div id="addEventModal" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h3>Добавить событие</h3>
                    <form id="addEventForm" class="event-form">
                        <div class="form-group">
                            <label for="eventTitle">Название:</label>
                            <input type="text" id="eventTitle" required>
                        </div>
                        <div class="form-group">
                            <label for="eventStartTime">Время начала:</label>
                            <input type="time" id="eventStartTime" required>
                        </div>
                        <div class="form-group">
                            <label for="eventEndTime">Время окончания:</label>
                            <input type="time" id="eventEndTime" required>
                        </div>
                        <div class="form-group">
                            <label for="eventDescription">Описание:</label>
                            <textarea id="eventDescription"></textarea>
                        </div>
                        <div class="form-group">
                            <label for="eventLocation">Место:</label>
                            <input type="text" id="eventLocation">
                        </div>
                        <button type="submit" class="submit-btn">Создать событие</button>
                    </form>
                </div>
            </div>
        `;
        
        this.container.innerHTML = calendarHTML;
        this.attachEventListeners();
    }

    generateDaysHTML(firstDay, lastDay) {
        let daysHTML = '';
        const firstDayIndex = (firstDay.getDay() + 6) % 7;
        
        // Добавляем пустые ячейки для выравнивания
        for (let i = 0; i < firstDayIndex; i++) {
            daysHTML += '<div class="day empty"></div>';
        }
        
        // Добавляем дни месяца
        for (let day = 1; day <= lastDay.getDate(); day++) {
            const date = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), day);
            const hasEvents = this.hasEventsOnDate(date);
            daysHTML += `
                <div class="day ${hasEvents ? 'has-events' : ''}" 
                     data-date="${date.toISOString().split('T')[0]}">
                    ${day}
                </div>
            `;
        }
        
        return daysHTML;
    }

    hasEventsOnDate(date) {
        return this.events.some(event => {
            const eventDate = new Date(event.start_time);
            return eventDate.toDateString() === date.toDateString();
        });
    }

    async loadEvents() {
        try {
            const response = await fetch('/api/events');
            const data = await response.json();
            this.events = data;
            this.renderCalendar();
        } catch (error) {
            console.error('Ошибка при загрузке событий:', error);
        }
    }

    showEvents(date) {
        const modal = document.getElementById('eventModal');
        const selectedDateSpan = document.getElementById('selectedDate');
        const eventsList = document.getElementById('eventsList');
        
        selectedDateSpan.textContent = date.toLocaleDateString('ru-RU');
        
        const dayEvents = this.events.filter(event => {
            const eventDate = new Date(event.start_time);
            return eventDate.toDateString() === date.toDateString();
        });
        
        if (dayEvents.length === 0) {
            eventsList.innerHTML = '<p>Нет событий на этот день</p>';
        } else {
            eventsList.innerHTML = dayEvents.map(event => `
                <div class="event-item ${event.is_bitrix ? 'bitrix-event' : 'user-event'}">
                    <h4>${event.title}</h4>
                    <p>${event.description || ''}</p>
                    <p>Время: ${new Date(event.start_time).toLocaleTimeString()} - 
                              ${new Date(event.end_time).toLocaleTimeString()}</p>
                    ${event.location ? `<p>Место: ${event.location}</p>` : ''}
                    ${!event.is_bitrix ? `
                        <button class="delete-event-btn" onclick="calendar.deleteEvent('${event.id}')">
                            Удалить
                        </button>
                    ` : ''}
                </div>
            `).join('');
        }
        
        modal.style.display = 'block';
    }

    showAddEventForm() {
        const modal = document.getElementById('addEventModal');
        const form = document.getElementById('addEventForm');
        const selectedDate = document.getElementById('selectedDate').textContent;
        
        // Устанавливаем текущую дату
        this.selectedDateForNewEvent = selectedDate;
        
        // Очищаем форму
        form.reset();
        
        // Показываем модальное окно
        modal.style.display = 'block';
        
        // Закрываем окно со списком событий
        document.getElementById('eventModal').style.display = 'none';
    }

    async deleteEvent(eventId) {
        if (!confirm('Вы уверены, что хотите удалить это событие?')) {
            return;
        }

        try {
            const response = await fetch(`/api/events/${eventId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Ошибка при удалении события');
            }
            
            // Закрываем модальное окно
            document.getElementById('eventModal').style.display = 'none';
            
            // Перезагружаем события
            await this.loadEvents();
            
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось удалить событие');
        }
    }

    async createEvent(eventData) {
        try {
            const response = await fetch('/api/events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...eventData,
                    user_id: this.userId
                })
            });
            
            if (!response.ok) {
                throw new Error('Ошибка при создании события');
            }
            
            // Закрываем модальное окно
            document.getElementById('addEventModal').style.display = 'none';
            
            // Перезагружаем события
            await this.loadEvents();
            
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось создать событие');
        }
    }

    attachEventListeners() {
        // Обработчики для кнопок навигации
        const prevMonthBtn = document.getElementById('prevMonth');
        const nextMonthBtn = document.getElementById('nextMonth');
        
        if (prevMonthBtn) {
            prevMonthBtn.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                this.renderCalendar();
                this.loadEvents();
            });
        }
        
        if (nextMonthBtn) {
            nextMonthBtn.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                this.renderCalendar();
                this.loadEvents();
            });
        }

        // Обработчики для дней календаря
        const days = this.container.querySelectorAll('.day:not(.empty)');
        days.forEach(day => {
            day.addEventListener('click', () => {
                const date = new Date(day.dataset.date);
                this.showEvents(date);
            });
        });

        // Закрытие модальных окон
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', () => {
                document.querySelectorAll('.modal').forEach(modal => {
                    modal.style.display = 'none';
                });
            });
        });

        // Обработка формы создания события
        const addEventForm = document.getElementById('addEventForm');
        if (addEventForm) {
            addEventForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const startTime = document.getElementById('eventStartTime').value;
                const endTime = document.getElementById('eventEndTime').value;
                
                const eventData = {
                    title: document.getElementById('eventTitle').value,
                    start_time: `${this.selectedDateForNewEvent}T${startTime}:00`,
                    end_time: `${this.selectedDateForNewEvent}T${endTime}:00`,
                    description: document.getElementById('eventDescription').value,
                    location: document.getElementById('eventLocation').value
                };
                
                await this.createEvent(eventData);
            });
        }

        // Закрытие модальных окон при клике вне их содержимого
        window.addEventListener('click', (e) => {
            document.querySelectorAll('.modal').forEach(modal => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        });
    }

    getMonthName(month) {
        const months = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ];
        return months[month];
    }
}

// Инициализация календаря
const calendar = new Calendar('calendar'); 