"""
-----------------------------------------------------------------------
File: frontend/app.py
Creation Time: Nov 9th 2024, 3:45 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
"""

import os
import jwt
import asyncio
import datetime
import requests
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2

# Set the port for Streamlit
os.environ["STREAMLIT_SERVER_PORT"] = "8501"


class GoogleOAuthHandler:
    def __init__(self):
        self.client_id = os.environ["GOOGLE_CLIENT_ID"]
        self.client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
        self.redirect_uri = os.environ["REDIRECT_URI"]
        self.client = GoogleOAuth2(self.client_id, self.client_secret)

    def initialize_session_state(self):
        if "authentication_status" not in st.session_state:
            st.session_state.authentication_status = None
        if "user_info" not in st.session_state:
            st.session_state.user_info = None
        if "token" not in st.session_state:
            st.session_state.token = None

    async def authenticate(self):
        try:
            if st.session_state.authentication_status is None:
                # Get authorization URL
                authorization_url = await self.client.get_authorization_url(
                    self.redirect_uri,
                    scope=["profile", "email"],
                    extras_params={"access_type": "offline", "prompt": "consent"},
                )

                print(f"Authorization URL: {authorization_url}")

                # Check for authorization code in URL
                query_params = st.query_params
                if "code" not in query_params:
                    self.show_login_button(authorization_url)
                    return False

                print(f"Query Params: {query_params}")

                # Exchange code for token
                token = await self.client.get_access_token(
                    query_params["code"], self.redirect_uri
                )

                print(f"Token: {token}")

                if token and not token.is_expired():
                    id_token = token.get("id_token")
                    decoded_token = jwt.decode(
                        id_token, options={"verify_signature": False}
                    )

                    # Extract user ID and email
                    user_id = decoded_token.get("sub")
                    user_email = decoded_token.get("email")
                    print(f"\n\nUser ID: {user_id}, Email: {user_email}")

                    # Store in session state
                    st.session_state.token = token
                    st.session_state.user_info = {"id": user_id, "email": user_email}
                    st.session_state.authentication_status = True

                    # Clear URL parameters
                    st.query_params.clear()
                    return True

            return st.session_state.authentication_status

        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            st.session_state.authentication_status = False
            return False

    def show_login_button(self, authorization_url):
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 50px;">
                <h1>Welcome to HackerNews Search</h1>
                <p>Please sign in to continue</p>
                <a href="{authorization_url}" target="_self">
                    <button style="
                        background-color: #4285f4;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    ">
                        Sign in with Google
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )


class HackerNewsPage:
    def __init__(self):
        self.api_url = "http://localhost:8000/api/schedule"

    @st.cache_data(ttl=300)  # Cache results for 5 minutes
    def fetch_hn_results(self, query: str, count: int):
        try:
            response = requests.post(
                self.api_url, json={"query": query, "count": count}, timeout=10
            )
            response.raise_for_status()
            return response.json()["result"]
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Failed to connect to the server")
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred: {str(e)}")

    def render(self):
        st.title("HackerNews Search")
        st.text("FastAPI, Restack, Together AI, LLamaIndex")

        # Input controls
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("Search Query", value="ai")
        with col2:
            count = st.number_input("Results", min_value=1, max_value=20, value=5)

        if st.button("Search", type="primary"):
            try:
                with st.spinner("Searching..."):
                    results = self.fetch_hn_results(query, count)

                # Store in history
                if "search_history" not in st.session_state:
                    st.session_state.search_history = []

                st.session_state.search_history.append(
                    {
                        "query": query,
                        "count": count,
                        "results": results,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

                # Display results
                self._display_results(results)

            except Exception as e:
                st.error(f"Error: {str(e)}")

        # Show history if available
        self._display_history()

    def _display_results(self, results):
        st.success("Search completed!")
        st.json(results)

    def _display_history(self):
        if "search_history" in st.session_state and st.session_state.search_history:
            with st.expander("Search History"):
                for idx, item in enumerate(
                    reversed(st.session_state.search_history), 1
                ):
                    st.markdown(f"### Search {idx}")
                    st.markdown(f"**Query:** {item['query']}")
                    st.markdown(f"**Time:** {item['timestamp']}")
                    with st.expander("Show Results"):
                        st.json(item["results"])


class StreamlitApp:
    def __init__(self):
        self.auth_handler = GoogleOAuthHandler()
        self.auth_handler.initialize_session_state()

    async def run(self):
        # Check authentication
        is_authenticated = await self.auth_handler.authenticate()

        if is_authenticated:
            self.show_authenticated_content()

    def show_authenticated_content(self):
        # Show user info
        st.sidebar.markdown(
            f"""
            <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
                📧 {st.session_state.user_info['email']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Horizontal navigation bar
        page = st.selectbox("Navigation", ["Home", "User Profile", "HackerNews"])

        if page == "Home":
            self.show_home_page()
        elif page == "User Profile":
            self.show_user_profile_page()
        elif page == "HackerNews":
            self.show_hackernews_page()

    def show_home_page(self):
        st.title("Welcome to HackerNews Search")
        st.write("Use the navigation bar to navigate to different sections.")

        # Search interface
        query = st.text_input("Search Query", value="ai")
        count = st.number_input("Number of Results", min_value=1, max_value=20, value=5)

        if st.button("Search", type="primary"):
            try:
                with st.spinner("Searching..."):
                    response = requests.post(
                        "http://localhost:8000/api/schedule",
                        json={"query": query, "count": count},
                        timeout=10,
                    )

                    if response.status_code == 200:
                        results = response.json()["result"]
                        st.success("Search completed!")
                        st.json(results)
                    else:
                        st.error(f"Error: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Failed to connect to the server. Please check if the API is running."
                )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = StreamlitApp()
    asyncio.run(app.run())
