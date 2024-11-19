'use client'

import * as React from 'react'
import { ChevronLeft, ChevronRight, Plus } from 'lucide-react'
import { addDays, format, getDay, isSameMonth, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay, isToday, parseISO } from 'date-fns'
import { Button } from "./components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./components/ui/dialog"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select"

// Mock data for recurring subjects
const recurringSubjects = [
  { name: 'Math', color: 'bg-blue-500', day: 1 }, // Monday
  { name: 'Physics', color: 'bg-green-500', day: 2 }, // Tuesday
  { name: 'Chemistry', color: 'bg-purple-500', day: 3 }, // Wednesday
  { name: 'Literature', color: 'bg-yellow-500', day: 4 }, // Thursday
  { name: 'History', color: 'bg-red-500', day: 5 }, // Friday
  { name: 'Computer Science', color: 'bg-indigo-500', day: 1 }, // Monday
]

interface Event {
  date: string
  title: string
  time: string
}

export default function ModernCalendar() {
  const [currentMonth, setCurrentMonth] = React.useState(new Date())
  const [events, setEvents] = React.useState<Event[]>([])
  const [newEvent, setNewEvent] = React.useState<Event>({ date: '', title: '', time: '' })
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)

  const firstDayOfMonth = startOfMonth(currentMonth)
  const lastDayOfMonth = endOfMonth(currentMonth)
  const startingDayIndex = getDay(firstDayOfMonth)
  const daysToAdd = startingDayIndex === 0 ? 6 : startingDayIndex - 1
  const startDate = addDays(firstDayOfMonth, -daysToAdd)

  const calendarDays = eachDayOfInterval({
    start: startDate,
    end: addDays(lastDayOfMonth, 42 - (lastDayOfMonth.getDate() + daysToAdd) % 7),
  })

  const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  const goToPreviousMonth = () => {
    setCurrentMonth(prevMonth => addDays(prevMonth, -30))
  }

  const goToNextMonth = () => {
    setCurrentMonth(prevMonth => addDays(prevMonth, 30))
  }

  const handleAddEvent = () => {
    if (newEvent.date && newEvent.title && newEvent.time) {
      setEvents([...events, newEvent])
      setNewEvent({ date: '', title: '', time: '' })
      setIsDialogOpen(false)
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="flex items-center justify-between p-4 border-b">
        <h2 className="text-2xl font-semibold text-gray-800">
          {format(currentMonth, 'MMMM yyyy')}
        </h2>
        <div className="flex space-x-2">
          <Button variant="outline" size="icon" onClick={goToPreviousMonth} aria-label="Previous month">
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon" onClick={goToNextMonth} aria-label="Next month">
            <ChevronRight className="h-4 w-4" />
          </Button>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="outline" size="icon" aria-label="Add event">
                <Plus className="h-4 w-4" />
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Add New Event</DialogTitle>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="event-date" className="text-right">
                    Date
                  </Label>
                  <Input
                    id="event-date"
                    type="date"
                    value={newEvent.date}
                    onChange={(e) => setNewEvent({ ...newEvent, date: e.target.value })}
                    className="col-span-3"
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="event-title" className="text-right">
                    Title
                  </Label>
                  <Input
                    id="event-title"
                    value={newEvent.title}
                    onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                    className="col-span-3"
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="event-time" className="text-right">
                    Time
                  </Label>
                  <Input
                    id="event-time"
                    type="time"
                    value={newEvent.time}
                    onChange={(e) => setNewEvent({ ...newEvent, time: e.target.value })}
                    className="col-span-3"
                  />
                </div>
              </div>
              <Button onClick={handleAddEvent}>Add Event</Button>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <div className="grid grid-cols-7 gap-px bg-gray-200">
        {weekDays.map(day => (
          <div key={day} className="bg-gray-50 py-2 text-center text-sm font-medium text-gray-500">
            {day}
          </div>
        ))}
        {calendarDays.map((day: Date, dayIdx: number) => {
          const dateKey = format(day, 'yyyy-MM-dd');
          const dayOfWeek = getDay(day);
          const daySubjects = recurringSubjects.filter(subject => subject.day === (dayOfWeek === 0 ? 7 : dayOfWeek));
          const dayEvents = events.filter(event => event.date === dateKey);

          return (
            <div
              key={day.toString()}
              className={`${
                !isSameMonth(day, currentMonth) ? 'bg-gray-50 text-gray-400' : 'bg-white'
              } relative py-2 px-3 h-32`}
            >
              <time
                dateTime={format(day, 'yyyy-MM-dd')}
                className={`${
                  isToday(day) ? 'bg-blue-600 text-white' : 'text-gray-700'
                } flex h-6 w-6 items-center justify-center rounded-full text-sm font-medium`}
              >
                {format(day, 'd')}
              </time>
              <ol className="mt-2">
                {daySubjects.map((subject, index) => (
                  <li key={`subject-${index}`} className="text-xs mb-1">
                    <div className={`${subject.color} text-white rounded px-1 py-0.5 truncate`}>
                      {subject.name}
                    </div>
                  </li>
                ))}
                {dayEvents.map((event, index) => (
                  <li key={`event-${index}`} className="text-xs mb-1">
                    <div className="bg-gray-200 text-gray-800 rounded px-1 py-0.5 truncate">
                      {event.time} - {event.title}
                    </div>
                  </li>
                ))}
              </ol>
            </div>
          );
        })}
      </div>
    </div>
  )
}