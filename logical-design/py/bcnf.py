# Counts the number of steps required to decompose a relation into BCNF.

from relation import *
from functional_dependency import *
from typing import Set

# You should implement the static function declared
# in the ImplementMe class and submit this (and only this!) file.
# You are welcome to add supporting classes and methods in this file.

# find closure of a target
def getClosure(target, fds):
    # print("\n+=== Start getClosure===+\n")
    closure = set()
    for t in target:
        closure.add(t)
    # print("target", closure)

    # print(fds)
    for _ in fds:
        for fd in fds:
            leftSet = fd.left_hand_side
            rightSet = fd.right_hand_side

            for left in leftSet:
                if left not in closure:
                    break
            else:
                for right in rightSet:
                    closure.add(right)

    # print("Final closure", closure)
    # print("\n+=== End getClosure ===+\n")
    return closure


# determine if any violations
def isAnyBCNFViolation(fds, relation):
    for l in fds:
        left = l.left_hand_side
        closure = getClosure(left, fds)
        if relation != closure:
            return True
    return False

def getViolation(fds, relation):
    for l in fds:
        left = l.left_hand_side
        closure = getClosure(left, fds)
        if relation != closure:
            return l
    return None

def projectFDS(relations, fds):
    f = fds
    r = relations
    validFDS = set()
    for fd in fds:
        attributes = fd.left_hand_side | fd.right_hand_side
        if isSubset(attributes, relations):
            validFDS.add(fd)

    return validFDS

# check if r2 contains all attribute in r1
def isSubset(r1, r2):
    for attribute in r1:
        if not attribute in r2:
            return False
    return True

class ImplementMe:
    # Returns the number of recursive steps required for BCNF decomposition
    #
    # The input is a set of relations and a set of functional dependencies.
    # The relations have *already* been decomposed.
    # This function determines how many recursive steps were required for that
    # decomposition or -1 if the relations are not a correct decomposition.
    @staticmethod
    def DecompositionSteps(relations, fds):
        s = set()
        # [{R1, R2, ..., R3}, step]
        answer = [s, 0]

        # relations: RelationSet = set(relations: Relation)
        # relation: Relation = set(attribute: set(char))
        relations = relations.relations

        # fds: FDSet = set(functional_dependencies: FunctionalDependency)
        # functional_dependencies: FunctionalDependency = set(left_hand_side: set(char)) and set(right_hand_side: set(char))
        functionalDependency = fds

        # union relations
        unionRelations = set()
        for relation in relations:
            unionRelations = unionRelations | relation.attributes

        def recursive(relations: Set, functionalDependency: FDSet):
            fds = functionalDependency.functional_dependencies
            fds = projectFDS(relations, fds)
            # check violation
            if not isAnyBCNFViolation(fds, relations):
                answer[0].add(Relation(relations))
                return relations
            else:
                # increase step
                answer[1] = answer[1] + 1

                # determine fds that violate BCNF
                fsViolation = getViolation(fds, relations)
                left = fsViolation.left_hand_side

                # find R1 and R2
                R1 = getClosure(left, fds)
                R2 = (relations - R1) | left

                recursive(R1, functionalDependency)
                recursive(R2, functionalDependency)

        recursive(unionRelations, functionalDependency)

        # retern the answer that match the fiven relations
        # print("answer:",answer)
        if answer[0] == relations:
            return answer[1]
        else:
            return -1