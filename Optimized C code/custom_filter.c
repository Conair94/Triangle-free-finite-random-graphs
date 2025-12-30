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

/*
 * Checks if all pairs of disjoint independent sets of size 3 have a common neighbor.
 * That is, for any two independent sets A and B with |A|=3, |B|=3, and A disjoint from B,
 * there exists a vertex z adjacent to all vertices in A U B.
 */
boolean is_3_existential(graph *g, int m, int n) {
    int triplets[2000][3]; // 16 choose 3 is 560.
    int num_triplets = 0;
    int i, j, k;
    setword *gi, *gj;
    
    // 1. Collect independent sets of size 3
    for (i = 0; i < n; i++) {
        gi = GRAPHROW(g, i, m);
        for (j = i + 1; j < n; j++) {
            if (ISELEMENT(gi, j)) continue;
            gj = GRAPHROW(g, j, m);
            for (k = j + 1; k < n; k++) {
                if (ISELEMENT(gi, k)) continue;
                if (ISELEMENT(gj, k)) continue;
                
                triplets[num_triplets][0] = i;
                triplets[num_triplets][1] = j;
                triplets[num_triplets][2] = k;
                num_triplets++;
            }
        }
    }

    // 2. Check pairs of triplets
    for (int t1 = 0; t1 < num_triplets; t1++) {
        for (int t2 = t1 + 1; t2 < num_triplets; t2++) {
             int *A = triplets[t1];
             int *B = triplets[t2];
             
             // Check disjointness
             if (A[0] == B[0] || A[0] == B[1] || A[0] == B[2]) continue;
             if (A[1] == B[0] || A[1] == B[1] || A[1] == B[2]) continue;
             if (A[2] == B[0] || A[2] == B[1] || A[2] == B[2]) continue;
             
             // Disjoint. Check common neighbor for A U B.
             boolean found = FALSE;
             for (int v = 0; v < n; v++) {
                 // Check adjacency to all 6 vertices
                 if (ISELEMENT(GRAPHROW(g, A[0], m), v) &&
                     ISELEMENT(GRAPHROW(g, A[1], m), v) &&
                     ISELEMENT(GRAPHROW(g, A[2], m), v) &&
                     ISELEMENT(GRAPHROW(g, B[0], m), v) &&
                     ISELEMENT(GRAPHROW(g, B[1], m), v) &&
                     ISELEMENT(GRAPHROW(g, B[2], m), v)) {
                     found = TRUE;
                     break;
                 }
             }
             
             if (!found) return FALSE;
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
            char *s = ntog6(g, m, n);
            size_t len = strlen(s);
            if (len > 0 && s[len-1] == '\n') s[len-1] = '\0';
            printf("%s,%d\n", s, is_3_existential(g, m, n));
        }
        FREES(g);
    }

    exit(0);
}