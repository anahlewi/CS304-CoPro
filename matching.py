import queries 

def match(roster):
    ''' Algorithm that just matches people arbitrarly from roster'''
    matches = {}
    listResHall = []
    matched = set()
    for person in roster:
        listResHall.append(person['bnumber'])
    while len(listResHall) != 0:
        key = listResHall.pop()
        try:
            matches[key] = listResHall.pop()
        except:
            matches[key] = None
    return matches



def groupNum(groups):
    ''' Every group number needs to be unique and it autoincrements in table'''
    result = []
    for group in groups:
        result.append(group['groupNum'])
    return max(result)+1 


if __name__ == '__main__':
    conn = queries.getConn('c9')
    roster = queries.roster(conn, 13587)
    
    groups = queries.allGroups(conn)
    print(groupNum(groups))
    print(match(roster))
