import asyncio
import os
import streamlit as st
import requests

from httpx_oauth.clients.google import GoogleOAuth2

page = st.sidebar.selectbox("Choose a page", ["Home", "HackerNews"])


async def write_authorization_url(client, redirect_uri):
    authorization_url = await client.get_authorization_url(
        redirect_uri,
        scope=["profile", "email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url


async def write_access_token(client, redirect_uri, code):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client, token):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def main(user_id, user_email):
    st.write(f"You're logged in as {user_email}")


def hackernews_page():
    # Set page title and header
    st.title("LLama Hackathon Quickstart")
    st.text("FastAPI, Restack, Together AI, LLamaIndex")

    # Create text area for user input with session state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    query = st.text_input("Query HN", key="query", value="ai")
    count = st.number_input("Number of results", key="count", value=5)

    # Initialize response history in session state
    if "response_history" not in st.session_state:
        st.session_state.response_history = []

    # Create button to send request
    if st.button("Search HN"):
        if query:
            try:
                with st.spinner("Searching..."):
                    # Make POST request to FastAPI backend
                    response = requests.post(
                        "http://localhost:8000/api/schedule",
                        json={"query": query, "count": count},
                    )

                    if response.status_code == 200:
                        st.success("Response received!")
                        # Add the new response to history with the original prompt
                        st.session_state.response_history.append(
                            {
                                "query": query,
                                "count": count,
                                "response": response.json()["result"],
                            }
                        )
                    else:
                        st.error(f"Error: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Failed to connect to the server. Make sure the FastAPI server is running."
                )
        else:
            st.warning("Please enter a prompt before submitting.")

    # Display response history
    if st.session_state.response_history:
        st.subheader("Response History")
        for i, item in enumerate(st.session_state.response_history, 1):
            st.markdown(f"**Query {i}:** {item['query']}")
            st.markdown(f"**Response {i}:** {item['response']}")
            st.markdown("---")


if __name__ == "__main__":
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
    redirect_uri = os.environ["REDIRECT_URI"]

    client = GoogleOAuth2(client_id, client_secret)

    authorization_url = asyncio.run(
        write_authorization_url(client=client, redirect_uri=redirect_uri)
    )

    if "token" not in st.session_state:
        st.session_state.token = None

    if st.session_state.token is None:
        try:
            code = st.query_params()["code"]
        except:
            st.write(
                f"""<h1>
                Please login using this <a target="_self"
                href="{authorization_url}">url</a></h1>""",
                unsafe_allow_html=True,
            )
        else:
            # Verify token is correct:
            try:
                token = asyncio.run(
                    write_access_token(
                        client=client, redirect_uri=redirect_uri, code=code
                    )
                )
            except:
                st.write(
                    f"""<h1>
                    This account is not allowed or page was refreshed.
                    Please try again: <a target="_self"
                    href="{authorization_url}">url</a></h1>""",
                    unsafe_allow_html=True,
                )
            else:
                # Check if token has expired:
                if token.is_expired():
                    if token.is_expired():
                        st.write(
                            f"""<h1>
                        Login session has ended,
                        please <a target="_self" href="{authorization_url}">
                        login</a> again.</h1>
                        """
                        )
                else:
                    st.session_state.token = token
                    user_id, user_email = asyncio.run(
                        get_email(client=client, token=token["access_token"])
                    )
                    st.session_state.user_id = user_id
                    st.session_state.user_email = user_email
                    main(
                        user_id=st.session_state.user_id,
                        user_email=st.session_state.user_email,
                    )
                    hackernews_page()
    else:
        main(user_id=st.session_state.user_id, user_email=st.session_state.user_email)
        hackernews_page()
