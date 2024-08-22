# Telegram Diffusion Bot

This project is a powerful and versatile Telegram bot designed for generating high-quality images based on user-provided text prompts. Leveraging the latest diffusion models, this bot allows users to interact via Telegram commands and receive AI-generated images within seconds. The bot is structured in a modular fashion, making it easy to extend and customize.

## Key Features

- **AI-Powered Image Generation**: Utilizes state-of-the-art diffusion models to generate images based on text descriptions provided by users.
- **Fast Response Time**: The bot typically generates and returns images within 9-10 seconds.
- **Modular Architecture**: The bot is built using a modular structure, which includes various handlers, filters, middlewares, and services that can be easily extended or customized.
- **Admin Functionality**: Special filters and handlers are included to manage administrative tasks, ensuring that only authorized users can access certain features.

## Project Structure

- **`bot.py`**: The main script that initializes the bot, sets up the diffusion pipeline, and handles incoming messages.
- **`tgbot/config.py`**: Contains configuration classes that load settings from environment variables, including bot tokens, database configurations, and more.
- **`tgbot/handlers/`**: Includes different handlers for managing bot commands, user interactions, and diffusion tasks. Key handlers include:
  - `admin.py`: Manages admin-specific commands and interactions.
  - `user.py`: Handles general user interactions such as start commands.
  - `diffusion.py`: Handles the diffusion-related commands where image generation takes place.
- **`tgbot/filters/`**: Custom filters, including `AdminFilter`, which filters messages based on admin status.
- **`tgbot/middlewares/`**: Middlewares for injecting configuration and handling database sessions within handlers.
- **`tgbot/services/`**: Services that include message broadcasting and image sending functionalities.

## Installation

### Prerequisites

- Python 3.11 or higher
- [Pytorch](https://pytorch.org/get-started/locally/) with CUDA support (for GPU acceleration)
- Redis (optional, for state management)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/tkavelli/testgit.git
   cd testgit
