import spacy
from collections import Counter


class PromptAnalyzer:

    def __init__(self) -> None:
        self.nlp_model = spacy.load('en_core_web_sm')
        self.word_counter = Counter()

    def extract_keywords(self, text: str):

        doc = self.nlp_model(text)

        return [ent.text for ent in doc.ents]

    def keyword_counter(self, text_data_list: None):
        for text_data in text_data_list:
            # Process text using spaCy
            doc = self.nlp_model(text_data)

            # Extract relevant tokens (e.g., nouns, verbs, etc.)
            relevant_tokens = [
                token.text.lower() for token in doc if not token.is_stop and token.is_alpha]

            # Update the counter
            self.word_counter.update(relevant_tokens)
        print(text_data_list)
        # Print the most common keywords
        most_common_keywords = self.word_counter.most_common(
            5)  # Change '10' to the desired number
        print(most_common_keywords)
