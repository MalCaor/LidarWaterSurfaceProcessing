def point_movement_line(baril_centre_arrays):
    list_line_frame = []

    previous_cloud = []
    for bc_point_cloud in baril_centre_arrays:
        if previous_cloud:
            # compare points
            pass
        # store previous state
        previous_cloud = bc_point_cloud
