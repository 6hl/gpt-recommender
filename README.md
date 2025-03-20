# GPT Recommender

GPT Recommender is a project designed to provide intelligent recommendations using OpenAI's GPT models or locally runnable LLMs. This repository contains the code and resources necessary to build and run a recommendation system powered by GPT.

## Features

- **Intelligent Recommendations**: Leverages advanced GPT models to provide context-aware and accurate suggestions based on user input.
- **Customizable Logic**: Easily adapt the recommendation engine to suit your specific use case with configurable parameters and modular design.
- **Modular design**: Designed for effortless integration with containerization process.

## Usage

### Server

1. Clone the repository:

    ```bash
    git clone https://github.com/6hl/gpt-recommender.git
    cd gpt-recommender
    pip install -e .
    ```

2. Build the Docker container:

    ```bash
    make docker-build
    ```

3. Run the server:

    ```bash
    make docker-run
    ```

    or

    ```bash
    gunicorn --bind 0.0.0.0:8080 app:app
    ```

4. Send a request to the live container:

    ```bash
    curl -X POST http://0.0.0.0:8080/recommend \
    -H "Content-Type: application/json" \
    -d '{"query": "Your input text here"}'
    ```

   Replace `"Your input text here"` with the text you want to send for recommendations.

### Local

```python
from consultant.consultant import Consultant
consultant = Consultant("cfg.yaml")
response = consultant(
    query="Give me restaurant recommentations for NYC.",
    skip_profile_recommendations=True
)
```

## Configuration

Base configs are inside [cfg/](./cfg/). Checkout the [cfg.md](cfg/cfg.md) for more info.
