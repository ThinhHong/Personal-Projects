def longestPalindrome(s: str) -> str:
        longest = s[0]
        for i in range(len(s)):
            p = s[i]
            for j in range(i +1,len(s)):
                p += s[j]
                if p == p[::-1] and len(p) > len(longest):
                    longest = p

        return longest

def longestPalindrome2(s: str) -> str:
        if len(s) <= 1:
            return s
              
        start = 0
        longest = 1
        for i in range(len(s)):
            odd = s[i]         

        return longest



c = "abbd"

def solution(n, p, numIntegers):
    if p == []:
        return n
    
    maximun = 0
    for num in p:
        current_max = num^n
        if current_max > maximun:
            maximun = current_max

    bowls_no_magic = min(c)
    ingredient_used_no_magic = []
    amount_needed = []
    for i in range(len(a)):
        ingredient_used_no_magic.append(b[i] - (bowls_no_magic * a[i]))
        amount_needed.append(a[i] - ingredient_used_no_magic[i])        
            
    for i in range(k):
        maximun = ingredient_used_no_magic.index(max(ingredient_used_no_magic))
        minimun = ingredient_used_no_magic.index(min(ingredient_used_no_magic))
        ingredient_used_no_magic[minimun] += 1
           
    magic_bowl = []       
    for i in range(len(ingredient_used_no_magic)):
        magic_bowl.append(ingredient_used_no_magic[i]//a[i])
    
    return min(magic_bowl)+ bowls_no_magic

    return maximun




def solution(a, b, k):
    bowls_can = []
    ingredients_left = []
    for i in range(len(a)):
        bowls_can.append(b[i]//a[i])
        ingredients_left.append(b[i]%a[i])
        
    min_bowls = min(bowls_can)
    min_index = bowls_can.index(min_bowls)
    for i in range(k):
       ingredients_left[min_index] += 1
       if ingredients_left[min_index] % a[min_index] == 0:
           ingredients_left[min_index] = 0
           bowls_can[min_index] += 1
           min_bowls = min(bowls_can) 
           min_index = bowls_can.index(min_bowls)

    return min_bowls

 
def convert(s,n):
    if len(s) < 2:
        return s
    
    ex = "PAYPALISHIRING"
    out = "PINALSIGYAHRPI"
    output = s[0]
    space = n -2
    next = space + n
    count = 0
    k = 1
    row = 0
    while len(output) != len(s):
        count += next
        if count > len(s):
            count = k
            output += s[count]
            k += 1
            r += 1
        output += s[count]
        