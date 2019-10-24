from settings import Settings
from pandas import read_csv
settings = Settings()


def vec2rate(inp_vec):
    if not inp_vec[0]:
        return None
    else:
        if inp_vec[1][0] != -1:
            return inp_vec[1][0]
        if inp_vec[1][1] != -1:
            return 5
        if inp_vec[1][2] != -1:
            return 5
        if inp_vec[1][3] != -1:
            return 5
        if inp_vec[1][4] != -1:
            return 4
        if inp_vec[1][5] != -1:
            return min(inp_vec[1][5], 5)


class Files:
    def __init__(self, load_ratings=False):
        print('loading the files...\nloading reviews')
        self.file_of_reviews = read_csv(settings.table_of_reviews.give_address())
        print('loading quotes')
        self.file_of_quotes = read_csv(settings.table_of_quotes.give_address())
        print('loading wish lists')
        self.file_of_wishlists = read_csv(settings.table_of_whishlists.give_address())
        print('loading purchases')
        self.file_of_purchases = read_csv(settings.table_of_purchases.give_address())
        print('loading download samples')
        self.file_of_download_samples = read_csv(settings.table_of_download_samples.give_address())
        print('loading readings')
        self.file_of_readings = read_csv(settings.table_of_readings.give_address())
        print('loading books')
        self.file_of_books = read_csv(settings.table_of_books.give_address())
        print('all the files are loaded.\n' + '=' * 100)
        if load_ratings:
            self.file_of_ratings = read_csv('my_ratings.csv')
        else:
            self.file_of_ratings = None

    def close_all(self):
        del self.file_of_download_samples
        del self.file_of_purchases
        del self.file_of_quotes
        del self.file_of_readings
        del self.file_of_reviews
        del self.file_of_wishlists
        del self.file_of_books


class RateCalculator:
    def __init__(self, load_ratings=False):
        self.files = Files(load_ratings=load_ratings)
        self.user_id_list = self.find_users()
        self.item_id_list = self.find_items()
        self.rated_item_id_list = self.find_rated_items()
        self.user_coding = {}
        self.item_coding = {}
        # self.files.close_all()

    def find_users(self):
        # print(self.files.file_of_reviews.columns)
        users1 = set(self.files.file_of_reviews.loc[:, 'AccountId'])
        # print(self.files.file_of_wishlists.columns)
        users1.union(set(self.files.file_of_wishlists.loc[:, 'AccountId']))
        # print(self.files.file_of_readings.columns)
        users1.union(set(self.files.file_of_readings.loc[:, 'AccountId']))
        # print(self.files.file_of_quotes.columns)
        users1.union(set(self.files.file_of_quotes.loc[:, 'accountId']))
        # print(self.files.file_of_download_samples.columns)
        users1.union(set(self.files.file_of_download_samples.loc[:, 'AccountId']))
        out = list(users1)
        print('we have ', len(out), ' users')
        with open('AccountCoding', 'w') as file:
            for index, val in enumerate(out):
                file.write(str(index) + ',' + str(val) + '\n')
                self.user_coding[val] = index
        return out

    def find_items(self):
        # print(self.files.file_of_books.columns)
        books1 = set(self.files.file_of_books.loc[:, 'Id'])
        out = list(books1)
        print('we have ', len(out), ' items.')
        with open('ItemCoding', 'w') as file:
            for index, val in enumerate(out):
                file.write(str(index) + ',' + str(val) + '\n')
                self.item_coding[val] = index
        return out

    def find_rated_items(self):
        # print(self.files.file_of_reviews.columns)
        items1 = set(self.files.file_of_reviews.loc[:, 'BookId'])
        # print(self.files.file_of_wishlists.columns)
        items1.union(set(self.files.file_of_wishlists.loc[:, 'BookId']))
        # print(self.files.file_of_readings.columns)
        items1.union(set(self.files.file_of_readings.loc[:, 'BookId']))
        # print(self.files.file_of_quotes.columns)
        items1.union(set(self.files.file_of_quotes.loc[:, 'bookId']))
        # print(self.files.file_of_download_samples.columns)
        items1.union(set(self.files.file_of_download_samples.loc[:, 'BookId']))
        out = list(items1)
        print('we have ', len(out), ' rated items.')
        return out

    def calculate_rate_vector(self, user_id, item_id):
        # print(self.files.file_of_reviews.head())
        rating = self.files.file_of_reviews[(self.files.file_of_reviews.AccountId == user_id) &
                                            (self.files.file_of_reviews.BookId == item_id)].Rate

        if len(rating) == 1:
            return tuple([True, [rating.item(), 0, 0, 0, 0, 0]])
        else:
            rating = -1
        quotes = self.files.file_of_quotes[(self.files.file_of_quotes.accountId == user_id) &
                                           (self.files.file_of_quotes.bookId == item_id)]
        wish_list = self.files.file_of_quotes[(self.files.file_of_wishlists.AccountId == user_id) &
                                              (self.files.file_of_wishlists.BookId == item_id)]
        purchase = self.files.file_of_quotes[(self.files.file_of_purchases.AccountId == user_id) &
                                             (self.files.file_of_purchases.BookId == item_id)]
        download_sam = self.files.file_of_download_samples[(self.files.file_of_download_samples.AccountId == user_id) &
                                                           (self.files.file_of_download_samples.BookId == item_id)]
        reading = self.files.file_of_readings[(self.files.file_of_readings.AccountId == user_id) &
                                              (self.files.file_of_readings.BookId == item_id)].TotalSeconds
        have_data = False
        if len(quotes) > 0:
            quotes = 1
            have_data = True
        else:
            quotes = -1
        if len(wish_list) > 0:
            wish_list = 1
            have_data = True
        else:
            wish_list = -1
        if len(purchase) > 0:
            purchase = 1
            have_data = True
        else:
            purchase = -1
        if len(download_sam) > 0:
            download_sam = 1
            have_data = True
        else:
            download_sam = -1
        if len(reading) == 1:
            reading = reading.item()
            have_data = True
        else:
            reading = -1
        if have_data:
            return tuple([True, [rating, quotes, wish_list, purchase, download_sam, reading]])
        return tuple([False, [0, 0, 0, 0, 0, 0]])

    def mother_process(self):
        with open('my_ratings', 'w') as file:
            interactions = self.files.file_of_download_samples[['AccountId', 'BookId']]
            num_of_interactions = interactions.shape[0]
            for interaction in interactions.iterrows():
                if (interaction[0] % 500) == 0:
                    print(interaction[0] * 100 / num_of_interactions, ' % completed.')
                user = interaction[1][0]
                item = interaction[1][1]
                rate = self.calculate_rate_vector(user, item)
                if rate[0]:
                    file.write(str(user) + ',' + str(item) + ',' + str(vec2rate(rate)) + '\n')

    def update_user_item_coding(self):
        if self.files.file_of_ratings:
            with open('my_coded_ratings', 'w') as file:
                num_of_interactions = self.files.file_of_ratings.shape[0]
                for interaction in self.files.file_of_ratings.iterrows():
                    if (interaction[0] % 500) == 0:
                        print(interaction[0] * 100 / num_of_interactions, ' % completed.')
                    user = self.user_coding[interaction[1][0]]
                    item = self.item_coding[interaction[1][1]]
                    rate = interaction[1][2]
                    file.write(str(user) + ',' + str(item) + ',' + str(vec2rate(rate)) + '\n')


rater = RateCalculator(load_ratings=True)
rater.update_user_item_coding()
# rater.mother_process()
