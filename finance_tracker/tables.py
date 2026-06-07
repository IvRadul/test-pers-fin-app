import csv

def export_to_csv(path_to_file, data):
    with open(path_to_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(list(map(str, row)))
