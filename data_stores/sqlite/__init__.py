"""
Initialization of SQLite interfaces and project-specific methods.
"""
import sqlite3

import pandas

from config import WIKIPEDIA_INDEX_FILE, SQLITE_ARCHIVE_INDEX_FILE


def parse_colons(s):
    """
    Separates the values delimited by the first two colons
    :param s: A String to parse colons over
    :return: the three Strings separated by the first two colons
    """
    portions = s.split(":")
    return [portions[0], portions[1], s[len(portions[0]) + len(portions[1]) + 2:len(s)]]


if __name__ == "__main__":

    indices = pandas.read_csv(WIKIPEDIA_INDEX_FILE, delimiter="|", names=["byte:id:title"])
    print("Done reading from csv")
    indices_values = indices.iloc[:, 0]
    row_values = []
    for i in range(len(indices_values)):
        if i % 100000 == 0:
            print(i)
        line = indices_values[i]
        row_values.append(parse_colons(line))

    print("done formatting data")

    # finding the next byte to read to (-1 if it should read to end of file)
    byte_values = list(set([val[0] for val in row_values]))
    byte_values.sort()
    byte_dict = {}
    for i, byte in enumerate(byte_values):
        byte_dict[byte] = byte_values[min(len(byte_values) - 1, i + 1)]
        if byte_dict[byte] == byte:
            byte_dict[byte] = -1

    for row in row_values:
        row.append(byte_dict[row[0]])

    articles = pandas.DataFrame(row_values, columns=["first_byte", "page_id", "title", "last_byte"])

    conn = sqlite3.connect(SQLITE_ARCHIVE_INDEX_FILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS articles;")
    conn.commit()
    # cursor.execute('CREATE TABLE articles (first_byte, page_id, title, last_byte)')
    articles.to_sql("articles", conn)
    conn.commit()
    cursor.execute("CREATE INDEX articles_id_idx ON articles (page_id);")
    cursor.execute("CREATE INDEX articles_title_idx ON articles (title);")
    conn.commit()
    conn.close()
