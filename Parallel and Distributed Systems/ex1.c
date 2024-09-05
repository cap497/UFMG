// Raphael Alves dos Reis

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define MAX_N 20  // Maximum size of the grid

typedef struct {
    int id;                // Thread identifier
    int group;             // Thread group identifier
    int num_positions;     // Number of positions the thread will visit
    int positions[MAX_N * 2][3]; // Stores positions and time to stay in each position
} ThreadInfo;

int N, n_threads;  // N is the size of the grid, n_threads is the number of threads
ThreadInfo threads[MAX_N]; // Array of thread information
pthread_mutex_t lock_grid[MAX_N][MAX_N]; // Mutex for each position on the grid
pthread_cond_t cond_grid[MAX_N][MAX_N];  // Condition for each position on the grid
int occupancy[MAX_N][MAX_N]; // Tracks which group is occupying each position

// Function to simulate passing time at a grid position
void passa_tempo(int tid, int x, int y, int decimos) {
    struct timespec zzz, agora;
    static struct timespec inicio = {0, 0};
    int tstamp;

    // Initialize start time if not already set
    if ((inicio.tv_sec == 0) && (inicio.tv_nsec == 0)) {
        clock_gettime(CLOCK_REALTIME, &inicio);
    }

    // Set sleep duration
    zzz.tv_sec = decimos / 10;
    zzz.tv_nsec = (decimos % 10) * 100L * 1000000L;

    // Log start time
    clock_gettime(CLOCK_REALTIME, &agora);
    tstamp = (10 * agora.tv_sec + agora.tv_nsec / 100000000L) -
             (10 * inicio.tv_sec + inicio.tv_nsec / 100000000L);

    printf("%3d [ %2d @(%2d,%2d) z%4d\n", tstamp, tid, x, y, decimos);
    nanosleep(&zzz, NULL); // Sleep for the specified time

    // Log end time
    clock_gettime(CLOCK_REALTIME, &agora);
    tstamp = (10 * agora.tv_sec + agora.tv_nsec / 100000000L) -
             (10 * inicio.tv_sec + inicio.tv_nsec / 100000000L);
    printf("%3d ) %2d @(%2d,%2d) z%4d\n", tstamp, tid, x, y, decimos);
}

// Thread function
void *thread_func(void *arg) {
    ThreadInfo *info = (ThreadInfo *)arg;
    int x, y, wait_time;

    for (int i = 0; i < info->num_positions; i++) {
        x = info->positions[i][0];
        y = info->positions[i][1];
        wait_time = info->positions[i][2];

        // Acquire the lock for the current position
        pthread_mutex_lock(&lock_grid[x][y]);

        // Wait until the condition is satisfied
        while (occupancy[x][y] != 0 && occupancy[x][y] == info->group) {
            pthread_cond_wait(&cond_grid[x][y], &lock_grid[x][y]);
        }

        // Enter the position
        occupancy[x][y] = info->group;
        passa_tempo(info->id, x, y, wait_time);
        occupancy[x][y] = 0;  // Vacate the position

        // Signal to other threads waiting for this position
        pthread_cond_broadcast(&cond_grid[x][y]);
        pthread_mutex_unlock(&lock_grid[x][y]);
    }

    return NULL;
}

// Main function to set up threads and read input
int main() {
    // Read grid size and number of threads
    scanf("%d %d", &N, &n_threads);
    for (int i = 0; i < n_threads; i++) {
        scanf("%d %d %d", &threads[i].id, &threads[i].group, &threads[i].num_positions);
        for (int j = 0; j < threads[i].num_positions; j++) {
            scanf("%d %d %d", &threads[i].positions[j][0], &threads[i].positions[j][1], &threads[i].positions[j][2]);
        }
    }

    // Initialize mutexes and condition variables
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            pthread_mutex_init(&lock_grid[i][j], NULL);
            pthread_cond_init(&cond_grid[i][j], NULL);
            occupancy[i][j] = 0;
        }
    }

    pthread_t tids[MAX_N]; // Array to hold thread identifiers
    // Create threads
    for (int i = 0; i < n_threads; i++) {
        pthread_create(&tids[i], NULL, thread_func, &threads[i]);
    }

    // Wait for all threads to complete
    for (int i = 0; i < n_threads; i++) {
        pthread_join(tids[i], NULL);
    }

    // Destroy mutexes and condition variables
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            pthread_mutex_destroy(&lock_grid[i][j]);
            pthread_cond_destroy(&cond_grid[i][j]);
        }
    }

    return 0;
}
