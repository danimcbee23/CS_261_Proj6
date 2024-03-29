# Name: Danielle McBride
# OSU Email: mcbridda@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/14/24
# Description: Implementation of a hash map with chaining collision resolution


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """ If key not in hash map add key/value pair
         if key in hash map update value """

        # Resize table if load factor >= 1.0
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # Calculate hash index
        hash_key = self._hash_function(key)
        hash_index = hash_key % self._capacity

        # Set pointer
        hash_bucket = self._buckets.get_at_index(hash_index)

        # Key found, update value
        for element in hash_bucket:
            if element.key == key:
                element.value = value
                return

        # Key not found, insert new pair
        hash_bucket.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """ Resize hash table capacity """

        # Return if capacity < 1
        if new_capacity < 1:
            return

        # Ensure new capacity is prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create new hash map
        new_table = HashMap(new_capacity, self._hash_function)

        # Handle when capacity needs to = 2
        if new_capacity == 2:
            new_table._capacity = 2

        # Insert elements into new table
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                for element in self._buckets.get_at_index(i):
                    new_table.put(element.key, element.value)

        # Reassigning new values to self
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table.get_capacity()

    def table_load(self) -> float:
        """ Return the current load factor of hash table """

        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """ Return # of empty buckets in hash table """

        bucket_count = 0

        # If bucket empty update count
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() == 0:
                bucket_count += 1

        return bucket_count

    def get(self, key: str):
        """ Return value of given key """

        # Calculate hash key
        hash_key = self._hash_function(key)

        # Map hash key to index & locate bucket
        hash_index = hash_key % self._capacity
        hash_bucket = self._buckets.get_at_index(hash_index)

        # If bucket empty, return None
        if hash_bucket.length() == 0:
            return None
        # Element located, return value
        else:
            for element in hash_bucket:
                if element.key == key:
                    return element.value

        # Element not found
        return None

    def contains_key(self, key: str) -> bool:
        """ Return T if key in hash map else return F """

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                # Key located, return True
                for element in self._buckets.get_at_index(i):
                    if element.key == key:
                        return True

        # Key not found
        return False

    def remove(self, key: str) -> None:
        """ If key is in hash map remove key/value pair """

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                for element in self._buckets.get_at_index(i):
                    # Key found, remove key/value pair
                    if element.key == key:
                        self._buckets.get_at_index(i).remove(key)
                        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """ Return a tuple of key/value pair """

        key_val_pair = DynamicArray()

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                # Create tuple with key/value pair
                for element in self._buckets.get_at_index(i):
                    key_val_pair.append((element.key, element.value))

        return key_val_pair

    def clear(self) -> None:
        """ Clear contents of hash map, keeps capacity """

        # Update map attributes
        self._buckets = DynamicArray()
        self._size = 0

        # Update buckets with empty lists
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """ Return a tuple containing mode value of da and frequency """

    # Create instance of Separate Chaining HashMap
    map = HashMap()

    # Count frequency of each element
    for i in range(da.length()):
        # Element not found frequency = 1
        if not map.contains_key(da.get_at_index(i)):
            map.put(da.get_at_index(i), 1)
        # Element found frequency += 1
        else:
            map.put(da.get_at_index(i), map.get(da.get_at_index(i)) + 1)

    arr = map.get_keys_and_values()
    mode_arr = DynamicArray()
    mode_freq = 0

    # Find max frequency
    for i in range(arr.length()):
        if mode_freq < arr.get_at_index(i)[1]:
            mode_freq = arr.get_at_index(i)[1]

    # Locate all elements with max frequency
    for i in range(arr.length()):
        if arr.get_at_index(i)[1] == mode_freq:
            mode_arr.append(arr.get_at_index(i)[0])

    return mode_arr, mode_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
