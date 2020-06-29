from Core.Time import Time


def animate_property(lambda_get, lambda_set, property_keys, interpolate=True, post_lambda=None):
    current_key = 0

    while current_key < len(property_keys):
        start_value = lambda_get()
        target_value = property_keys[current_key][0]
        time_to_do = property_keys[current_key][1]
        if interpolate:
            value_difference = target_value - start_value

        time_done = 0.0
        while time_done < time_to_do:
            time_done += Time().delta_time()
            if time_done > time_to_do:
                lambda_set(target_value)
                break
            if interpolate:
                lambda_set(start_value + value_difference * (time_done / time_to_do))
            yield
        current_key += 1

    if post_lambda is not None:
        post_lambda()
