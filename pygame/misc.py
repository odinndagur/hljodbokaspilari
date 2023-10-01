def mapf(val, in_min, in_max, out_min, out_max, clamped=False):
    new_val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if clamped:
        if new_val < 0:
            new_val = 0
        if new_val > out_max:
            new_val = out_max
    return new_val

