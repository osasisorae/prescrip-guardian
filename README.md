# Script-Warden Project: An AutoGPT-Powered Chat Agent with OCR Augmentation for Enhanced Retrieval and Generation.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Commands](#commands)
  - [Creating Your Health Profile](#creating-your-health-profile)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)
- [Environment Variables](#environment-variables)

## Introduction
Script-Warden is your guardian in the world of medication safety. This innovative software seamlessly integrates into hospital systems, redefining the way healthcare professionals handle prescriptions. With a focus on accuracy and patient well-being, Script-Warden streamlines workflows and eradicates errors, promising a brighter future for healthcare.

## Features 

- **Interactive Chatbot**: Engage in conversations with the chatbot via the Telegram messaging platform.
- **Streamlined User Registration**: Script-Warden offers tailored registration options for various healthcare stakeholders. Choose from /set_admin for administrators overseeing doctor approvals, /doctor for doctor onboarding, /pharmacist for pharmacist onboarding, and /user for patient registration.
- **Innovative Prescription Creation**: Say goodbye to traditional prescription methods. With /create_prescription, doctors can effortlessly send handwritten images or explore digital alternatives, all backed by Optical Character Recognition (OCR) and robust data security. WIP.
- **Rapid Patient Data Input**: Doctors input patient data swiftly and accurately through interactive forms or messages, ensuring the integrity and accessibility of critical information. WIP.
- **Precision with NLP**: Experience the power of advanced Natural Language Processing (NLP) algorithms, meticulously assessing prescriptions and patient data to guarantee accuracy and patient safety. The automation of prescription delivery to pharmacists further enhances efficiency and reliability.

## Getting Started
### Prerequisites
Before you begin, ensure you have the following prerequisites:
- [Python](https://www.python.org/) 3.x
- [Telegram Bot Token](https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/)
- [OpenAI Keys](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)
- [Apify Keys](https://docs.apify.com/platform/integrations/api)


### Installation
1. Clone this repository:
   ```shell
   git clone https://github.com/osasisorae/script-warden
   ```

2. Install required Python dependencies:
    ```shell
    pip install -r requirements.txt
    ```
## Environment Variables
Make sure to set the following environment variables in your `.env` file:

- `BOT_TOKEN`: Your Telegram Bot token.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `APIFY_API_TOKEN`: Your Apify API token.

## Usage
1. Start Bot:
    ```shell
    cd script-warden
    mkdir admins
    mkdir doctors
    python bot.py
    ```

### Commands
- `/start`: Get started with Script-Warden and explore its capabilities.
- `/chat`: Engage in conversations with the chatbot.
- `/set_admin`: Begin the process of setting up administrator privileges for doctor approvals. **Do this first**
- `/doctor`: Start onboarding doctors seamlessly.
- `/pharmacist`: Facilitate the onboarding of pharmacists within your healthcare system.
- `/user`: Enable patients to register and access the benefits of Script-Warden.
- `/create_prescription`: Explore innovative prescription creation methods, including image-based and digital alternatives, supported by OCR and secure data storage.
- `/store_user_data`: Swiftly input patient data via interactive forms or messages, ensuring data integrity.
- `/verify_prescription`: Experience the precision of advanced Natural Language Processing (NLP) algorithms for prescription verification, enhancing accuracy and patient safety. Automated prescription delivery to pharmacists seals the deal.

## Architecture
The project's architecture includes the following components:

WIP

For a detailed architectural overview, refer to the Architecture document.

## Contributing
We welcome contributions to the project. If you'd like to contribute, please follow our [Contribution Guidelines](CONTRIBUTING.md).

## License
This project is licensed under the MIT License.


## Currently Integrated Sites
Check the site we get out our real time data [here](SITES.md)

## For changes and Updates
Check out our updates [here](UPDATES.md)

## Our Sites
- [Our Site](https://script-warden.framer.ai/)
