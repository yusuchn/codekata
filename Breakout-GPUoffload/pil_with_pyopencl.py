#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is a simple test to do image operations on pyopencl in combination with PIL
#
# based on the code of: https://gist.github.com/likr/3735779

import pyopencl as cl
import numpy

from PIL import Image


# initialize OpenCL
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# load and build OpenCL function
prg = cl.Program(ctx, '''//CL//
__kernel void convert(
    read_only image2d_t src,
    write_only image2d_t dest
)
{
    const sampler_t sampler =  CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;
    int2 pos = (int2)(get_global_id(0), get_global_id(1));
    uint4 pix = read_imageui(src, sampler, pos);

    // A simple test operation: delete pixel in form of a checkerboard pattern
    if((get_global_id(0)+((get_global_id(1)+1)%2)) % 2 == 0) {
        pix.x = 0;
        pix.y = 0;
        pix.z = 0;
    }

    write_imageui(dest, pos, pix);
    
    /////////////////////////////////////////////////////
    // added by sy for testing the image width and height
    int width = get_image_width(src);
    int height = get_image_height(src);

    if (pos.x < width && pos.y < height)
    {   
        uint4 black = (uint4)(0,0,0,0);

        if (pos.x % 2== 0)
        {   
            const uint4 outColor = black;
            write_imageui(dest, pos, outColor);
        }
        else
        {
            write_imageui(dest, pos, pix);
        }
    }    
    /////////////////////////////////////////////////////
}
''').build()

# load and convert source image
# src_img = Image.open('source.png').convert('RGBA')  # This example code only works with RGBA images
src_img = Image.open('fromserver_1..png').convert('RGBA')  # This example code only works with RGBA images
src = numpy.array(src_img)

# get size of source image (note height is stored at index 0)
h = src.shape[0]
w = src.shape[1]

# build a 2D OpenCL Image from the numpy array
src_buf = cl.image_from_array(ctx, src, 4)

# build destination OpenCL Image
fmt = cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNSIGNED_INT8)
dest_buf = cl.Image(ctx, cl.mem_flags.WRITE_ONLY, fmt, shape=(w, h))

# execute OpenCL function
prg.convert(queue, (w, h), None, src_buf, dest_buf)

# copy result back to host
dest = numpy.empty_like(src)
cl.enqueue_copy(queue, dest, dest_buf, origin=(0, 0), region=(w, h))

# convert image and save it
dest_img = Image.fromarray(dest)
dest_img.save('result_1.png', "PNG")