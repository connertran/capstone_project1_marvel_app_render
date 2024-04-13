def return_first_15_words(sentence):
    # Split the sentence into words and take the first 15
    words = sentence.split()[:15]
    result = ' '.join(words)
    return result + "..."

p = "The Mad Titan Thanos, a melancholy, brooding individual, consumed with the concept of death, sought out personal power and increased strength, endowing himself with cybernetic implants until he became more powerful than any of his brethren."
print(return_first_15_words(p))