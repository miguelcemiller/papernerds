def boyer_moore_horspool(text, pattern):
    '''
    :param text: (string)
    :param pattern: (string)
    :return: list of indexes where full match occurs
    '''
    t_len = len(text)
    p_len = len(pattern)
    results = []

    # Step 1: Preprocess the data
    # Create "bad matches" table (with a size of jump)
    # ord() - As input given "x" char. As output - integer representing the unicode
    T = {i: p_len for i in range(256)}  # table of 256 integers (each char represents as unique integer in unicode)
    for i, char in enumerate(pattern):
        T[ord(char)] = p_len - i

    # Step 2: Search pattern in the text
    i = 0

    while i <= t_len - p_len:
        skip = 0
        text_part = text[i:i + p_len][::-1]

        # Iterate over reversed part of text (from right to left)
        for j, current_char in enumerate(text_part):
            # Mismatch found, now we can jump through several indexes
            if pattern[p_len - j - 1] != current_char:
                if T[ord(pattern[p_len - j - 1])] != 0:
                    skip = T[ord(pattern[p_len - j - 1])]
                else:
                    skip = 1
                break

        # Finally if we found complete match, we should add its index to results list
        else:
            results.append(i)
            skip = 1
        i += skip

    return results