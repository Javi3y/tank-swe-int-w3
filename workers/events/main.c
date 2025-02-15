#include <libpq-fe.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <jansson.h>

int main(void) {
    // Connection string; update with your PostgreSQL credentials
    const char *conninfo = "host=localhost port=5432 dbname=fapi user=postgres password=changeme";

    // Connect to the database
    PGconn *conn = PQconnectdb(conninfo);
    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "Connection to database failed: %s\n", PQerrorMessage(conn));
        PQfinish(conn);
        exit(EXIT_FAILURE);
    }
    printf("Connected to PostgreSQL successfully.\n");

    while (1) {
        PGresult *res = PQexec(conn, 
            "SELECT * FROM event WHERE event_status = 'pending' "
            "AND timestamp >= now() AND timestamp <= now() + interval '61 seconds';"
        );

        if (PQresultStatus(res) != PGRES_TUPLES_OK) {
            fprintf(stderr, "SELECT failed: %s\n", PQerrorMessage(conn));
            PQclear(res);
            PQfinish(conn);
            exit(EXIT_FAILURE);
        }

        int nrows = PQntuples(res);
        // Get column indexes for "id" and "payload"
        int id_index = PQfnumber(res, "id");
        int payload_index = PQfnumber(res, "payload");

        for (int i = 0; i < nrows; i++) {
            if (payload_index >= 0 && id_index >= 0) {
                const char *payload_val = PQgetvalue(res, i, payload_index);
                const char *event_id_str = PQgetvalue(res, i, id_index);

                json_error_t error;
                json_t *json_payload = json_loads(payload_val, 0, &error);
                if (!json_payload) {
                    fprintf(stderr, "Error parsing JSON in row %d: %s\n", i + 1, error.text);
                    // Print original payload if JSON parsing fails
                    printf("payload: %s\n", payload_val);
                } else {
                    // Insert the event_id into the JSON object
                    json_object_set_new(json_payload, "event_id", json_string(event_id_str));
                    // Convert modified JSON to a compact string
                    char *new_payload = json_dumps(json_payload, JSON_COMPACT);
                    printf("%s\n", new_payload);
                    free(new_payload);
                    json_decref(json_payload);
                }
            } else {
                printf("payload: (column not found)\n");
            }
        }

        PQclear(res);
        sleep(10);
    }

    PQfinish(conn);
    return 0;
}
