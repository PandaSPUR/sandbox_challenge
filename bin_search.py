'''
Name: Pawan M Ranganatha Rao
ID: 0497218

Runs Binary Search recursively.
Also Used to test stack limit set by giving large arrays

'''


def recBinSearch(x, nums, low, high):
    if low > high: # No place left to look, return -1
        return -1
    mid = (low + high) / 2
    item = nums[mid]
    if item == x: # Found it! Return the index
        return mid
    elif x < item: # Look in lower half
        return recBinSearch(x, nums, low, mid-1)
    else: # Look in upper half
        return recBinSearch(x, nums, mid+1, high)
 


def main():
    nums = [2,4,8,34,43,68]
    key = 2
    pos = recBinSearch(key, nums, 0, len(nums)-1)
    if (pos != -1):
        print "key found"
    else:
        print "key not found"

if __name__=="__main__":
    main()
