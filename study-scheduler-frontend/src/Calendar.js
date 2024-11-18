import React, { useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';

const CalendarComponent = () => {
    const [events, setEvents] = useState([]);

    const handleEventClick = (eventInfo) => {
        alert(`Task: ${eventInfo.event.title}`);
    };

    return (
        <FullCalendar
            plugins={[dayGridPlugin]}
            initialView="dayGridMonth"
            events={events}
            eventClick={handleEventClick}
        />
    );
};

export default CalendarComponent;
