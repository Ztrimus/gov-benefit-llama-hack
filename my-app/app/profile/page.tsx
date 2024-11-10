'use client'

import { useState } from 'react'
import { useSession } from 'next-auth/react'

interface FormData {
  name: string
  occupation: string
  dob: string
  income: string
  demographics: string
  affiliatedOrg: string
}

export default function ProfilePage() {
  const { data: session } = useSession()
  const [formData, setFormData] = useState<FormData>({
    name: '',
    occupation: '',
    dob: '',
    income: '',
    demographics: '',
    affiliatedOrg: ''
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSelectChange = (value: string, name: string) => {
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log(formData)
    // Here you would typically send the data to your backend
  }

  if (!session) {
    return <div>Please sign in to access this page.</div>
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-2xl">
        <h2 className="text-2xl font-semibold mb-2">User Profile</h2>
        <p className="mb-4 text-gray-600">Please provide your information to help us find relevant benefits for you.</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="name" className="block font-medium mb-1">Full Name</label>
            <input 
              id="name" 
              name="name" 
              value={formData.name} 
              onChange={handleChange} 
              required 
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div>
            <label htmlFor="occupation" className="block font-medium mb-1">Occupation</label>
            <input 
              id="occupation" 
              name="occupation" 
              value={formData.occupation} 
              onChange={handleChange} 
              required 
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div>
            <label htmlFor="dob" className="block font-medium mb-1">Date of Birth</label>
            <input 
              id="dob" 
              name="dob" 
              type="date" 
              value={formData.dob} 
              onChange={handleChange} 
              required 
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div>
            <label htmlFor="income" className="block font-medium mb-1">Annual Income</label>
            <input 
              id="income" 
              name="income" 
              type="number" 
              value={formData.income} 
              onChange={handleChange} 
              required 
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div>
            <label htmlFor="demographics" className="block font-medium mb-1">Demographics</label>
            <select 
              id="demographics" 
              name="demographics" 
              value={formData.demographics} 
              onChange={(e) => handleSelectChange(e.target.value, 'demographics')} 
              className="w-full p-2 border border-gray-300 rounded"
              required
            >
              <option value="">Select your demographic</option>
              <option value="african-american">African American</option>
              <option value="asian">Asian</option>
              <option value="hispanic">Hispanic</option>
              <option value="native-american">Native American</option>
              <option value="white">White</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label htmlFor="affiliatedOrg" className="block font-medium mb-1">Affiliated Organization</label>
            <textarea 
              id="affiliatedOrg" 
              name="affiliatedOrg" 
              value={formData.affiliatedOrg} 
              onChange={handleChange} 
              placeholder="Enter any organizations you're affiliated with (optional)" 
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
            Save Profile
          </button>
        </form>
      </div>
    </div>
  )
}
