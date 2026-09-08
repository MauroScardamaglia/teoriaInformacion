def getProbs(words):
  alfa = list(set(words))
  probs = [words.count(word) / len(words) for word in alfa]
  return alfa, probs

def sortProbs(alfa, probs):
  sort = sorted(zip(probs, alfa), reverse=True)
  alfa = [x[1] for x in sort]
  probs = [x[0] for x in sort]
  return alfa, probs

def getZipf(count, s = 1):
  const = 1 / sum(1 / (i + 1) ** s for i in range(count))
  return [const / (i + 1) ** s for i in range(count)]

def getWords(file):
  text = open(file, "r", encoding="utf-8").read()
  return ["".join(c for c in word.lower() if c.isalnum()) for word in text.split()]

def printZipf(alfa, probs, zipf, length):
  for i in range(length):
    print(f'P("{alfa[i]}") = {probs[i]:.4f} ~ {zipf[i]:.4f}')

words = getWords("el_quijote.txt")
alfa, probs = getProbs(words)
alfa, probs = sortProbs(alfa, probs)
zipf = getZipf(len(alfa))

printZipf(alfa, probs, zipf, 20)