def get_fixed_windows(image_size, wind_size, overlap_size):
    '''
    This function can generate overlapped windows given various image size
    params:
        image_size (w, h): the image width and height
        wind_size (w, h): the window width and height
        overlap (overlap_w, overlap_h): the overlap size contains x-axis and y-axis

    return:
        rects [(xmin, ymin, xmax, ymax)]: the windows in a list of rectangles
    '''
    rects = set()

    assert overlap_size[0] < wind_size[0]
    assert overlap_size[1] < wind_size[1]

    im_w = wind_size[0] if image_size[0] < wind_size[0] else image_size[0]
    im_h = wind_size[1] if image_size[1] < wind_size[1] else image_size[1]

    stride_w = wind_size[0] - overlap_size[0]
    stride_h = wind_size[1] - overlap_size[1]

    for j in range(wind_size[1], im_h + stride_h, stride_h):
        for i in range(wind_size[0], im_w + stride_w, stride_w):
            right, down = i, j
            right = right if right < im_w else im_w
            down  =  down if down < im_h  else im_h

            left = right - wind_size[0]
            up   = down  - wind_size[1]

            rects.add((left, up, right, down))

    return list(rects)

temp = get_fixed_windows((800, 700), (300, 200), (200, 100))