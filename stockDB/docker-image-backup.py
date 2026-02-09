import docker


# Define image details
LOCAL_IMAGE_NAME = "test_mysql_image"  # The name of your existing local image
REPO_NAME = "liulirun/mysql-stock2"  # Replace 'myuser' with your registry username
TAG_1 = "v0.0.1-a"
TAG_2 = "v0.0.1-b"


class DockerBackup:
    def __init__(self):
        self.IF_DEBUG = True
        self.client = docker.from_env()

    def push_mysql_image(self, container_name="db", repo="liulirun/mysql-stock2"):
        container = self.client.containers.get(container_id=container_name)
        container.commit(container_name, tag=TAG_1)
        for line in self.client.images.push(
            repository=repo, tag=TAG_1, stream=True, decode=True
        ):
            print(line)
        print("docker updated")

    #    4        2.101 docker build -t test-mysql-image .
    #    5       39.158 docker build -t test-mysql-image .
    #    6        0.566 docker run -d --name my-custom-db -p 3306:3306 test-mysql-image
    #    7        0.099 docker tag test-my-sql-image:0.0.1 liulirun/mysql-stock2:v0.0.1
    #    8        0.092 docker image ls
    #    9        0.089 docker tag test-my-sql-image:latest liulirun/mysql-stock2:v0.0.1
    #   10        0.087 docker tag test-mysql-image:0.0.1 liulirun/mysql-stock2:v0.0.1
    #   11        0.100 docker tag test-mysql-image:latest liulirun/mysql-stock2:v0.0.1
    #   12        5.820 docker push liulirun/mysql-stock2:v0.0.1
    #   13        0.267 docker push liulirun/mysql-stock2:latest
    #   14        0.094 history
    #   15        0.105 docker tag test-mysql-image:latest liulirun/mysql-stock2:latest
    #   16        2.478 docker push liulirun/mysql-stock2:latest
    #   17        0.067 docker image ls

    def image_backup(self):
        # 1. Tag the local image with the first remote tag
        try:
            image = self.client.images.get(name=LOCAL_IMAGE_NAME)
            for tag_name in [TAG_1, TAG_2]:
                image.tag(REPO_NAME, tag_name)
                print(f"Image tagged as {REPO_NAME}:{tag_name}")
        except docker.errors.ImageNotFound:
            print(f"Error: Local image '{LOCAL_IMAGE_NAME}' not found.")
            exit()

        # 2. Push the first tagged image to the remote repository
        try:
            for tag_name in [TAG_1, TAG_2]:
                # The push method yields status information, which can be iterated over
                for line in self.client.images.push(
                    repository=REPO_NAME, tag=tag_name, stream=True, decode=True
                ):
                    print(line)
                print(f"Successfully pushed {REPO_NAME}:{tag_name}")
        except Exception as e:
            print(f"Error pushing {REPO_NAME}:{tag_name}: {e}")


if __name__ == "__main__":
    b = DockerBackup()
    b.push_mysql_image()
