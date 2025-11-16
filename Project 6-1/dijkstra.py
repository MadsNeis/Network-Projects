import sys
import json
import math

def ip_to_int(ip):
    parts = ip.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

def netmask_to_int(netmask):
    bits = int(netmask[1:])
    return (0XFFFFFFFF << (32 - bits)) & 0xFFFFFFFF

def get_address(ip, netmask):
    ip_int = ip_to_int(ip)
    mask_int = netmask_to_int(netmask)
    return ip_int & mask_int

def share_network(ip1, ip2, netmask):
    return get_address(ip1, netmask) == get_address(ip2, netmask)

def find_router_ip(routers, ip):
    for router_ip, router_data in routers.items():
        netmask = router_data['netmask']
        if share_network(router_ip, ip, netmask):
            return router_ip
    return None

def dijkstra(routers, start_router):
    distance = {}
    parent = {}
    to_visit = set()

    for router_ip in routers.keys():
        distance[router_ip] = math.inf
        parent[router_ip] = None
        to_visit.add(router_ip)

    distance[start_router] = 0

    while to_visit:
        current = min(to_visit, key=lambda x:distance[x])
        to_visit.remove(current)

        if distance[current] == math.inf:
            break

        connections = routers[current]['connections']
        for neighbor_ip, connection_data in connections.items():
            if neighbor_ip in to_visit:
                edge_weight = connection_data['ad']
                new_distance = distance[current] + edge_weight

                if new_distance < distance[neighbor_ip]:
                    distance[neighbor_ip] = new_distance
                    parent[neighbor_ip] = current

    return distance, parent

def reconstruct_path(parent, start_router, end_router):
    if parent[end_router] is None and start_router != end_router:
        return[]

    path = []
    current = end_router

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path




def dijkstras_shortest_path(routers, src_ip, dest_ip):
    src_router = find_router_ip(routers, src_ip)
    dest_router = find_router_ip(routers, dest_ip)

    if src_router is None or dest_router is None:
        return[]

    if src_router == dest_router:
        return []

    distance, parent = dijkstra(routers, src_router)

    path = reconstruct_path(parent, src_router, dest_router)


    return path



#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
