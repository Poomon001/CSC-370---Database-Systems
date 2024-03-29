from erd import *
from table import *

def getOtherRelation(currRelationshipName, relationshipSet):
    getRelation = relationshipSet[currRelationshipName][0]
    return getRelation

# get a foreign key format for relationship
def formatRelationshipForeignKey(value):
    formatForeignKey = []
    relationName = value[0]

    # [[connectionTables, references]]
    names_and_pks = value[4]

    # get foreign keys
    for i in range(len(names_and_pks)-1,-1,-1):
        tableName = names_and_pks[i][0]
        reference = names_and_pks[i][1]
        if relationName != tableName:
            formatForeignKey.append((tuple(reference), tableName, tuple(reference)))
    return formatForeignKey

# get a foreign key format for entry
def formatEntryForeignKey(currTable, currRelationshipName, relationshipSet):
    formatForeignKey = []
    names_and_pks = relationshipSet[currRelationshipName][4]
    for name_and_pk in names_and_pks:
        if name_and_pk[0] != currTable:
            reference = name_and_pk[1]
            formatForeignKey.append((tuple(reference), name_and_pk[0], tuple(reference)))
    return formatForeignKey

# convert to database answer
def convert_to_db(tableSet, relationshipSet):
    # [table: Table]
    db = []

    # build a table form entrySet
    for key, value in tableSet.items():
        name = key
        attributes = value[0]
        primary_key = value[1]
        connections = value[2]
        parents = value[3]
        supporting_relations = value[4]

        # [attribute, primary_key, foreign keys]
        tempProperties = [set(attributes),set(primary_key),set()]

        if connections:
            for connection in connections:
                otherRelationship = getOtherRelation(connection[0], relationshipSet)

                # many-one without pk
                if connection[1] == "MANY" and otherRelationship == "ONE" and len(relationshipSet[connection[0]][5]) == 0:
                    tempProperties[0] = tempProperties[0]|set(relationshipSet[connection[0]][2])
                    tempProperties[2] = tempProperties[2]|set(formatEntryForeignKey(name, connection[0], relationshipSet))

        if parents:
            # class inheritance
            for parent in parents:
                parent_primary_key = tableSet[parent][1]
                tempProperties[0] = tempProperties[0] | set(parent_primary_key)
                tempProperties[1] = tempProperties[1] | set(parent_primary_key)
                tempProperties[2] = tempProperties[2] | set([(tuple(parent_primary_key), parent, tuple(parent_primary_key))])

                tableSet[name][0] = tempProperties[0] | set(parent_primary_key)
                tableSet[name][1] = tempProperties[1] | set(parent_primary_key)
                tableSet[name][2] = tempProperties[2] | set([(tuple(parent_primary_key), parent, tuple(parent_primary_key))])

        if supporting_relations:
            # supporting relations
            for supporting_relation_name in supporting_relations:
                supporting_relation = relationshipSet[supporting_relation_name]
                tempProperties[0] = tempProperties[0] | set(supporting_relation[3])
                tempProperties[1] = tempProperties[1] | set(supporting_relation[3])
                tempProperties[2] = tempProperties[2] | set(formatEntryForeignKey(name, supporting_relation_name, relationshipSet))

                tableSet[name][0] = tempProperties[0] | set(supporting_relation[3])
                tableSet[name][1] = tempProperties[1] | set(supporting_relation[3])
                tableSet[name][2] = tempProperties[2] | set(formatEntryForeignKey(name, supporting_relation_name, relationshipSet))

                # update connection
                if connections:
                    for connection in connections:
                        connectionName = connection[0]
                        relationshipSet[connectionName][2] = set(relationshipSet[connectionName][2]) | set(supporting_relation[2])
                        relationshipSet[connectionName][3] = set(relationshipSet[connectionName][3]) | set(supporting_relation[3])
                        for relationship in relationshipSet[connectionName][4]:
                            relationship[1].extend(supporting_relation[4][0][1])
                            relationship[1] = list(set(relationship[1]))

        db.append(Table(name, tempProperties[0], tempProperties[1], tempProperties[2]))

    # build a table form relationshipSet
    for key, value in relationshipSet.items():
        name = key
        type = value[0]
        connectionTables = value[1]
        attributes = value[2]
        primary_key = value[3]
        names_and_pks = value[4]
        original_primary_key = value[5]

        # many-many case
        if type == "MANY":
            db.append(Table(name, set(attributes), set(primary_key), set(formatRelationshipForeignKey(value))))

        # many-one with pk
        if type == "ONE" and len(original_primary_key) != 0:
            manyPK = []
            # get manyPK
            for name_and_pk in names_and_pks:
                n = name_and_pk[0]
                if n in tableSet and (name, 'MANY') in tableSet[n][2]:
                    manyPK.extend(tableSet[n][1])
            manyPK.extend(original_primary_key)
            db.append(Table(name, set(attributes), set(manyPK), set(formatRelationshipForeignKey(value))))

    return Database(db)


# This function converts an ERD object into a Database object
# The Database object should correspond to a fully correct implementation
# of the ERD, including both data structure and constraints, such that the
# CREATE TABLE statements generated by the Database object will populate an
# empty MySQL database to exactly implement the conceptual design communicated
# by the ERD.
#
# @TODO: Implement me!
def convert_to_table( erd ):
    relationshipList = erd.relationships
    entrySetList = erd.entity_sets

    # {tableName: str, [[attribute set], [primary key], [connection], [parent], [supporting_relation]]}
    tableSet = {}

    # {relationshipName: str, [type:str, [connection tables], [attribute set], [all primary keys], [foreign key], [original primary keys]]}
    relationshipSet = {}

    # extract entrySet properties
    for entry in entrySetList:
        name = entry.name
        attribute_list = entry.attributes
        primary_key_list = entry.primary_key

        #[[name: str, type: int]]
        connections = entry.connections
        parent_list = entry.parents
        supporting_relations_list = entry.supporting_relations

        # create a new set
        if name not in tableSet:
            tableSet[name] = [[],[],[],[],[]]

        # get attributes
        if attribute_list:
            tableSet[name][0].extend(attribute_list)

        # get primary key
        if primary_key_list:
            tableSet[name][1].extend(primary_key_list)

        # get connections
        if connections:
            for connection in connections:
                relation_name = connection[0]
                type = connection[1].name
                tableSet[name][2].append((relation_name, type))

                # make relationship set
                if relation_name not in relationshipSet:
                    relationshipSet[relation_name] = [type, [], [], [], [], []]
                # add more data to relationship set
                # always keep ONE if possible
                relationshipSet[relation_name][0] = type if relationshipSet[relation_name][0] == "MANY" else relationshipSet[relation_name][0]
                relationshipSet[relation_name][1].append(name)
                [relationshipSet[relation_name][2].append(pk) for pk in primary_key_list]
                [relationshipSet[relation_name][3].append(pk) for pk in primary_key_list]
                [relationshipSet[relation_name][4].append([name, primary_key_list])]

        if parent_list:
            tableSet[name][3].extend(parent_list)

        if supporting_relations_list:
            tableSet[name][4].extend(supporting_relations_list)

    # extract relationships
    for relationship in relationshipList:
        name = relationship.name
        attribute = relationship.attributes
        primary_keys = relationship.primary_key

        # create a new set
        if attribute:
            [relationshipSet[name][2].append(attr) for attr in attribute]

        if primary_keys:
            [relationshipSet[name][3].append(pk) for pk in primary_keys]
            [relationshipSet[name][5].append(pk) for pk in primary_keys]

    # make db
    db = convert_to_db(tableSet, relationshipSet)

    return db
