import random
import regex
import matplotlib.pyplot as plt

fs = open('sample_simple_english_wiki.txt', 'r')
content = fs.read()
fs.close()

# Preprocessing the content

processContent = content.lower()
finalContent = regex.sub(r'[^\w\s]', '', processContent)
print("Processed Content-\n", finalContent)

# Printing some stats
n_chars = len(finalContent)
vocab = ''.join(set(finalContent))
print("unique_chars:", vocab)
n_unique_chars = len(vocab)
print("Number of characters:", n_chars)
print("Number of unique characters:", n_unique_chars)

# Creating probability of each character
char_prob_dict = dict()
for chars in vocab:
    char_prob_dict[chars] = [finalContent.count(chars), finalContent.count(chars) / n_chars]
print(char_prob_dict)

# Sampling from probability model

# Separating the probability from dictionary
cum_prob_list = []
for key in char_prob_dict:
    cum_prob_list.append(char_prob_dict[key][1])

# Calculating the cumulative probability for all elements
for i in range(1, len(cum_prob_list)):
    cum_prob_list[i] = cum_prob_list[i] + cum_prob_list[i - 1]

# Adding back the cumulative probability to dictionary
flag = 0
for key in char_prob_dict:
    char_prob_dict[key].append(cum_prob_list[flag])
    flag = flag + 1

# Generating the random number for generating char
gen_rand_num = []
for num in range(0, 35000):
    gen_rand_num.append(random.random())

gen_char_text = ''
# Generating character
for numb in gen_rand_num:
    for key in char_prob_dict:
        if char_prob_dict[key][2] > numb:
            gen_char_text += str(key)
            break
        else:
            pass

# Checking the word count of original
original_word_len = dict()
original_words = finalContent.split(' ')

for or_word in original_words:
    if len(or_word) in original_word_len:
        original_word_len[len(or_word)] += 1
    else:
        original_word_len[len(or_word)] = 1
print("Original word lengths", original_word_len)


# Probability of Original words
original_word_prob = dict()
for org_word in original_word_len:
    original_word_prob[org_word] = original_word_len[org_word] / sum(original_word_len.values())
print("Original probability", original_word_prob)

# Checking the word count of generated
generated_word_len = dict()
generated_words = gen_char_text.split(' ')

for gen_word in generated_words:
    if len(gen_word) in generated_word_len:
        generated_word_len[len(gen_word)] += 1
    else:
        generated_word_len[len(gen_word)] = 1
print("Original word lengths", generated_word_len)

# Probability of generated words
generated_word_prob = dict()
for gen_word in generated_word_len:
    generated_word_prob[gen_word] = generated_word_len[gen_word] / sum(generated_word_len.values())
print("Generated probability:", generated_word_prob)

# Creating text file out of the generated text
with open('GeneratedFile.txt', 'w') as gen_file:
    gen_file.write(gen_char_text)

# Separating values for mapping on bar plot
original_values = []
generated_values = []
original_x_values = []
generated_x_values = []
for original_key_value in original_word_prob:
    original_values.append(original_word_prob[original_key_value])
    original_x_values.append(original_key_value)

for generated_key_value in generated_word_prob:
    generated_values.append(generated_word_prob[generated_key_value])
    generated_x_values.append(generated_key_value)

print("Original", original_values)
print("Generated", generated_values)

# Plotting the graph
plot = plt.subplot(111)
plot.bar(original_x_values, original_values, label='Original word', width=0.5, color='b', align='edge')
plot.bar(generated_x_values, generated_values, label='Generated word', width=0.5, color='g', align='center')
plot.set_xlabel("Length of words")
plot.set_ylabel("Probability of word lengths")
plt.title("Probability word distribution of Original and Generated words")
plt.legend()
plt.show()
