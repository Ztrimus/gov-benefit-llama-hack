# Benefit Notification Tool

### Team Members:

Saurabh Zinjad, Shikha Verma, and Keval Shah

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Motivation](#motivation)
3. [Challenges in Benefit Access](#challenges-in-benefit-access)
4. [Solution Overview](#solution-overview)
5. [Architecture](#architecture)
6. [Features](#features)
7. [Technology Stack](#technology-stack)
8. [User Personas](#user-personas)
9. [Prototype and Demo](#prototype-and-demo)
10. [Future Work](#future-work)
11. [Acknowledgments](#acknowledgments)

---

## Project Overview

The **Benefit Notification Tool** is an accessible platform designed to assist underprivileged individuals in locating government benefits tailored to their unique profiles. By continuously monitoring government websites, the tool provides timely notifications and relevant benefit information via email, reducing the manual search burden on users.

---

## Motivation

Many individuals face significant hurdles in accessing public benefits due to:

-   Complex application processes that are lengthy and challenging to navigate
-   Lack of awareness about available support options
-   Language and digital literacy barriers, which hinder access for non-native speakers and individuals unfamiliar with digital tools

Our goal is to bridge these gaps by creating a simple, accessible platform that proactively notifies users of applicable benefits.

---

## Challenges in Benefit Access

The primary obstacles users face include:

1. **Complex Application Processes**
2. **Lack of Awareness**
3. **Language and Digital Literacy Barriers**
4. **Documentation Requirements**
5. **Frequent Eligibility Changes**

---

## Solution Overview

### Key Features

-   **Automated Web Crawling**: Monitors government websites for updates on benefit information.
-   **Personalized Notifications**: Tailored emails inform users about benefits suited to their profiles.
-   **Language-Agnostic Design**: The platform supports multiple languages to enhance accessibility.
-   **Real-Time Updates**: Ensures users receive the latest information on available benefits.
-   **Simplified Access**: Guides users directly to relevant benefits without requiring manual searches.

---

## Architecture

The Benefit Notification Tool operates through a series of integrated components:

1. **Web Crawler**: Built with `SimpleWebPageReader`, the crawler gathers updated information from government websites, saving data in a vector database for quick retrieval.
2. **Vector Database**: Uses Pinecone to store and query collected data, allowing for fast matching and retrieval of benefits.
3. **Personalized Notification System**: Leverages user profile data to send customized notifications on relevant benefits.
4. **Safety and Fairness**: Incorporates Llama Guard to minimize biases and ensure information integrity.
5. **Authentication**: Uses Google OAuth 2.0 for secure access and data protection.

---

## Features

1. **Automated Information Gathering**: Automatically crawls and updates government benefit data daily, maintaining an up-to-date database.
2. **Multilingual Support**: Enhances accessibility by supporting multiple languages, addressing language barriers.
3. **Real-Time Notifications**: Delivers prompt updates on benefit eligibility and availability to users.
4. **User-Friendly Design**: Prioritizes accessibility with a streamlined, easy-to-navigate interface.
5. **Privacy and Security**: Secured with Google OAuth 2.0 and other protective measures to ensure user data safety.

---

## Technology Stack

-   **Frontend**: React (with environment variable `REACT_APP_API_BASE_URL` for API requests)
-   **Backend**: FastAPI, REST API
-   **Data Storage**: Pinecone (Vector Database)
-   **Authentication**: Google OAuth 2.0
-   **Additional Tools**: Llama Guard for bias prevention

---

## User Personas

The primary users and beneficiaries include:

1. Low-income individuals and families
2. Elderly citizens
3. People with disabilities
4. Veterans
5. Students
6. Unemployed individuals
7. Single parents

---

## Prototype and Demo

Our current prototype features:

-   **Functionality**: Data is gathered from government websites, stored, and matched to users' profiles to send notifications about relevant benefits.
-   **Demo**: [Link to Demo or Video](#) _(Link to be updated based on hackathon submission platform)_

---

## Future Work

We aim to expand the tool's capabilities, including:

1. **Language Support Expansion**: Adding support for more popular languages in the U.S.
2. **Subscription Model**: Allowing new websites to join and share benefits information on our platform.
3. **Application Process Integration**: Assisting users through benefit application processes directly from our platform.

---

## Acknowledgments

Special thanks to **Philippe** for mentorship and guidance on prioritizing accessibility and direct user outreach, which helped refine the solution to be both simple and proactive.

---

This structure covers your project from the initial concept to the technical architecture and future work, making it easy for others to understand and navigate. Feel free to adapt each section to add specific details or links as needed.
