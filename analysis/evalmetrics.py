import pandas as pd
import textstat
import matplotlib.pyplot as plt
from pathlib import Path

#  Load data
DATA_PATH = Path("../data/commonlitpairs.csv")
df = pd.read_csv(DATA_PATH)

#
df["complex_text"] = df["complex_text"].astype(str)
df["simplified_text"] = df["simplified_text"].astype(str)

def word_count(text: str) -> int:
    return len(text.split())

def avg_sentence_length(text: str) -> float:
    sentences = textstat.sentence_count(text)
    if sentences == 0:
        return 0
    return word_count(text) / sentences

#  Compute metrics
# Readability scores (Flesch–Kincaid Grade Level)
df["fk_complex"] = df["complex_text"].apply(textstat.flesch_kincaid_grade)
df["fk_simple"] = df["simplified_text"].apply(textstat.flesch_kincaid_grade)

# Average sentence length
df["avg_sent_len_complex"] = df["complex_text"].apply(avg_sentence_length)
df["avg_sent_len_simple"] = df["simplified_text"].apply(avg_sentence_length)

# Compression ratio (how much shorter)
df["complex_words"] = df["complex_text"].apply(word_count)
df["simple_words"] = df["simplified_text"].apply(word_count)
df["compression_ratio"] = df["simple_words"] / df["complex_words"]

print("Average Flesch–Kincaid grade (complex):", df["fk_complex"].mean())
print("Average Flesch–Kincaid grade (simple):", df["fk_simple"].mean())
print("Average compression ratio:", df["compression_ratio"].mean())

#  VISUALIZATION 1: Readability Score
plt.figure()
plt.bar(["Complex", "Simplified"],
        [df["fk_complex"].mean(), df["fk_simple"].mean()])
plt.ylabel("Flesch–Kincaid Grade Level")
plt.title("Average Reading Grade Level\nBefore vs After Simplification")
plt.savefig("../data/vis_readability.png", bbox_inches="tight")

# VISUALIZATION 2: Sentence Length Distribution
plt.figure()
plt.hist(df["avg_sent_len_complex"], bins=10, alpha=0.5, label="Complex")
plt.hist(df["avg_sent_len_simple"], bins=10, alpha=0.5, label="Simplified")
plt.xlabel("Average Sentence Length (words)")
plt.ylabel("Number of Passages")
plt.title("Sentence Length Distribution\nBefore vs After Simplification")
plt.legend()
plt.savefig("../data/vis_sentence_length.png", bbox_inches="tight")

# VISUALIZATION 3: Compression Ratio
plt.figure()
plt.hist(df["compression_ratio"], bins=10)
plt.xlabel("Compression Ratio (simplified_words / complex_words)")
plt.ylabel("Number of Passages")
plt.title("How Much Shorter Are Simplified Texts?")
plt.savefig("../data/vis_compression_ratio.png", bbox_inches="tight")

print("Saved: vis_readability.png, vis_sentence_length.png, vis_compression_ratio.png in data/ folder")
