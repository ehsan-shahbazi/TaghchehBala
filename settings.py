class Table:
    def __init__(self, location, name, file_type='.csv', list_of_columns=None, rows=None):
        """
        :param location: This item should be stringed location of the file written from the project location some
        thing like: '../datas/recommendation/recommendation/'
        :param name: This item should be the name of the file excluding the .type of that like 'books'
        :param file_type: This item should contain the type of the file for example '.csv'
        :param list_of_columns: It should be a list of strings containing the name of the columns like:
        ['product_id', 'product_name', ...]
        :param rows: It should be an integer containing the number of rows in the file remain it 0 if you don't know or
        if this is a dynamic file.
        """
        self.location = location
        self.name = name
        self.file_type = file_type
        self.columns = list_of_columns
        self.rows = rows

    def give_address(self):
        return self.location + self.name + self.file_type


class Settings:
    def __init__(self):
        location = '../datas/recommendation/recommendation/'
        self.table_of_categories = Table(location, 'book-categories')
        self.table_of_books = '../datas/recommendation/recommendation/books.csv'
        self.table_of_download_samples = '../datas/recommendation/recommendation/download-sample.csv'
        self.table_of_purchases = '../datas/recommendation/recommendation/purchases.csv'
        self.table_of_quotes = '../datas/recommendation/recommendation/quotes.csv'
        self.table_of_readings = '../datas/recommendation/recommendation/readings.csv'
        self.table_of_reviews = '../datas/recommendation/recommendation/reviews.csv'
        self.table_of_whishlists = '../datas/recommendation/recommendation/whishlists.csv'
