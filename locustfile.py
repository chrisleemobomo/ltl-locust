from locust import HttpLocust, TaskSet, task, TaskSequence, seq_task
from realbrowserlocusts import FirefoxLocust, ChromeLocust, PhantomJSLocust, HeadlessChromeLocust
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class WebsiteTasks(TaskSet):

    @task(1)
    def index(self):
        self.client.get("/")

    @task(1)
    def leagues(self):
        self.client.get("/leagues")

    @task(1)
    def about(self):
        self.client.get("/about")

    @task(1)
    def rules(self):
        self.client.get("/rulesandregulations")

    @task(1)
    def shop(self):
        self.client.get("/shop")

    @task(1)
    def blog(self):
        self.client.get("/roundup")

    @task(1)
    def user(self):
        self.client.get("/user")
        

class BackEndTasks(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.get("/user/login")
        soup = BeautifulSoup(response.text, "html.parser")
        drupal_form_id = soup.select('input[name="form_build_id"]')[0]["value"]
        r = self.client.post("/user/login", {"name":"user", "pass":"pw", "form_id":"user_login", "op":"Log+in", "form_build_id":drupal_form_id})

    @task(1)
    def landing(self):
        self.client.get("/", name="Main Landing Page")

    @task(1)
    def add_node(self):
        self.client.get("/node/add", name="Add Content Page")

    @task(1)
    def add_atom(self):
        self.client.get("/atom/add", name="Add Atom Page")

    @task(1)
    def status_report(self):
        self.client.get("/admin/reports/status", name="Status Report")

    # @task(10)
    # def add_node(self):
    #     self.client.get("node/add", name="Add Content Page")
    #
    # @task(10)
    # def add_node(self):
    #     self.client.get("node/add", name="Add Content Page")
    #
    # @task(10)
    # def add_node(self):
    #     self.client.get("node/add", name="Add Content Page")
    #
    # @task(10)
    # def add_node(self):
    #     self.client.get("node/add", name="Add Content Page")

class UserFlowTasks(TaskSequence):

    @seq_task(1)
    @task(1)
    def index(self):
        self.client.get("/", name="Step 1 Landing Page")

    # @seq_task(2)
    # @task(30)
    # def earthquakes(self):
    #     self.client.get("/science-explorer-results?es=earthquakes", name="Step 2 Search Results Earthquake")

    # @seq_task(2)
    # @task(1)
    # def earthquakes(self):
    #     self.client.get("/news/kilauea-volcano-erupts", name="Step 2 Kilauea Article")
    #
    # @seq_task(3)
    # @task(1)
    # def earthquakes_media(self):
    #     self.client.get("/media/images/k-lauea-volcano-fissure-8-aerial", name="Step 3 Kilauea Image")



class ChromeTasks(TaskSet):

    @task(1)
    def hp(self):
        self.client.get("/")

    @task(1)
    def pubs(self):
        self.client.get("/")








class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 20000


class WebsiteUserFlow(HttpLocust):
    task_set = UserFlowTasks
    min_wait = 5000
    max_wait = 20000


class BackEndUser(HttpLocust):
    task_set = BackEndTasks
    screen_width = 1200
    screen_height = 600
    min_wait = 5000
    max_wait = 20000


class ChromeUser(HeadlessChromeLocust):
    task_set = ChromeTasks
    timeout = 30
    screen_width = 1200
    screen_height = 1080
    min_wait = 5000
    max_wait = 50000
