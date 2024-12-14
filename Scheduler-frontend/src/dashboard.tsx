'use client'

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ChevronDown, LogOut, Settings, Plus, User } from 'lucide-react'
import ModernCalendar from './modern-calendar'
import { Flashcard } from './components/Flashcard';

interface Subject {
  id: number;
  name: string;
  progress: number;
  flashcards_total: number;
  flashcards_studied: number;
  allocated_day: string;
}

interface UserData {
  id: number;
  name: string;
  email: string;
  study_hours: number;
  study_time: string;
  subjects: Subject[];
}

interface Flashcard {
  id: number;
  question: string;
  answer: string;
}

export default function Dashboard() {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null);
  const [isFlashcardOpen, setIsFlashcardOpen] = useState(false);
  const [currentFlashcardIndex, setCurrentFlashcardIndex] = useState(0);
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isAddingSubject, setIsAddingSubject] = useState(false);
  const [newSubject, setNewSubject] = useState<{ name: string; file: File | null; allocatedDay: string }>({
    name: '',
    file: null,
    allocatedDay: ''
  });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:5000/test_user_data/1');
        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        } else {
          throw new Error('Failed to fetch user data');
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        setError('Failed to load user data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  const handleSubjectClick = (subject: Subject) => {
    setSelectedSubject(subject);
    setIsFlashcardOpen(true);
    setCurrentFlashcardIndex(0);
    // Fetch flashcards for the selected subject
    // This is a placeholder. Replace with actual API call.
    setFlashcards([
      { id: 1, question: "What is the capital of France?", answer: "Paris" },
      { id: 2, question: "What is 2 + 2?", answer: "4" },
      // Add more flashcards as needed
    ]);
  };

  const handleNextFlashcard = () => {
    if (currentFlashcardIndex < flashcards.length - 1) {
      setCurrentFlashcardIndex(currentFlashcardIndex + 1);
    }
  };

  const handlePreviousFlashcard = () => {
    if (currentFlashcardIndex > 0) {
      setCurrentFlashcardIndex(currentFlashcardIndex - 1);
    }
  };

  const handleCloseFlashcards = () => {
    setIsFlashcardOpen(false);
    setSelectedSubject(null);
  };

  const handleAddSubject = async () => {
    if (newSubject.name && newSubject.file && newSubject.allocatedDay) {
      const formData = new FormData();
      formData.append('name', newSubject.name);
      formData.append('file', newSubject.file);
      formData.append('allocatedDay', newSubject.allocatedDay);

      try {
        const response = await fetch('http://localhost:5000/add_subject', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const newSubjectData = await response.json();
          setUserData(prevData => ({
            ...prevData!,
            subjects: [...prevData!.subjects, newSubjectData]
          }));
          setNewSubject({ name: '', file: null, allocatedDay: '' });
          setIsAddingSubject(false);
        } else {
          throw new Error('Failed to add subject');
        }
      } catch (error) {
        console.error('Error adding subject:', error);
        // Handle error (e.g., show error message to user)
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    setNewSubject(prev => ({
      ...prev,
      file: file ? file : null
    }));
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="flex items-center justify-center h-screen text-red-500">{error}</div>;
  }

  if (!userData) {
    return <div className="flex items-center justify-center h-screen">No user data available</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Study Dashboard</h1>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="flex items-center space-x-2">
                <User className="h-5 w-5" />
                <span>{userData.name}</span>
                <ChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                <span>Preferences</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleLogout}>
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-900">Your Subjects</h2>
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
                    <Label htmlFor="allocatedDay" className="text-right">
                      Study Day
                    </Label>
                    <Select
                      onValueChange={(value) => setNewSubject({ ...newSubject, allocatedDay: value })}
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
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {userData.subjects.map((subject) => (
              <Card key={subject.id} className="hover:shadow-lg transition-shadow duration-200">
                <CardHeader>
                  <CardTitle>{subject.name}</CardTitle>
                  <CardDescription>Allocated Day: {subject.allocated_day}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Progress value={subject.progress} className="w-full" />
                  <p className="mt-2">Progress: {subject.progress}%</p>
                  <p>Flashcards: {subject.flashcards_studied} / {subject.flashcards_total}</p>
                </CardContent>
                <CardFooter>
            <Button onClick={() => handleSubjectClick(subject)}>View Flashcards</Button>
          </CardFooter>
        </Card>
      ))}
      {isFlashcardOpen && selectedSubject && flashcards.length > 0 && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card className="w-96 h-64 relative">
            <div className="h-full flex flex-col items-center justify-center p-4">
              <p className="text-lg font-semibold text-center mb-4">{flashcards[currentFlashcardIndex].question}</p>
              <Button onClick={() => setIsFlipped(!isFlipped)}>
                {isFlipped ? 'Show Question' : 'Show Answer'}
              </Button>
              {isFlipped && (
                <p className="mt-4 text-center">{flashcards[currentFlashcardIndex].answer}</p>
              )}
            </div>
            <div className="absolute bottom-4 left-0 right-0 flex justify-center space-x-4">
              <Button onClick={handlePreviousFlashcard} disabled={currentFlashcardIndex === 0}>
                Previous
              </Button>
              <Button onClick={handleNextFlashcard} disabled={currentFlashcardIndex === flashcards.length - 1}>
                Next
              </Button>
            </div>
            <Button className="absolute top-2 right-2" variant="ghost" onClick={handleCloseFlashcards}>
              Close
            </Button>
          </Card>
        </div>
      )}
        </div>
        <div className="mt-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Your Schedule</h2>
            <ModernCalendar />
          </div>
        </div>
      </main>
    </div>
  );
}

