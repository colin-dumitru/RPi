import threading
import time
import smbus
import sqlite3

ADDR = 0x48

class Temp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
	    
        self.name = 'temp'
        self.daemon = True

        self.table_name = 'temp_points'
        self.refresh_period = 15 * 60 # 15 minutes
        self.expired_time = 2 * 24 * 60 * 60 # two days

    def init(self, app):
        self.app = app
        self.bus = smbus.SMBus(1)
        self.conn = sqlite3.connect('temperature.db', check_same_thread = False, isolation_level = None)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()

        self.cursor.execute( 'create table if not exists ' + self.table_name + ' (time integer, temp real)')
        self.conn.commit()

        self.start()

    def get_temp(self):
        word = self.bus.read_word_data(ADDR , 0 )
        lsb = (word & 0xff00) >> 8 
        msb = (word & 0x00ff)
        
        return ((( msb * 256 ) + lsb) >> 4 ) * 0.0625

    def store_temp(self):
        temp = self.get_temp()
        current_time = int(time.time())
        sql = 'insert into ' + self.table_name + ' (time,temp) values (%d,%f)' % (current_time, temp)

        self.lock.acquire()
        self.cursor.execute(sql)
        self.conn.commit()
        self.lock.release()

    def delete_old_values(self):
        current_time = int(time.time())
        sql = 'delete from ' + self.table_name + ' where time < %d' % (current_time - self.expired_time)

        self.lock.acquire()
        self.cursor.execute(sql)
        self.conn.commit()
        self.lock.release()

    def get_stored_values(self):
       sql = 'select * from ' + self.table_name + ' order by time asc'

       self.lock.acquire()
       self.cursor.execute(sql)
       values = self.cursor.fetchall()
       self.lock.release()

       return values

    def run(self):
        while True:
            self.store_temp()
            self.delete_old_values()
            time.sleep(self.refresh_period)

    def process(self, params):
        action = params
        
        if action == 'read':
            return self.get_temp()
        if action == 'get_past':
            return self.get_stored_values()
        
