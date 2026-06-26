"""
Additional Coding Practice — 10 Python Programs
Class XII Data Science Holiday Homework

Programs 1-5: List operations
Programs 6-10: String operations
"""

# ---------------- LIST PROGRAMS ----------------

# 1. Largest element in a list
def largest_element(lst):
    largest = lst[0]
    for item in lst:
        if item > largest:
            largest = item
    return largest


# 2. Remove duplicates from a list (preserving order)
def remove_duplicates(lst):
    result = []
    for item in lst:
        if item not in result:
            result.append(item)
    return result


# 3. Sort a list (ascending) using simple bubble sort
def sort_list(lst):
    arr = lst.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# 4. Linear search for an element in a list
def search_element(lst, target):
    for i, item in enumerate(lst):
        if item == target:
            return i        # return index if found
    return -1               # not found


# 5. Sum and average of a list
def sum_and_average(lst):
    total = sum(lst)
    average = total / len(lst) if lst else 0
    return total, average


# ---------------- STRING PROGRAMS ----------------

# 6. Reverse a string
def reverse_string(s):
    return s[::-1]


# 7. Check if a string is a palindrome
def is_palindrome(s):
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


# 8. Count vowels in a string
def count_vowels(s):
    vowels = "aeiouAEIOU"
    count = 0
    for ch in s:
        if ch in vowels:
            count += 1
    return count


# 9. Word counter
def word_count(s):
    words = s.split()
    return len(words)


# 10. Count occurrences of each character
def char_frequency(s):
    freq = {}
    for ch in s:
        if ch != " ":
            freq[ch] = freq.get(ch, 0) + 1
    return freq


# ---------------- DEMO / DRIVER CODE ----------------
if __name__ == "__main__":
    print("===== LIST PROGRAMS =====")
    nums = [10, 4, 25, 4, 7, 25, 100, 1]
    print("List:", nums)
    print("1. Largest element :", largest_element(nums))
    print("2. Without duplicates:", remove_duplicates(nums))
    print("3. Sorted list     :", sort_list(nums))
    print("4. Search 25       : index", search_element(nums, 25))
    print("5. Sum & Average   :", sum_and_average(nums))

    print("\n===== STRING PROGRAMS =====")
    text = "Madam Anna went to the level"
    print("Text:", text)
    print("6. Reversed     :", reverse_string(text))
    print("7. Is palindrome:", is_palindrome("MadaM"))
    print("8. Vowel count  :", count_vowels(text))
    print("9. Word count   :", word_count(text))
    print("10. Char freq   :", char_frequency(text))
