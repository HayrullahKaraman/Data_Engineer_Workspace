import cassandra
from cassandra.cluster import Cluster
from scripts.read_json import read_fitness


def save_fitness():
    cluster = Cluster(["172.30.0.4"],port = 9042)
    
    session=cluster.connect("running")
    for i in range(0, len(read_fitness())):
        session.execute("""INSERT INTO  running.run_table (timestamp,elevation,source_type,duration,distance,elevation_gain,elevation_loss) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s)""",(read_fitness()[i]["timestamp"],read_fitness()[i]['elevation'],read_fitness()[i]['source_type'],read_fitness()[i]['duration']
                                                    ,read_fitness()[i]['distance'],read_fitness()[i]['elevation_gain'],read_fitness()[i]['elevation_loss'])
                    )

