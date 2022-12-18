# Project Goal

To make an API to fetch the latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.


# Basic Requirements

- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
- Dockerize the project.
- It should be scalable and optimised.


# Running the Project

1. Clone the repository.
    ```commandline
    git clone https://github.com/siddydutta/YouTube-Search.git
    ```


2. Add environment variables.
    ```commandline
    cd YouTube-Search/
    touch .env
    ```
    <details>
        <summary>Sample variables.</summary>
   
   ```properties
    DATABASE_URL=postgresql://postgres:root@db/youtube
    DEVELOPER_KEY=yOuTubeApIKey
    SEARCH_QUERY=F1
    REFRESH_ENABLED=true
    REFRESH_INTERVAL=24
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=root
    POSTGRES_DB=youtube
    ```
   </details>


3. Start application.
   ```commandline
   docker-compose up --build
   ```


# API Usage

- Get all videos.
   ```shell
   curl -XGET 'http://127.0.0.1/videos?page=1&limit=10'
   ```
- Search videos.
   ```shell
   curl -XGET 'http://127.0.0.1/videos/search?query=f1'
   ```
- Refresh Database Manually
   ```shell
   curl -XGET 'http://127.0.0.1/refresh'
   ```
