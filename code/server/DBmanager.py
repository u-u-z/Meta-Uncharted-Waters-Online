import pickle

# add relative directory to python_path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

# import from common(dir)
from role import Role
from role import Ship
from role import Mate
import constants as c

class Database:
    # data table
    def create_character(self, account, character_name):
        # exists?
        try:
            player = pickle.load(open("data/save." + account, "rb"))
            print("exists!")
            return False

        # no
        except:
            # check if role name exists
            sql_read = "SELECT * FROM accounts WHERE role = '{}'". \
                format(character_name)
            print(sql_read)
            self.cursor.execute(sql_read)
            rows = self.cursor.fetchall()

            # exists
            if rows:
                return False

            # not exist
            else:
                if str(character_name).isdigit():
                    return False
                else:
                    # set role name in DB
                    sql_update = "UPDATE accounts SET role = '{}' WHERE name = '{}'".\
                        format(character_name,account)
                    print(sql_update)
                    self.cursor.execute(sql_update)
                    self.db.commit()

                    # developer mode
                    if c.DEVELOPER_MODE_ON:
                        self._make_developer_mode_role(account, character_name)
                    else:
                        self._make_normal_role(account, character_name)

                    return True

    def _make_developer_mode_role(self, account, character_name):
        x = y = c.PIXELS_COVERED_EACH_MOVE
        default_role = Role(x, y, character_name)

        mate0 = Mate(1)
        mate0.name = character_name
        default_role.mates.append(mate0)
        default_role.discoveries[2] = 1

        ship0 = Ship('Reagan', 'Frigate')
        ship0.crew = 300
        default_role.ships.append(ship0)
        mate0.set_as_captain_of(ship0)

        for i in range(9):
            # add ship
            ship1 = Ship('Reagan1', 'Frigate')
            ship1.crew = 300
            ship1.now_hp = 60
            default_role.ships.append(ship1)

            # add mate
            mate1 = Mate(i + 2)
            default_role.mates.append(mate1)
            mate1.set_as_captain_of(ship1)

        default_role.mates[0].exp = 10000

        pickle.dump(default_role, open("data/save." + account, "wb"))
        print("new player created!")

    def _make_normal_role(self, account, character_name):
        x = y = c.PIXELS_COVERED_EACH_MOVE
        default_role = Role(x, y, character_name)

        mate0 = Mate(1)
        mate0.name = character_name
        default_role.mates.append(mate0)
        default_role.discoveries[2] = 1

        ship0 = Ship('Sheep', 'Balsa')
        ship0.crew = 5
        default_role.ships.append(ship0)
        mate0.set_as_captain_of(ship0)

        pickle.dump(default_role, open("data/save." + account, "wb"))
        print("new player created!")

    def get_character_data(self, account, nickname):
        try:
            return pickle.load(open("data/save." + account, "rb"))
        except:
            if c.DEVELOPER_MODE_ON:
                return self._make_developer_mode_role(account, nickname)
            else:
                return self._make_normal_role(account, nickname)

    def save_character_data(self, account, player):

        # save to file
        pickle.dump(player, open("data/save." + account, "wb"))
        print("saved!")

    def set_online_to_false(self, account):
        sql_update = "UPDATE accounts SET online = '0' WHERE name = '{}'". \
            format(account)
        print(sql_update)
        self.cursor.execute(sql_update)
        self.db.commit()

if __name__ == '__main__':
    pass
    # db = Database()
    # # db.register('test2', 'a9901025')
    # id, account = db.login('t21', 't21')
    # db.create_character(id, account, "你好")
    # player = db.get_character_data(account)
    # print(player.name)
    # player.name = 'new_name'
    #
    # db.save_character_data(account, player)

