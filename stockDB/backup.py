import docker


class Backup:
    def __init__(self):
        self.IF_DEBUG = True
        self.client = docker.from_env()

    def run(self):
        self.backup_mysql(container_name="db")
        # self.push_mysql_image(
        #     container_name="mysql-stock2", repo="liulirun/mysql-stock2"
        # )

    def backup_mysql(self, container_name):
        for container in self.client.containers.list():
            if container.name == container_name:
                c = self.client.containers.get(container_id=container.short_id)
                # res = c.exec_run(
                #     '/bin/sh -c "rm /var/lib/mysql/bk_stock.sql && mysqldump -u root -pmysql_pass --databases stock > /var/lib/mysql/bk_stock.sql && ls /var/lib/mysql/bk_stock.sql"'
                # )
                res = c.exec_run(
                    '/bin/sh -c "mysqldump -u root -pmysql_pass --databases stock > /var/lib/mysql/bk_stock.sql && ls /var/lib/mysql/bk_stock.sql"'
                )
                if self.IF_DEBUG:
                    print(res)

    def push_mysql_image(
        self, container_name="mysql-stock2", repo="liulirun/mysql-stock2"
    ):
        container = self.client.containers.get(container_id=container_name)
        container.commit(container_name, tag="latest")
        for line in self.client.images.push(
            repository=repo, tag="latest", stream=True, decode=True
        ):
            print(line)
        print("docker updated")


if __name__ == "__main__":
    b = Backup()
    b.run()
