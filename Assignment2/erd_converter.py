from erd import *
from table import *

def formatForeignKey(value):
    formatForeignKey = []

    # [[connectionTables], [references]]
    foreignKeys = value[4]

    for i in range(len(foreignKeys)-1,-1,-1):
        table = foreignKeys[i][0]
        reference = foreignKeys[i][1]
        formatForeignKey.append(((reference,), table, (reference,)))
    return formatForeignKey


def convert_to_db(tableSet, relationshipSet):
    # [table: Table]
    db = []

    # build a table form entrySet
    for key, value in tableSet.items():
        name = key
        attributes = value[0]
        primary_key = value[1]
        connections = value[2]

        # print(key, attributes, primary_key)

        if not connections:
            db.append(Table(name, set(attributes), set(primary_key), set()))
        else:
            if connections[1] == "MANY":
                db.append(Table(name, set(attributes), set(primary_key), set()))

    # build a table form relationshipSet
    for key, value in relationshipSet.items():
        name = key
        type = value[0]
        connectionTables = value[1]
        attributes = value[2]
        primary_key = value[3]
        foreign_key = value[4]

        db.append(Table(name, set(attributes), set(primary_key), set(formatForeignKey(value))))
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

    # {tableName: str, [[attribute set], [primary key]]}
    tableSet = {}

    # {relationshipName: str, [type:str, [connection tables], [attribute set], [primary key], [foreign key]]}
    relationshipSet = {}

    # extract entrySet properties
    for entry in entrySetList:
        name = entry.name
        attribute_list = entry.attributes
        primary_key_list = entry.primary_key

        #[[name: str, type: int]]
        connections = entry.connections

        # create a new set
        if name not in tableSet:
            tableSet[name] = []

        # get attributes
        if attribute_list:
            tableSet[name].append(attribute_list)
        else:
            tableSet[name].append([])

        # get primary key
        if primary_key_list:
            tableSet[name].append(primary_key_list)
        else:
            tableSet[name].append([])

        # get connections
        if connections:
            for connection in connections:
                relation_name = connection[0]
                type = connection[1].name
                tableSet[name].append([relation_name, type])

                # make relationship set
                if relation_name not in relationshipSet:
                    relationshipSet[relation_name] = [type, [], [], [], []]
                # add more data to relationship set
                relationshipSet[relation_name][0] = type
                relationshipSet[relation_name][1].append(name)
                [relationshipSet[relation_name][2].append(pk) for pk in primary_key_list]
                [relationshipSet[relation_name][3].append(pk) for pk in primary_key_list]
                [relationshipSet[relation_name][4].append([name, pk]) for pk in primary_key_list]

        else:
            tableSet[name].append([])

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

    # make db
    db = convert_to_db(tableSet, relationshipSet)

    print("\n")
    print("expect", "\n".join([str(val) for val in expectedDB.tables]))
    print("\n========================\n")
    print("mine", "\n".join([str(val) for val in db.tables]))
    return db
