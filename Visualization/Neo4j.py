from py2neo import Graph, Node, Relationship, NodeMatcher
import csv


def test_database(filepath, clus):
    graph = Graph("http://localhost:7474", username="neo4j", password='39742619')
    if clus == 1:
        graph.delete_all()
    f = open(filepath, 'r')
    f_csv = csv.reader(f)
    # labels = next(f_csv)
    labels = ['none', 'site1', 'name', 'score', 'genres', 'site2', 'year']
    print(labels)
    for row in f_csv:

        node_poster = Node("Poster", cluster=clus, name=row[labels.index('name')])
        genres = row[labels.index('genres')].split('|')
        # print(genres)
        # node_poster.update(name=row[labels.index('movie_title')])
        attr = {}
        for data in row:
            if not labels[row.index(data)] == 'name':
                attr[labels[row.index(data)]] = data
        node_poster.update(attr)

        matcher = NodeMatcher(graph)
        if node_poster not in matcher.match("Poster %d" % clus):
            graph.create(node_poster)
            print(row)

        # tar = matcher.match("Country", name=row[labels.index('country')]).first()
        # if tar:
        #     poster_locate_in = Relationship(node_poster, "country", tar)
        #     graph.create(poster_locate_in)
        # else:
        #     node_country = Node("Country", name=row[labels.index('country')])
        #     graph.create(node_country)
        #     poster_locates_in = Relationship(node_poster, "country", node_country)
        #     graph.create(poster_locates_in)

        # tar = matcher.match("Year", name=row[labels.index('year')]).first()
        # if tar:
        #     poster_locate_in = Relationship(node_poster, "year", tar)
        #     graph.create(poster_locate_in)
        # else:
        #     node_country = Node("Year", name=row[labels.index('year')])
        #     graph.create(node_country)
        #     poster_locates_in = Relationship(node_poster, "year", node_country)
        #     graph.create(poster_locates_in)

        for genre in genres:
            tar = matcher.match("Genre", name=genre).first()
            if tar:
                poster_genre_is = Relationship(node_poster, "genre", tar)
                graph.create(poster_genre_is)
            else:
                node_genre = Node("Genre", name=genre)
                graph.create(node_genre)
                poster_genre_is = Relationship(node_poster, "genre", node_genre)
                graph.create(poster_genre_is)

        for tar in matcher.match("Poster", cluster=clus):
            if tar == node_poster:
                continue
            sim_poster = Relationship(node_poster, "similar", tar)
            graph.create(sim_poster)

    return labels

# def simlilar_link(list, labels):
#     for pos_a in


if __name__ == '__main__':
    # filepath = 'C:\\Users\\X1 Yoga\\Desktop\\NUS\\CD\\Data Set\\testdata.csv'
    for i in range(1, 14, 1):
    # i = 7
        filepath = 'C:\\Users\\X1 Yoga\\Desktop\\NUS\\CD\\Data Set\\1\\{:.0f}.csv'.format(i)
        labels = test_database(filepath, i)
