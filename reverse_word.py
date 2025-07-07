def reverse_words(input_string):
    # handle edge case of empty or whitespace-only string
    if not input_string or input_string.isspace():
        return input_string  # return as-is for empty/whitespace strings
    
    # split string into words using whitespace as delimiter
    word_list = input_string.split()  # automatically handles multiple spaces and strips leading/trailing spaces
    
    # reverse each word individually and store in result list
    reversed_word_list = []
    for word in word_list:
        reversed_word = word[::-1]  # python slice notation for string reversal
        reversed_word_list.append(reversed_word)
    
    # join all reversed words back with single space
    result = ' '.join(reversed_word_list)  # combine words with single space separator
    
    return result

# alternative one-liner solution using list comprehension
def reverse_words_concise(input_string):
    # handle edge case then apply transformation in one line
    if not input_string or input_string.isspace():
        return input_string
    
    # split -> reverse each word -> join back
    return ' '.join(word[::-1] for word in input_string.split())