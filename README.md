# Cosa Neutra

## Models

The `models.py` file defines the data models used in the game. These models interact with the MongoDB database to store and retrieve data.

- **Model**: A base class for all models, providing common functionality.
- **Segment**: Represents a segment of text to be neutralized.
- **Neutralization**: Represents a user's neutralization of a segment.
- **Review**: Represents a review of a neutralization.
- **Game**: Represents a game instance.
- **Team**: Represents a team of users.
- **User**: Represents a user of the bot.
- **UserWithRole**: An abstract base class for users with specific roles.
  - **Neutralizer**: A user who neutralizes segments.
  - **Reviewer**: A user who reviews neutralizations.
  - **Hybrid**: A user who can both neutralize and review.

## Handlers

The handlers manage the bot's interactions with users. They are responsible for processing commands and messages, guiding users through the game, and handling various states.

- **start.py**: Handles the `/start` command, welcoming users and initiating the onboarding process.
- **onboarding.py**: Guides new users through the onboarding process, asking for their team and role.
- **tutorial.py**: Provides a tutorial to new users, explaining the game mechanics.
- **play.py**: Manages the game play, including submitting neutralizations and reviews.
- **fallbacks.py**: Handles unknown commands and default messages.
- **main.py**: The main message handler that routes messages based on the user's current state.

## Locales

The game currently exists in 2 languages: French and English. The translations are to be found in `locales.py`.
