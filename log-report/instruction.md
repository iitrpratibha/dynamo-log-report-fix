# Access log report

There is an Apache-style access log at /app/access.log. Each line is one HTTP request in the common log format, for example:

    192.168.0.1 - - [16/Jun/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024

Read the log and write a JSON summary to /app/report.json. It must be a single JSON object with exactly these keys:

- total_requests (integer): how many requests are in the log. Count one per non-empty line.
- unique_ips (integer): how many distinct client IPs appear. The client IP is the first field on each line.
- top_path (string): the request path that shows up in the most requests. The path is the second token inside the quoted request line, for example /index.html in "GET /index.html HTTP/1.1".

## Success criteria

1. /app/report.json exists and is a single JSON object.
2. total_requests matches the number of requests in /app/access.log.
3. unique_ips matches the number of distinct client IPs in the log.
4. top_path is the path with the most requests.

You have 120 seconds to complete this task.
