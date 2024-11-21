'use client'

import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Button } from "./components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./components/ui/card"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"
import { Progress } from "./components/ui/progress"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "./components/ui/dropdown-menu"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "./components/ui/dialog"
import { ChevronDown, Plus, LogOut, Settings } from 'lucide-react'
import ModernCalendar from './modern-calendar'

interface Subject {
  name: string
  progress: number
  flashcards_total: number
  flashcards_studied: number
}

interface UserData {
  id: number
  name: string
  email: string
  study_hours: number
  study_time: string
  subjects: Subject[]
}

// Mock data for subjects
const initialSubjects = [
  { id: 1, name: 'Mathematics', progress: 65 },
  { id: 2, name: 'Physics', progress: 40 },
  { id: 3, name: 'Computer Science', progress: 80 },
]

// Mock flashcards data
const mockFlashcards = [
  { id: 1, summary: "The Pythagorean theorem states that in a right triangle, the square of the length of the hypotenuse is equal to the sum of the squares of the other two sides." },
  { id: 2, summary: "Newton's First Law of Motion: An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force." },
  { id: 3, summary: "Object-Oriented Programming (OOP) is a programming paradigm based on the concept of 'objects', which can contain data and code: data in the form of fields, and code in the form of procedures." },
]

export default function HomeDashboard() {
  const [userData, setUserData] = useState<UserData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        navigate('/')
        return
      }

      try {
        const response = await fetch('http://localhost:5000/user_data', {
          headers: {
            'Authorization': token
          }
        })

        if (response.ok) {
          const data = await response.json()
          setUserData(data)
        } else {
          throw new Error('Failed to fetch user data')
        }
      } catch (error) {
        console.error('Error fetching user data:', error)
        setError('Failed to load user data. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchUserData()
  }, [navigate])

  // logout function
  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>
  }

  if (error) {
    return <div className="flex items-center justify-center h-screen text-red-500">{error}</div>
  }

  const [subjects, setSubjects] = useState(initialSubjects)
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null)
  const [isAddingSubject, setIsAddingSubject] = useState(false)
  const [newSubject, setNewSubject] = useState<{ name: string; file?: File | null; studyDay: string }>({
    name: '',
    file: null,
    studyDay: ''
  })

  const handleSubjectClick = (subjectId: number) => {
    setSelectedSubject(subjectId)
  }

  const handleAddSubject = () => {
    if (newSubject.name && newSubject.studyDay) {
      setSubjects([...subjects, { id: subjects.length + 1, name: newSubject.name, progress: 0 }])
      setNewSubject({ name: '', file: null, studyDay: '' })
      setIsAddingSubject(false)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    setNewSubject(prev => ({
      ...prev,
      file: file ? file : null
    }));
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">
                Menu <ChevronDown className="ml-2 h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                <span>Settings</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <ModernCalendar />
          <div className="mt-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Your Subjects</h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {subjects.map((subject) => (
                <Card key={subject.id} className="hover:shadow-lg transition-shadow duration-200">
                  <CardHeader>
                    <CardTitle>{subject.name}</CardTitle>
                    <CardDescription>Progress: {subject.progress}%</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Progress value={subject.progress} className="w-full" />
                  </CardContent>
                  <CardFooter>
                    <Button onClick={() => handleSubjectClick(subject.id)}>Study Now</Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
            <div className="mt-8">
              <Dialog open={isAddingSubject} onOpenChange={setIsAddingSubject}>
                <DialogTrigger asChild>
                  <Button>
                    <Plus className="mr-2 h-4 w-4" /> Add New Subject
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-[425px]">
                  <DialogHeader>
                    <DialogTitle>Add New Subject</DialogTitle>
                    <DialogDescription>
                      Enter the details for your new subject here.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="name" className="text-right">
                        Name
                      </Label>
                      <Input
                        id="name"
                        value={newSubject.name}
                        onChange={(e) => setNewSubject({ ...newSubject, name: e.target.value })}
                        className="col-span-3"
                      />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="file" className="text-right">
                        PDF File
                      </Label>
                      <Input
                        id="file"
                        type="file"
                        onChange={handleFileChange}
                        className="col-span-3"
                      />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="studyDay" className="text-right">
                        Study Day
                      </Label>
                      <Select
                        onValueChange={(value) => setNewSubject({ ...newSubject, studyDay: value })}
                      >
                        <SelectTrigger className="col-span-3">
                          <SelectValue placeholder="Select a day" />
                        </SelectTrigger>
                        <SelectContent>
                          {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map((day) => (
                            <SelectItem key={day} value={day}>{day}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <DialogFooter>
                    <Button onClick={handleAddSubject}>Add Subject</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>
          <div className="mt-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Recent Flashcards</h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {mockFlashcards.map((flashcard) => (
                <Card key={flashcard.id}>
                  <CardHeader>
                    <CardTitle>Flashcard #{flashcard.id}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p>{flashcard.summary}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
