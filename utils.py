

# gcd
def __gcd(a, b):
    if (a == 0):
        return b
    return __gcd(b % a, a)
 
# lcm of array
def Lcm_of_array(arr, idx):
   
    # lcm(a,b) = (a*b/gcd(a,b))
    if (idx == len(arr)-1):
        return arr[idx]
    a = arr[idx]
    b = Lcm_of_array(arr, idx+1)
    return int(a*b/__gcd(a,b)) # __gcd(a,b) is inbuilt library function


if __name__ == '__main__':
    # test case for lcmOfArray
    arr = [1,2,8,3]
    print(Lcm_of_array(arr, 0))
    arr = [2,7,3,9,4]
    print(Lcm_of_array(arr,0))