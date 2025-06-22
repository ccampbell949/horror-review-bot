import pytest
from unittest.mock import patch, MagicMock
from horrorbot.review.generator import ReviewGenerator

@patch("horrorbot.review.generator.OpenAI")
def test_generate_review_success(mock_openai_class):
    # Mock the client and the chat.completions.create method chain
    mock_openai_instance = MagicMock()
    mock_openai_class.return_value = mock_openai_instance
    
    # Setup mock response structure as expected
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This horror flick is chilling! 👻 #scary #horror"

    # Configure the chain call to return mock_response
    mock_openai_instance.chat.completions.create.return_value = mock_response

    generator = ReviewGenerator(api_key="fake_api_key")
    review = generator.generate("Scary Movie", "A haunted house story.")

    # Check that the response content matches our mocked content
    assert review == "This horror flick is chilling! 👻 #scary #horror"

    # Verify the API call was made with correct parameters (optional but recommended)
    mock_openai_instance.chat.completions.create.assert_called_once()
    args, kwargs = mock_openai_instance.chat.completions.create.call_args
    assert kwargs["model"] == "deepseek/deepseek-r1-0528-qwen3-8b:free"
    assert any("Scary Movie" in msg["content"] for msg in kwargs["messages"])

@patch("horrorbot.review.generator.OpenAI")
def test_generate_review_handles_exception(mock_openai_class):
    # Simulate an exception raised by the API client
    mock_openai_instance = MagicMock()
    mock_openai_class.return_value = mock_openai_instance
    mock_openai_instance.chat.completions.create.side_effect = Exception("API failure")

    generator = ReviewGenerator(api_key="fake_api_key")
    review = generator.generate("Scary Movie", "A haunted house story.")

    assert review.startswith("Error generating review:")
