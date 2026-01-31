import docker


class Backup:
    def __init__(self):
        self.IF_DEBUG = False
        self.client = docker.from_env()

    def run(self):
        self.backup_mysql()
        self.push_mysql_image()

    def backup_mysql(self, container_name="mysql-stock2"):
        for container in self.client.containers.list():
            if (container.name == container_name):
                c = self.client.containers.get(container.short_id)
                res = c.exec_run(
                    '/bin/sh -c "rm /var/lib/mysql/bk_stock.sql && mysqldump -u root -pmysql_pass --databases stock > /var/lib/mysql/bk_stock.sql && ls /var/lib/mysql/bk_stock.sql"')
                if self.IF_DEBUG:
                    print(res)

    def push_mysql_image(self, image_name="liulirun/mysql-stock2"):
        container = self.client.containers.get('mysql-stock2')
        container.commit('mysql-stock2', tag='latest')
        for line in self.client.images.push(image_name, tag='latest', stream=True, decode=True):
            print(line)
        print('docker updated')

if __name__ == "__main__":
    b = Backup()
    b.run()
