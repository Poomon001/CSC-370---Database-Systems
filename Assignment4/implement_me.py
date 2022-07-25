# Implementation of B+-tree functionality.

from index import *

# You should implement all of the static functions declared
# in the ImplementMe class and submit this (and only this!) file.
class ImplementMe:

    # Returns a B+-tree obtained by inserting a key into a pre-existing
    # B+-tree index if the key is not already there. If it already exists,
    # the return value is equivalent to the original, input tree.
    #
    # Complexity: Guaranteed to be asymptotically linear in the height of the tree
    # Because the tree is balanced, it is also asymptotically logarithmic in the
    # number of keys that already exist in the index.
    @staticmethod
    def InsertIntoIndex( index, key ):
        keySets = index.root.keys
        pointerSets = index.root.pointers.pointers
        print(index)
        print(keySets)
        print(pointerSets)
        print(key)
        return index

    # Returns a boolean that indicates whether a given key
    # is found among the leaves of a B+-tree index.
    #
    # Complexity: Guaranteed not to touch more nodes than the
    # height of the tree
    @staticmethod
    def LookupKeyInIndex( index, key ):
        currNode = index.root
        currKey = currNode.keys

        while currKey != KeySet([None, None]):
            # set currKey to the left-most key
            currKeyVal = currKey.keys[0]

            if key == currKeyVal:
                return True

            # go left-side pointer
            if key < currKeyVal:
                # None represent the none Node
                if currNode.pointers.pointers[0] and currNode.pointers.pointers[0] is not None:
                    leftPointer = currNode.pointers.pointers[0]
                else:
                    return False

                currKey = leftPointer.keys
                currPointer = leftPointer.pointers # None represent the none Node
                currNode = Node(currKey, currPointer)
                continue


            # set currKey to the right-most key
            currKeyVal = currKey.keys[1]

            if key == currKeyVal:
                return True

            # go middle pointer
            if currKeyVal is None or key < currKeyVal:
                # None represent the none Node
                if currNode.pointers.pointers[1] and currNode.pointers.pointers[1] is not None:
                    middlePointer = currNode.pointers.pointers[1]
                else:
                    return False

                currKey = middlePointer.keys
                currPointer = middlePointer.pointers # None represent the none Node
                currNode = Node(currKey, currPointer)
                continue

            # # go right-side pointer
            if key > currKeyVal:
                # None represent the none Node
                if currNode.pointers.pointers[2] and currNode.pointers.pointers[2] is not None:
                    rightPointer = currNode.pointers.pointers[2]
                else:
                    return False

                currKey = rightPointer.keys
                currPointer = rightPointer.pointers  # None represent the none Node
                currNode = Node(currKey, currPointer)
                continue


        print("====")
        keySets = index.root.keys
        pointerSets = index.root.pointers
        print(index.root)
        print(keySets)
        print(pointerSets)

        print(key)

        # create new node from keys and pointers
        newNode = Node(keySets, pointerSets)
        print(newNode)
        return False

    # Returns a list of keys in a B+-tree index within the half-open
    # interval [lower_bound, upper_bound)
    #
    # Complexity: Guaranteed not to touch more nodes than the height
    # of the tree and the number of leaves overlapping the interval.
    @staticmethod
    def RangeSearchInIndex( index, lower_bound, upper_bound ):
        return []
