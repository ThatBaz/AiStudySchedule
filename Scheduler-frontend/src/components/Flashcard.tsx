import { useState } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, X } from 'lucide-react'

interface FlashcardProps {
  flashcards: { question: string; answer: string }[]
  onClose: () => void
}

export function Flashcard({ flashcards, onClose }: FlashcardProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)

  const handleNext = () => {
    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(currentIndex + 1)
      setIsFlipped(false)
    }
  }

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1)
      setIsFlipped(false)
    }
  }

  const handleFlip = () => {
    setIsFlipped(!isFlipped)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <Card className="w-96 h-64 perspective-1000">
        <CardContent 
          className={`w-full h-full transition-transform duration-500 transform-style-preserve-3d cursor-pointer ${
            isFlipped ? 'rotate-y-180' : ''
          }`}
          onClick={handleFlip}
        >
          <div className="absolute inset-0 backface-hidden">
            <div className="flex flex-col items-center justify-center h-full p-4">
              <p className="text-lg font-semibold text-center">{flashcards[currentIndex].question}</p>
            </div>
          </div>
          <div className="absolute inset-0 backface-hidden rotate-y-180">
            <div className="flex flex-col items-center justify-center h-full p-4">
              <p className="text-lg font-semibold text-center">{flashcards[currentIndex].answer}</p>
            </div>
          </div>
        </CardContent>
      </Card>
      <div className="absolute bottom-4 left-0 right-0 flex justify-center space-x-4">
        <Button onClick={handlePrevious} disabled={currentIndex === 0}>
          <ChevronLeft className="w-4 h-4 mr-2" />
          Previous
        </Button>
        <Button onClick={handleNext} disabled={currentIndex === flashcards.length - 1}>
          Next
          <ChevronRight className="w-4 h-4 ml-2" />
        </Button>
      </div>
      <Button className="absolute top-4 right-4" variant="ghost" onClick={onClose}>
        <X className="w-4 h-4" />
      </Button>
    </div>
  )
}

