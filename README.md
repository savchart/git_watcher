<h1>Github Events Viewer</h1>
Description:

This application is a simple web-based viewer for Github events data. 
The user can enter the name of a Github repository and view the average time between pull requests.
And the count of events by type, and graph of events by type.

Requirements: Docker

Here are the steps to run the application:
1. Clone the repository: `git clone https://github.com/savchart/git_watcher.git`
2. Change directory: `cd git_watcher`
3. Build the Docker image: `docker build -t git_watcher .`
4. Start the container: `docker run -p 8000:8000 --net host git_watcher`
5. Access the app in your web browser at `localhost`.
6. To stop the Docker container, run the following command: `docker stop $(docker ps -aq --filter ancestor=git_watcher)`


The following diagram shows the C4 model for this application:

            +-------------+
            |   Browser   |
            +-------------+
                    |
                    |
            +-------------+
            |     Web     |
            |   Browser   |
            +-------------+
                    |
                    |
            +-------------+
            |   Flask     |
            |   Server    |
            +-------------+
                    |
                    |
            +-------------+
            |   Github    |
            |   API       |
            +-------------+

The diagram shows four components: the user's browser, a web browser, a Flask server, and the Github API. 
The user interacts with the application through their browser, which sends requests to the Flask server. 
The server then makes requests to the Github API to retrieve data about events in the specified repository, 
and returns the results to the user's browser for display.
