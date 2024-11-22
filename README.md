# Bridging Underprivileged to Government Support

### Team Members:

-   Saurabh Zinjad(https://github.com/Ztrimus)
-   Keval Shah (https://github.com/kevalshah14)
-   Shikha Verma(https://github.com/sverma89asu)

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
9. [Future Work](#future-work)

---

## Project Overview

The **Benefit Notification Tool** is an accessible platform designed to assist underprivileged individuals in locating government benefits tailored to their unique profiles. By continuously monitoring government websites, the tool provides timely notifications and relevant benefit information via email, reducing the manual search burden on users.

- [Demo Video](https://youtu.be/jLphWh1i8cQ)
- [Won 1st Prize of Llama Impact Hackathon](https://lablab.ai/event/llama-impact-hackathon/ragnarok/bridging-underprivileged-to-government-support)
- [Code Repo](https://github.com/Ztrimus/gov-benefit-llama-hack)

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
![Arch](./resources/Screenshot%202024-11-10%20at%204.39.03 PM.JPG)

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

-   **Frontend**: React, TailwindCSS, DaisyUI (with environment variable `REACT_APP_API_BASE_URL` for API requests)
-   **Backend**: FastAPI, REST API, Python
-   **Data Storage**: Pinecone (Vector Database), PostgreSQL
-   **Authentication**: Google OAuth 2.0
-   **Additional Tools**: LLama 3.1, Llama3.2, and Llama Guard for bias prevention
-   **Automated Pipeline**: Restack, Github Actions
    ![Arch](./resources/Screenshot%202024-11-10%20at%204.53.47 PM.JPG)

---

## User Personas

The primary users and beneficiaries include:

1. Single parents
2. Students
3. Elderly citizens
4. People with disabilities
5. Veterans
6. Low-income individuals and families
7. Unemployed individuals

---

## Future Work

We aim to expand the tool's capabilities, including:

1. **Language Support Expansion**: Adding support for more popular languages in the U.S.
2. **Subscription Model**: Allowing new websites to join and share benefits information on our platform.
3. **Application Process Integration**: Assisting users through benefit application processes directly from our platform.
