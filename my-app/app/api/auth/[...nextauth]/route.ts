import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
      authorization: {
        params: {
          redirect_uri: process.env.REDIRECT_URI,
        },
      },
    }),
  ],
  callbacks: {
    async redirect({ url, baseUrl }) {
      // Ensure that after login, the user is redirected to the intended URL
      return url.startsWith(baseUrl) ? url : baseUrl;
    }},
  secret: process.env.NEXTAUTH_SECRET,
  pages: {
    newUser: "/profile", // Redirect to /profile after a successful login for new users
  },
});

export { handler as GET, handler as POST };
