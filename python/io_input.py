def reverse(text):
    return text[::-1]

def is_palindrome(text):
    return text == reverse(text)

something = input("Enter text:")
something_lower = something.lower()

format = 'abcdefghijklmnopqrstuvwxyz'

for c in something_lower:
    if c not in format:
        something_lower = something_lower.replace(c, '')
	
print(something_lower)
	
if is_palindrome(something_lower):
    print("yes,it is a palindrome")
else:
    print("no,it is not a palindrome")