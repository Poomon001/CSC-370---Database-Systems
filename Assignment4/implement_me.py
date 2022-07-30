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
        pointerSets = index.root.pointers
        print(index.root)
        print("\n ======= \n")

        print(keySets)
        print(pointerSets)

        # create new node from keys and pointers
        newNode = Node(keySets, pointerSets)
        print(newNode)

        currNode = index.root
        currKey = currNode.keys
        path = []
        splitKey = []

        # insert into empty B+ tree
        if currKey == KeySet([None, None]):
            keySets = KeySet([key, index.root.keys.keys[1]])
            pointerSets = index.root.pointers
            index = Index(Node(keySets, pointerSets))


        while currKey != KeySet([None, None]):
            # save current path
            path.append(currNode)

            # set currKey to the left-most key
            currKeyVal = currKey.keys[0] # int | None

            ''' Traverse to a leaf node '''

            # find a duplicate, return original B+ tree
            if key == currKeyVal:
                return index

            # case 1: key is less than left-most key
            if key < currKeyVal:
                # None represent the none Node
                if currNode.pointers.pointers[0] and currNode.pointers.pointers[0] is not None:
                    # currNode is not a leaf, go left-side pointer
                    currNode = currNode.pointers.pointers[0]
                    currKey = currNode.keys
                    currPointer = currNode.pointers  # None represent the none Node
                    continue

            # set currKey to the right-most key
            currKeyVal = currKey.keys[1]  # int | None

            # find a duplicate, return original B+ tree
            if key == currKeyVal:
                return index

            # case 2: key is between left-most and right-most keys
            if currKeyVal is None or key < currKeyVal:
                # None represent the none Node
                if currNode.pointers.pointers[0] and currNode.pointers.pointers[0] is not None:
                    # currNode is not a leaf, go middle pointer
                    currNode = currNode.pointers.pointers[1]
                    currKey = currNode.keys
                    currPointer = currNode.pointers  # None represent the none Node
                    continue

            # case 3: key is greater than right-most key
            if currKeyVal and key > currKeyVal:
                # None represent the none Node
                if currNode.pointers.pointers[0] and currNode.pointers.pointers[0] is not None:
                    # currNode is not a leaf, go right pointer
                    currNode = currNode.pointers.pointers[2]
                    currKey = currNode.keys
                    currPointer = currNode.pointers  # None represent the none Node
                    continue

            ''' insertion at a leaf '''
            # space is available to insert
            path.pop()
            if None in currKey.keys:
                 currKey.keys = [min(key, currKey.keys[0]), max(key, currKey.keys[0])]
                 return index
            else:
                # split to the next level
                nums = sorted([currKey.keys[0], currKey.keys[1], key])
                splitKey.append(nums[1])
                currNode.keys = KeySet([nums[0], None])
                currNode.pointers = PointerSet([None] * Index.FAN_OUT)
                rightNode = Node(KeySet([nums[1], nums[2]]), PointerSet([None] * Index.FAN_OUT))
                currNode.pointers.pointers[Index.NUM_KEYS] = rightNode

                # add to the next level
                while splitKey:
                    key = splitKey.pop()
                    if path:
                        # still parent left
                        parent = path.pop()
                    else:
                        # no parent left
                        parent = Node(KeySet([key, None]), PointerSet([currNode, rightNode, None]))
                        currNode.pointers.pointers[Index.NUM_KEYS] = rightNode
                        break

                    # insert at a leaf
                    if leftNode and rightNode:
                        prev = None
                        print("+++++")
                        p = parent
                        for i in range(len(parent.pointers.pointers)):
                            print(i)
                        # # edit pointer
                        # parent.pointers.pointers[0].pointers.pointers[Index.NUM_KEYS] = leftNode
                        # # edit leaf
                        leftNode = rightNode = []



                    # split to upper level

                return Index(parent)

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

        keySets = index.root.keys
        pointerSets = index.root.pointers
        # print(index.root)
        # print(keySets)
        # print(pointerSets)
        # # create new node from keys and pointers
        # newNode = Node(keySets, pointerSets)
        # print(newNode)

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

            # go right-side pointer
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

        return False

    # Returns a list of keys in a B+-tree index within the half-open
    # interval [lower_bound, upper_bound)
    #
    # Complexity: Guaranteed not to touch more nodes than the height
    # of the tree and the number of leaves overlapping the interval.
    @staticmethod
    def RangeSearchInIndex( index, lower_bound, upper_bound ):
        return []