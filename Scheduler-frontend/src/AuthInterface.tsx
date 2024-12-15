'use client'

import { useState, useEffect } from 'react'
import { Button } from "./components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select"
import { useNavigate } from 'react-router-dom';



// Login Component
const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate(); // Initialize the navigation hook

  /**
   * Handles the login form submission
   * param {React.FormEvent} e - The form event object
   */
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }
  
      const data = await response.json();
      console.log('Login successful:', data);
  
      // Save the token (if returned) to localStorage or cookies for authentication
      if (data.token) {
        localStorage.setItem('token', data.token);
      }
      
      // Redirect to the dashboard
      navigate('/dashboard');

    } catch (error) {
      console.error('Error during login:', error);
      alert('Invalid email or password');
    }  
  };

  return (
    <form onSubmit={handleLogin}>
      {/* Form fields */}
    </form>
  )
}

// Multi-step Signup Component
const Signup = () => {
  const navigate = useNavigate(); // Initialize the navigation hook
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    studyHours: '',
    studyTime: '',
    subjects: [{ name: '', file: null as File | null, studyDay: '' }]
  })
  const [passwordConfirmation, setPasswordConfirmation] = useState('')
  const [passwordError, setPasswordError] = useState('')

  /**
   * Handles changes to form inputs
   * param {React.ChangeEvent<HTMLInputElement>} e - The input change event
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  /**
   * Validates password strength
   * @param {string} password - The password to validate
   * @returns {string} Error message if password doesn't meet requirements, otherwise empty string
   */
  const validatePassword = (password: string) => {
    if (password.length < 8) {
      return "Password must be at least 8 characters long"
    }
    if (!/[A-Z]/.test(password)) {
      return "Password must contain at least one capital letter"
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      return "Password must contain at least one symbol"
    }
    if (!/\d/.test(password)) {
      return "Password must contain at least one number"
    }
    return ""
  }

  /**
   * Handles navigation to the next step in signup process
   */
  const handleNextStep = () => {
    if (step === 1) {
      const passwordValidationError = validatePassword(formData.password)
      if (passwordValidationError) {
        setPasswordError(passwordValidationError)
        return
      }
      if (formData.password !== passwordConfirmation) {
        setPasswordError("Passwords do not match")
        return
      }
      setPasswordError("")
    }
    setStep(step + 1)
  }

  /**
   * Handles changes to subject fields
   * param {number} index - Index of the subject being edited
   * param {string} field - Field name being updated
   * param {string} value - New value for the field
   */
  const handleSubjectChange = (index: number, field: string, value: string) => {
    const newSubjects = [...formData.subjects]
    newSubjects[index] = { ...newSubjects[index], [field]: value }
    setFormData({ ...formData, subjects: newSubjects })
  }

  /**
   * Handles file uploads for subjects
   * param {number} index - Index of the subject being edited
   * param {File | null} file - Uploaded file object
   */
  const handleFileChange = (index: number, file: File | null) => {
    const newSubjects = [...formData.subjects]
    newSubjects[index] = { ...newSubjects[index], file }
    setFormData({ ...formData, subjects: newSubjects })
  }

  /**
   * Adds a new subject to the form data
   */
  const addSubject = () => {
    setFormData({
      ...formData,
      subjects: [...formData.subjects, { name: '', file: null, studyDay: '' }]
    })
  }
  /**
   * Handles form submission for signup
   * param {React.FormEvent} e - The form event object
   */
  // submit function for pushing the signup data to the backend
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Gather the data
    const data = {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        studyHours: formData.studyHours,
        studyTime: formData.studyTime,
        subjects: formData.subjects.map(subject => ({
            name: subject.name,
            studyDay: subject.studyDay,
            file: subject.file?.name, // Handle file uploads separately
        }))
    }

    try {
        const response = await fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        const result = await response.json()
        if (response.ok) {
            alert('Signup successful!')
            localStorage.setItem('token', result.token)
            navigate('/dashboard')
        } else {
            alert(result.error || 'Signup failed')
        }
    } catch (error) {
        console.error('Error during signup:', error)
        alert('An error occurred during signup')
    }
}

  return (
    <form onSubmit={handleSubmit}>
      {step === 1 && (
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input 
              id="name" 
              name="name"
              type="text" 
              placeholder="John Doe" 
              value={formData.name}
              onChange={handleChange}
              required 
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input 
              id="email" 
              name="email"
              type="email" 
              placeholder="m@example.com" 
              value={formData.email}
              onChange={handleChange}
              required 
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input 
              id="password" 
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required 
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input 
              id="confirmPassword" 
              name="confirmPassword"
              type="password"
              value={passwordConfirmation}
              onChange={(e) => setPasswordConfirmation(e.target.value)}
              required 
            />
          </div>
          {passwordError && (
            <div className="text-red-500 text-sm">{passwordError}</div>
          )}
          <Button type="button" onClick={handleNextStep} className="w-full">Next</Button>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="studyHours">Preferred Study Hours</Label>
            <Input 
              id="studyHours" 
              name="studyHours"
              type="number" 
              placeholder="2"
              value={formData.studyHours}
              onChange={handleChange}
              required 
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="studyTime">Preferred Study Time</Label>
            <Input 
              id="studyTime" 
              name="studyTime"
              type="time"
              value={formData.studyTime}
              onChange={handleChange}
              required 
            />
          </div>
          <Button type="submit" className="w-full">Sign Up</Button>
        </div>
      )}
    </form>
  )
}

// Main Component
export default function AuthInterface() {
  const navigate = useNavigate(); // Initialize the navigation hook
  const [isLogin, setIsLogin] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      verifyToken(token)
    }
  }, [])

  
  /**
   * Verifies the authentication token
   * param {string} token - The token to verify
   */
  const verifyToken = async (token: string) => {
    try {
      const response = await fetch('http://localhost:5000/verify_token', {
        method: 'POST',
        headers: {
          'Authorization': token
        }
      })
      if (response.ok) {
        navigate('/dashboard')
      } else {
        localStorage.removeItem('token')
      }
    } catch (error) {
      console.error('Error verifying token:', error)
    }
  }
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>{isLogin ? 'Login' : 'Sign Up'}</CardTitle>
          <CardDescription>
            {isLogin ? 'Enter your credentials to login' : 'Create a new account'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLogin ? <Login /> : <Signup />}
          <div className="mt-4 text-center">
            <Button 
              variant="link" 
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? 'Need an account? Sign up' : 'Already have an account? Log in'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
