import docker


class Backup:
    def __init__(self):
        self.docker_client = docker.from_env()

    def backup_mysql(self, container_name="mysql-stock2"):
        print("Backup.backup_mysql() started")
        for container in self.docker_client.containers.list():
            if (container.name == container_name):
                c = self.docker_client.containers.get(container.short_id)
                res = c.exec_run(
                    '/bin/sh -c "rm /var/lib/mysql/bk_stock.sql && mysqldump -u root -pmysql_pass --databases stock > /var/lib/mysql/bk_stock.sql && ls /var/lib/mysql/bk_stock.sql"')
                print(res)

    def push_mysql_image(self, image_name="liulirun/mysql-stock2"):
        print("Backup.push_mysql_image() started")

        image = self.docker_client.images.get("{}:latest".format(image_name))
        image.tag(image_name, tag='latest')
        for line in self.docker_client.images.push(image_name, tag='latest', stream=True, decode=True):
            print(line)


if __name__ == "__main__":
    b = Backup()
    b.backup_mysql()
    b.push_mysql_image()
