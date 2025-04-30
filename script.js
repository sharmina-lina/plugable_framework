
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function () {
    // Define the URL of the frontend service
    let url = 'http://localhost:8080';

    // Send a GET request to the frontend service
    let res = http.get(url);

    // Check if the response status is 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });

    // Sleep for 1 second between iterations
    sleep(1);
}

    