
import nltk
import re
from collections import Counter

# Download sentence tokenizer data
nltk.download("punkt_tab", quiet=True)

print("=" * 40)
print("       AI TEXT SUMMARIZER")
print("=" * 40)

# Get summary percentage first
percentage = input(
    "\nEnter summary percentage (25, 50, or 75): "
)

try:
    percentage = int(percentage)

    if percentage not in [25, 50, 75]:
        print("Invalid choice! Using 50% summary.")
        percentage = 50

except ValueError:
    print("Invalid input! Using 50% summary.")
    percentage = 50

# Get paragraph from the user
text = input("\nEnter your paragraph:\n").strip()

if not text:
    print("Error: Please enter some text.")
else:
    # Split paragraph into sentences
    sentences = nltk.sent_tokenize(text)

    # Find all words
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    # Remove common words
    stop_words = {
        "is", "a", "an", "the", "and", "or", "in",
        "to", "of", "it", "for", "are", "was", "on",
        "with", "has", "have", "this", "that", "they",
        "their", "be", "as", "by", "at", "from", "use"
    }

    important_words = [
        word for word in words
        if word not in stop_words
    ]

    # Count word frequencies
    word_frequency = Counter(important_words)
    
# Generate important keywords
keywords = word_frequency.most_common(5)

print("\n===== IMPORTANT KEYWORDS =====")

if keywords:
    for word, frequency in keywords:
        print(f"{word} ({frequency})")
else:
    print("No important keywords found.")

    # Calculate sentence scores
    sentence_scores = {}

    for sentence in sentences:
        sentence_words = re.findall(
            r"\b[a-zA-Z]+\b",
            sentence.lower()
        )

        score = sum(
            word_frequency[word]
            for word in sentence_words
            if word not in stop_words
        )

        sentence_scores[sentence] = score

    # Calculate number of sentences for summary
    number_of_sentences = max(
        1,
        round(len(sentences) * percentage / 100)
    )

    number_of_sentences = min(
        number_of_sentences,
        len(sentences)
    )

    # Select the most important sentences
    important_sentences = sorted(
        sentences,
        key=lambda sentence: sentence_scores[sentence],
        reverse=True
    )

    summary_sentences = important_sentences[
        :number_of_sentences
    ]

    # Keep sentences in original order
    summary_sentences.sort(key=sentences.index)

    # Create the final summary
    summary = " ".join(summary_sentences)

    # Display results
    print("\n" + "=" * 40)
    print("             SUMMARY")
    print("=" * 40)
    print(summary)

    # Display word counts
    original_words = len(text.split())
    summary_words = len(summary.split())

    print("\nOriginal word count:", original_words)
    print("Summary word count:", summary_words)
    print("Summary percentage selected:", percentage, "%")
    print("\nSummarization completed successfully!")
    
    # Save summary automatically
    with open("summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)

    print("Summary saved successfully to summary.txt!")