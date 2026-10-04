
import nltk
import re
from collections import Counter

# Download tokenizer data
nltk.download("punkt_tab", quiet=True)

print("=" * 40)
print("       AI TEXT SUMMARIZER")
print("=" * 40)

# Get summary percentage
percentage = input(
    "\nEnter summary percentage (25,,50, or 75): "
)

try:
    percentage = int(percentage)

    if percentage not in [25, 50, 75]:
        print("Invalid choice! Using 50%.")
        percentage = 50

except ValueError:
    print("Invalid input! Using 50%.")
    percentage = 50

# Get paragraph
text = input("\nEnter your paragraph:\n").strip()

if not text:
    print("Error: Please enter some text.")

else:
    # Split text into sentences
    sentences = nltk.sent_tokenize(text)

    # Count words
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    stop_words = {
        "is", "a", "an", "the", "and", "or", "in",
        "to", "of", "it", "for", "are", "was", "on",
        "with", "has", "have", "this", "that", "they",
        "their", "be", "as", "by", "at", "from", "use",
        "how", "you", "your"
    }

    important_words = [
        word for word in words
        if word not in stop_words
    ]

    word_frequency = Counter(important_words)

    # Display important keywords
    print("\n===== IMPORTANT KEYWORDS =====")

    keywords = word_frequency.most_common(5)

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

    # Select important sentences
    number_of_sentences = max(
        1,
        round(len(sentences) * percentage / 100)
    )

    number_of_sentences = min(
        number_of_sentences,
        len(sentences)
    )

    important_sentences = sorted(
        sentences,
        key=lambda sentence: sentence_scores[sentence],
        reverse=True
    )

    summary_sentences = important_sentences[
        :number_of_sentences
    ]

    # Keep original sentence order
    summary_sentences.sort(key=sentences.index)

    # Create summary
    summary = " ".join(summary_sentences)

    # Display summary
    print("\n===== SUMMARY =====")
    print(summary)

    # Display word counts
    original_words = len(text.split())
    summary_words = len(summary.split())

    print("\nOriginal word count:", original_words)
    print("Summary word count:", summary_words)
    print("Summary percentage:", percentage, "%")

    # Save summary to a text file
    try:
        with open("summary.txt", "w", encoding="utf-8") as file:
            file.write(summary)

        print("\nSummary saved successfully to summary.txt!")

    except OSError as error:
        print("\nCould not save summary:", error)

    print("\nSummarization completed successfully!")