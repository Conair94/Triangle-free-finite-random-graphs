#include "gtools.h"

/* 
 * checks if the graph is maximal triangle-free.
 * A triangle-free graph is maximal if adding any edge creates a triangle.
 * This is equivalent to: Every pair of non-adjacent vertices has at least one common neighbor.
 */
boolean is_maximal_triangle_free(graph *g, int m, int n) {
    setword *gi, *gj;
    int i, j, k;
    boolean has_common;

    for (i = 0; i < n; i++) {
        gi = GRAPHROW(g, i, m);
        for (j = i + 1; j < n; j++) {
            if (ISELEMENT(gi, j)) continue; // Already adjacent

            gj = GRAPHROW(g, j, m);
            
            // Check for common neighbor (intersection of neighbor sets)
            has_common = FALSE;
            for (k = 0; k < m; k++) {
                if (gi[k] & gj[k]) {
                    has_common = TRUE;
                    break;
                }
            }

            if (!has_common) return FALSE; // Non-adjacent pair with no common neighbor -> can add edge without triangle
        }
    }
    return TRUE;
}

/*
 * Checks if the graph is twin-free.
 * A graph is twin-free if no two vertices have identical neighborhoods.
 */
boolean is_twin_free(graph *g, int m, int n) {
    setword *gi, *gj;
    int i, j, k;
    boolean identical;

    for (i = 0; i < n; i++) {
        gi = GRAPHROW(g, i, m);
        for (j = i + 1; j < n; j++) {
            gj = GRAPHROW(g, j, m);

            // Check if neighborhoods are identical
            identical = TRUE;
            for (k = 0; k < m; k++) {
                if (gi[k] != gj[k]) {
                    identical = FALSE;
                    break;
                }
            }
            if (identical) return FALSE; // Found twins
        }
    }
    return TRUE;
}

int main(int argc, char *argv[]) {
    graph *g;
    int m, n;
    
    // Initialize nauty/gtools environment if needed (usually not for simple tools)
    // readg reads from a FILE*. We use stdin.
    // readg signature: graph *readg(FILE *f, graph *g, int reqm, int *m, int *n)
    
    while ((g = readg(stdin, NULL, 0, &m, &n)) != NULL) {
        if (is_twin_free(g, m, n) && is_maximal_triangle_free(g, m, n)) {
            writeg6(stdout, g, m, n);
        }
        FREES(g);
    }

    exit(0);
}