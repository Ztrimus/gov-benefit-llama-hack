'use client'

import Image from 'next/image'
import { Button } from "@/components/ui/button"
import { signIn } from 'next-auth/react'

export function BlockPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md w-96">
        <div className="flex flex-col items-center space-y-4">
          <Image
            src="/placeholder.svg?height=80&width=80"
            alt="Government Benefits Platform Logo"
            width={80}
            height={80}
            className="rounded-full"
          />
          <h1 className="text-2xl font-bold text-gray-900">Government Benefits Platform</h1>
          <p className="text-center text-gray-600">
            Access information about various government benefits and programs for underprivileged citizens.
          </p>
          <Button 
            onClick={() => signIn('google', { callbackUrl: '/profile' })}
            className="w-full"
          >
            Sign in with Google
          </Button>
        </div>
      </div>
    </div>
  )
}