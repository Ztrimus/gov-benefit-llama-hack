// app/api/auth/[...nextauth]/route.ts

import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    }),
  ],
  // Remove the custom signIn page to use NextAuth's default behavior
  // If you want to use the default NextAuth sign-in page, omit the 'pages' property
  // To directly initiate Google sign-in, you don't need to specify a custom sign-in page
  // pages: {
  //   signIn: '/register',
  // },
  secret: process.env.NEXTAUTH_SECRET, // Ensure this is set in your .env.local
});

export { handler as GET, handler as POST };
