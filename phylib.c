#include "phylib.h"


/* phylib_new_still_ball function to create new still ball */
phylib_object *phylib_new_still_ball(unsigned char number,
                                        phylib_coord *pos) {

    // allocate memory for a new still ball
    phylib_object *new_still_ball = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_still_ball == NULL) {
        return NULL; // if memory allocation failure
    }

    // set attributes
    new_still_ball->type = PHYLIB_STILL_BALL;
    new_still_ball->obj.still_ball.number = number;
    new_still_ball->obj.still_ball.pos = *pos;

    // return pointer to the new ball
    return new_still_ball;

} // end of phylib_new_still_ball


/* phylib_new_rolling_ball function to create new rolling ball */
phylib_object *phylib_new_rolling_ball(unsigned char number,
                                        phylib_coord *pos,
                                        phylib_coord *vel,
                                        phylib_coord *acc) {

    // allocate memory for a new rolling ball
    phylib_object *new_rolling_ball = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_rolling_ball == NULL) {
        return NULL; // if memory allocation failure
    }

    // set attributes
    new_rolling_ball->type = PHYLIB_ROLLING_BALL;
    new_rolling_ball->obj.rolling_ball.number = number;
    new_rolling_ball->obj.rolling_ball.pos = *pos;
    new_rolling_ball->obj.rolling_ball.vel = *vel;
    new_rolling_ball->obj.rolling_ball.acc = *acc;

    // return pointer to the new ball
    return new_rolling_ball;

} // end of phylib_new_rolling_ball


/* phylib_new_hole function to create new hole */
phylib_object *phylib_new_hole(phylib_coord *pos) {

    // allocate memory for a new hole
    phylib_object *new_hole = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_hole == NULL) {
        return NULL; // if memory allocation failure
    }

    // set attributes
    new_hole->type = PHYLIB_HOLE;
    new_hole->obj.hole.pos = *pos;

    // return pointer to the new hole
    return new_hole;

} // end of phylib_new_hole


/* phylib_new_hcushion function to create new horizontal cushion */
phylib_object *phylib_new_hcushion(double y) {

    // allocate memory for a new horizontal cushion
    phylib_object *new_hcushion = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_hcushion == NULL) {
        return NULL; // if memory allocation failure
    }

    // set attributes
    new_hcushion->type = PHYLIB_HCUSHION;
    new_hcushion->obj.hcushion.y = y;

    // return pointer to the new cushion
    return new_hcushion;

} // end of phylib_new_hcushion


/* phylib_new_vcushion function to create new vertical cushion */
phylib_object *phylib_new_vcushion(double x) {

    // allocate memory for a new vertical cushion
    phylib_object *new_vcushion = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_vcushion == NULL) {
        return NULL; // if memory allocation failure
    }

    // set attributes
    new_vcushion->type = PHYLIB_VCUSHION;
    new_vcushion->obj.vcushion.x = x;

    // return pointer to the new cushion
    return new_vcushion;

} // end of phylib_new_vcushion


/* phylib_new_table function to create new table */
phylib_table *phylib_new_table(void) {

    // allocate memory for a new table
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));
    if (new_table == NULL) {
        return NULL; // if memory allocation failure
    }

    // set time to zero
    new_table->time = 0.0;

    // add 4 cushions
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // add 6 holes
    new_table->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0}); 
    new_table->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH});
    new_table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    new_table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    new_table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH});
    new_table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

    // set remaining pointers to NULL
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        new_table->object[i] = NULL;
    }

    // return pointer to the new table
    return new_table;

} // end of phylib_new_table


/* phylib_copy_object function to copy an object */
void phylib_copy_object(phylib_object **dest, phylib_object **src) {

    // if src points to a location containing a NULL pointer, location pointed to by dest assigned NULL
    if (*src == NULL) {
        *dest = NULL;
        return;
    }

    // allocate new memory for a phylib_object and save to *dest
    *dest = (phylib_object *)malloc(sizeof(phylib_object));
    if (*dest == NULL) {
        return; // if memory allocation failure
    }

    // copy contents of the object from the location pointed to by src
    memcpy(*dest, *src, sizeof(phylib_object));

} // end of phylib_copy_object


/* phylib_copy_table function to copy a table */
phylib_table *phylib_copy_table(phylib_table *table) {

    // check if pointer null
    if (table == NULL) {
        return NULL;
    }

    //  allocate memory for a new phylib_table
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));
    if (new_table == NULL) {
        return NULL; // if memory allocation failure
    }

    // copy contents pointed to by table to the new memory location
    new_table->time = table->time;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        phylib_copy_object(&(new_table->object[i]), &(table->object[i]));
    }

    // return address of the new table
    return new_table;

} // end of phylib_copy_table


/* phylib_add_object function to add an object to the table */
void phylib_add_object(phylib_table *table, phylib_object *object) {

    // iterate over object array in the table until NULL pointer found
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) {
            table->object[i] = object; // assign NULL pointer to be equal to the address of object
            return;
        }
    }

} // end of phylib_add_object


/* phylib_free_table function to free allocated memory */
void phylib_free_table(phylib_table *table) {

    if (table == NULL) {
        return;
    }

    // free every non-NULL pointer in the object array of table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }
    // free the table
    free(table);

} // end of phylib_free_table


/* phylib_sub function to calculate difference between c1 and c2 */
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {

    // calculate difference between c1 and c2 for x and y
    phylib_coord result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;

    // return the difference
    return result;

} // end of phylib_sub


/* phylib_length function to get the length of the vector/coordinate c */
double phylib_length(phylib_coord c) {

    // calculate length of vector/coordinate c using Pythagorean theorem
    double len = sqrt((c.x * c.x) + (c.y * c.y));

    return len; // return result

} // end of phylib_length


/* phylib_dot_product function to get the dot-product between two vectors */
double phylib_dot_product(phylib_coord a, phylib_coord b) {

    // compute dot-product (sum of the product of the x-values and the product of the y-values)
    double dot_prod = ((a.x * b.x) + (a.y * b.y));

    return dot_prod; // return result

} // end of phylib_dot_product


/* phylib_distance function to get the distance between two objects, where object 1 is a rolling ball */
double phylib_distance(phylib_object *obj1, phylib_object *obj2) {

    if (obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0; // invalid objects, obj1 must be a rolling ball
    }

    // initialize distance variable as 0
    double distance = 0.0;

    // for each obj2 type, calculate the distance
    switch (obj2->type) {

        case PHYLIB_STILL_BALL:
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
            break;
        case PHYLIB_ROLLING_BALL:
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
            break;
        case PHYLIB_HOLE:
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
            break;
        case PHYLIB_HCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            break;
        case PHYLIB_VCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;
        default:
            distance = -1.0; // invalid obj2 type
            break;

    }

    // return the distance
    return distance;

} // end of phylib_distance


/* phylib_roll function to update a new phylib_object that represents the old phylib_object after it
has rolled for a period of time. */
void phylib_roll(phylib_object *new, phylib_object *old, double time) {

    // check both objects are valid
    if (new == NULL || old == NULL || new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return; // do nothing if not rolling balls
    }

    // initialize variables for old vel, pos, and acc
    phylib_coord old_vel;
    old_vel.x = old->obj.rolling_ball.vel.x;
    old_vel.y = old->obj.rolling_ball.vel.y;

    phylib_coord old_pos;
    old_pos.x = old->obj.rolling_ball.pos.x;
    old_pos.y = old->obj.rolling_ball.pos.y;

    phylib_coord old_acc;
    old_acc.x = old->obj.rolling_ball.acc.x;
    old_acc.y = old->obj.rolling_ball.acc.y;

    // update velocities
    new->obj.rolling_ball.vel.x = old_vel.x + (old_acc.x * time);
    new->obj.rolling_ball.vel.y = old_vel.y + (old_acc.y * time);
    
    // update positions
    new->obj.rolling_ball.pos.x = old_pos.x + (old_vel.x * time) + (0.5 * old_acc.x * (time * time));
    new->obj.rolling_ball.pos.y = old_pos.y + (old_vel.y * time) + (0.5 * old_acc.y * (time * time));

    // if either velocity changes sign, then that velocity and its corresponding acceleration set to zero
    if ((new->obj.rolling_ball.vel.x * old_vel.x) < 0) {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }
    if ((new->obj.rolling_ball.vel.y * old_vel.y) < 0) {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }

} // end of phylib_roll


/* phylib_stopped function to check whether a ROLLING_BALL has stopped, if stopped then convert to STILL_BALL */
unsigned char phylib_stopped(phylib_object *object) {

    // check if object is a ROLLING_BALL
    if (object == NULL || object->type != PHYLIB_ROLLING_BALL) {
        return 0; // return 0 if ball not converted
    }

    // calculate speed of ball (length of velocity)
    double speed = phylib_length(object->obj.rolling_ball.vel);

    // ball stopped if its speed is less than PHYLIB_VEL_EPSILON
    if (speed < PHYLIB_VEL_EPSILON) {

        // convert the ROLLING_BALL to a STILL_BALL
        object->type = PHYLIB_STILL_BALL;
        // transfer attributes to the still ball
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;

        return 1; // return 1 if ball was converted 

    }

    return 0; // ball not converted

} // end of phylib_stopped


/* phylib_bounce function to handle object collisions, where object a is a ROLLING_BALL */
void phylib_bounce(phylib_object **a, phylib_object **b) {

    // initialize variables
    phylib_object * obj_a = *a;
    phylib_object * obj_b = *b;
    phylib_coord r_ab;
    phylib_coord v_rel;

    if (obj_a == NULL || obj_b == NULL || obj_a->type != PHYLIB_ROLLING_BALL) {
        return; // do nothing if object a not rolling ball
    }

    // case for each object b type
    switch (obj_b->type) {

        case PHYLIB_HCUSHION:
            // reflect in the y-direction
            obj_a->obj.rolling_ball.vel.y *= -1;
            obj_a->obj.rolling_ball.acc.y *= -1;
            break;
        case PHYLIB_VCUSHION:
            // reflect in the x-direction
            obj_a->obj.rolling_ball.vel.x *= -1;
            obj_a->obj.rolling_ball.acc.x *= -1;
            break;
        case PHYLIB_HOLE:
            // ball falls off the table, free memory and set to NULL
            free(*a);
            *a = NULL;
            a = NULL;
            break;
        case PHYLIB_STILL_BALL:
            // convert STILL_BALL to ROLLING_BALL
            obj_b->type = PHYLIB_ROLLING_BALL;
            // update attributes
            obj_b->obj.rolling_ball.number = obj_b->obj.still_ball.number;
            obj_b->obj.rolling_ball.pos.x = obj_b->obj.still_ball.pos.x;
            obj_b->obj.rolling_ball.pos.y = obj_b->obj.still_ball.pos.y;
            // set velocities and accelerations to 0
            obj_b->obj.rolling_ball.acc.x = 0;
            obj_b->obj.rolling_ball.acc.y = 0;
            obj_b->obj.rolling_ball.vel.x = 0;
            obj_b->obj.rolling_ball.vel.y = 0;
            // continue to case ROLLING_BALL
        case PHYLIB_ROLLING_BALL:
            // calculate the position and velocity differences
            r_ab = phylib_sub(obj_a->obj.rolling_ball.pos, obj_b->obj.rolling_ball.pos);
            v_rel = phylib_sub(obj_a->obj.rolling_ball.vel, obj_b->obj.rolling_ball.vel);
            phylib_coord n = {r_ab.x / phylib_length(r_ab), r_ab.y / phylib_length(r_ab)};
            double v_rel_n = phylib_dot_product(v_rel, n);

            // update velocities
            obj_a->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            obj_a->obj.rolling_ball.vel.y -= v_rel_n * n.y;
            obj_b->obj.rolling_ball.vel.x += v_rel_n * n.x;
            obj_b->obj.rolling_ball.vel.y += v_rel_n * n.y;

            // calculate speeds
            double speed_a = phylib_length(obj_a->obj.rolling_ball.vel);
            double speed_b = phylib_length(obj_b->obj.rolling_ball.vel);

            // apply drag if speed is greater than PHYLIB_VEL_EPSILON
            if (speed_a > PHYLIB_VEL_EPSILON) {
                obj_a->obj.rolling_ball.acc.x = (-(obj_a->obj.rolling_ball.vel.x) / speed_a * PHYLIB_DRAG);
                obj_a->obj.rolling_ball.acc.y = (-(obj_a->obj.rolling_ball.vel.y) / speed_a * PHYLIB_DRAG);
            }
            if (speed_b > PHYLIB_VEL_EPSILON) {
                obj_b->obj.rolling_ball.acc.x = (-(obj_b->obj.rolling_ball.vel.x) / speed_b * PHYLIB_DRAG);
                obj_b->obj.rolling_ball.acc.y = (-(obj_b->obj.rolling_ball.vel.y) / speed_b * PHYLIB_DRAG);
            }
            break;
        default:
            break;

    }

} // end of phylib_bounce

/* phylib_rolling function to get the number of ROLLING_BALLS on the table */
unsigned char phylib_rolling(phylib_table *t) {

    if (t == NULL) {
        return 0; // invalid table
    }

    // initialize counter to 0
    unsigned char num_rolling = 0;

    // iterate through objects array to count rolling balls
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            num_rolling++; // increment counter if rolling ball found
        }
    }

    return num_rolling; // return final count

} // end of phylib_rolling


/* phylib_segment function to return a segment of a pool shot */
phylib_table *phylib_segment(phylib_table *table) {
  
    double curr_time = PHYLIB_SIM_RATE;
  
    if (table == NULL || phylib_rolling(table) < 1) {
        return NULL; // if no ROLLING_BALLs on the table
    }

    // get a copy of the table
    phylib_table *segment_table = phylib_copy_table(table);
    if (!segment_table) {
        return NULL;
    }

    // loop over the time
    while(curr_time < PHYLIB_MAX_TIME) {
    
        // iterate through each object
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
      
            // check if the object is a ROLLING_BALL
            if(segment_table->object[i] && segment_table->object[i]->type == PHYLIB_ROLLING_BALL) {
                
                // apply phylib_roll to each ROLLING_BALL
                phylib_roll(segment_table->object[i], table->object[i], curr_time);

            }

        }
   
        for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {

            if(segment_table->object[j] && segment_table->object[j]->type == PHYLIB_ROLLING_BALL) {
      
                if (phylib_stopped(segment_table->object[j]) == 1) {
                    // if ROLLING_BALL has stopped, return the copied table
                    segment_table->time = segment_table->time + curr_time;
                    return segment_table;
                }
                for(int k = 0; k < PHYLIB_MAX_OBJECTS; k++) {
                    // get distance between the objects in case of collision
                    if(j != k && segment_table->object[k] && (phylib_distance(segment_table->object[j], segment_table->object[k]) < 0.0)) {
                        // if distance between the ball and another phylib_object is less than 0.0, apply bounce
                        phylib_bounce(&segment_table->object[j], &segment_table->object[k]);
                        segment_table->time = segment_table->time + curr_time;
                        return segment_table;
                    }
                }
            }
        }
        // Increase by sim rate
        curr_time = curr_time + PHYLIB_SIM_RATE;
    }

    segment_table->time = segment_table->time + curr_time;
    // if PHYLIB_MAX_TIME is reached, return the copied table
    return segment_table;

} // end of phylib_segment


/* phylib_object_string function to return objects as string */
char *phylib_object_string(phylib_object *object) {

    static char string[80];

    if (object==NULL) {

        snprintf( string, 80, "NULL;" );
        return string;

    }

    switch (object->type) {

        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
                    "STILL_BALL (%d,%6.1lf,%6.1lf)",
                    object->obj.still_ball.number,
                    object->obj.still_ball.pos.x,
                    object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
                    "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                    object->obj.rolling_ball.number,
                    object->obj.rolling_ball.pos.x,
                    object->obj.rolling_ball.pos.y,
                    object->obj.rolling_ball.vel.x,
                    object->obj.rolling_ball.vel.y,
                    object->obj.rolling_ball.acc.x,
                    object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
                    "HOLE (%6.1lf,%6.1lf)",
                    object->obj.hole.pos.x,
                    object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
                    "HCUSHION (%6.1lf)",
                    object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
                    "VCUSHION (%6.1lf)",
                    object->obj.vcushion.x );
            break;

    }

    return string;

} // end of phylib_object_string
